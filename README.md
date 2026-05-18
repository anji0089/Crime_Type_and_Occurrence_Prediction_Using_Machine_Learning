# Crime Type and Occurrence Prediction Using Machine Learning

## Overview

Crime Type and Occurrence Prediction Using Machine Learning is a web-based application developed to predict crime-related outcomes using machine learning techniques. The project uses a trained machine learning model and provides a simple Django web interface for users to enter input details and view prediction results.

This project helps in understanding how machine learning can be applied to crime data analysis and prediction.

## Features

- Predicts crime type and occurrence based on user input
- Uses a trained machine learning model saved in `.joblib` format
- Provides a Django-based web interface
- Uses SQLite database for local data storage
- Includes frontend pages using HTML, CSS, and templates
- Demonstrates integration of machine learning with a web application

## Technologies Used

- Python
- Django
- Machine Learning
- Scikit-learn
- Pandas
- NumPy
- SQLite
- HTML
- CSS
- Joblib

## Project Structure

```text
Crime_Type_and_Occurrence_Prediction_Using_Machine_Learning/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
├── Crime_RF.joblib
├── label_encoder.joblib
├── onehot_encoder.joblib
│
├── templates/
├── static/
├── media/
├── Users/
│
└── README.md
