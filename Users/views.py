from django.shortcuts import render
from concurrent.futures import process

# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages

#import Text_Based_Emotion_Detection

from .forms import UserRegistrationForm
from .models import UserRegistrationModel
from django.conf import settings



def userbase(request):
    return render (request,'users/userbase.html')




def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'userregistration.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'userregistration.html',{'form':form})

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(
                loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/userhome.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'userlogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'userlogin.html', {})



def UserHome(request):
    return render(request, 'users/userhome.html', {})



import os
from django.conf import settings
import pandas as pd
from django.shortcuts import render

def DatasetView(request):
    # Construct the file path using os.path.join for better cross-platform compatibility
    path = os.path.join(settings.MEDIA_ROOT, 'crime_dataset_india.csv')

    # Check if the file exists before proceeding
    if os.path.exists(path):
        # Read the CSV file
        d = pd.read_csv(path)

        # Convert DataFrame to a list of dictionaries for easier rendering in template
        if not d.empty:
            df = d.to_dict(orient='records')  # Convert DataFrame rows to dictionaries
            return render(request, 'users/datasetview.html', {'df': df})
        else:
            return render(request, 'users/datasetview.html', {'error': 'Dataset is empty.'})
    else:
        return render(request, 'users/datasetview.html', {'error': 'File not found.'})
import os
import pandas as pd
import joblib
from django.conf import settings
from django.shortcuts import render
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report
from scipy.sparse import save_npz, load_npz  # For saving sparse matrices
from scipy.sparse import hstack, csr_matrix

# Convert DataFrame to sparse matrix before stacking
def training(request):
    # Define dataset path
    path = os.path.join(settings.MEDIA_ROOT, 'crime_dataset_india.csv')

    # Load dataset
    df = pd.read_csv(path)

    # Remove unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Handle missing values
    df.fillna("Unknown", inplace=True)

    # Separate features (X) and target variable (y)
    X = df.drop(['Crime Domain'], axis=1)
    y = df['Crime Domain']

    # One-hot encode categorical features (using sparse_output=True)
    onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
    X_encoded = onehot_encoder.fit_transform(X)  # This now returns a sparse matrix

    # Save encoder for later use
    joblib.dump(onehot_encoder, os.path.join(settings.MEDIA_ROOT, 'onehot_encoder.joblib'))
    save_npz(os.path.join(settings.MEDIA_ROOT, 'X_encoded.npz'), X_encoded)  # Save sparse matrix

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

    # Encode target labels
    label_encoder = LabelEncoder()
    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.transform(y_test)

    # Train Random Forest model
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # Save model and encoders
    joblib.dump(rf, os.path.join(settings.MEDIA_ROOT, 'Crime_RF.joblib'))
    joblib.dump(label_encoder, os.path.join(settings.MEDIA_ROOT, 'label_encoder.joblib'))

    # Model evaluation
    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    return render(request, 'users/training.html', {
        'accuracy': accuracy,
        'classification_report': report
    })

import os
import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from scipy.sparse import csr_matrix

def prediction(request):
    if request.method == 'POST':
        try:
            # Load trained model and encoders
            rf = joblib.load(os.path.join(settings.MEDIA_ROOT, 'Crime_RF.joblib'))
            label_encoder = joblib.load(os.path.join(settings.MEDIA_ROOT, 'label_encoder.joblib'))
            onehot_encoder = joblib.load(os.path.join(settings.MEDIA_ROOT, 'onehot_encoder.joblib'))
        except Exception as e:
            return render(request, 'users/prediction.html', {'error': f"Error loading model or encoders: {e}"})

        # Get user input
        input_data = {
            'Date of Occurrence': request.POST.get('Date of Occurrence'),
            'Time of Occurrence': request.POST.get('Time of Occurrence'),
            'City': request.POST.get('City'),
            'Crime Code': request.POST.get('Crime Code'),
            'Crime Description': request.POST.get('Crime Description'),
            'Victim Age': request.POST.get('Victim Age'),
            'Victim Gender': request.POST.get('Victim Gender'),
            'Police Deployed': request.POST.get('Police Deployed'),
            'Case Closed': request.POST.get('Case Closed'),
            'Weapon Used': request.POST.get('Weapon Used')
        }

        # Convert input to DataFrame
        input_df = pd.DataFrame([input_data])

        # 🔹 Get the original feature names used in training (before encoding)
        categorical_features = onehot_encoder.feature_names_in_.tolist()

        # 🔹 Ensure input_df has all the expected raw categorical features
        input_df = input_df.reindex(columns=categorical_features, fill_value='')

        # 🔹 Transform categorical input using the one-hot encoder
        input_encoded = onehot_encoder.transform(input_df)

        # 🔹 Convert to DataFrame with correct column names
        encoded_feature_names = onehot_encoder.get_feature_names_out().tolist()
        input_encoded_df = pd.DataFrame.sparse.from_spmatrix(input_encoded, columns=encoded_feature_names)

        # 🔹 Ensure feature order exactly matches training
        input_encoded_df = input_encoded_df.reindex(columns=encoded_feature_names, fill_value=0)

        # 🔹 Convert to sparse format for model input
        input_encoded_sparse = csr_matrix(input_encoded_df.values)

        # 🔹 Debugging: Print expected vs. actual feature names before prediction
        print("Expected Raw Features (from training):", categorical_features)
        print("One-Hot Encoded Features:", encoded_feature_names)
        print("Actual Features (from input data):", list(input_encoded_df.columns))

        # 🔹 Make prediction
        prediction = rf.predict(input_encoded_sparse)
        predicted_class = label_encoder.inverse_transform(prediction)

        return render(request, 'users/prediction.html', {
            'input_data': input_data,
            'predicted_class': predicted_class[0]
        })

    else:
        return render(request, 'users/prediction.html')
