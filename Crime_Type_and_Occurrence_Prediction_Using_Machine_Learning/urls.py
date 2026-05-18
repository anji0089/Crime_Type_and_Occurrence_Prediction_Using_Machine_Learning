"""
URL configuration for Crime_Type_and_Occurrence_Prediction_Using_Machine_Learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Users import views as usr
from .import views as mainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainView.base,name='base'), 
    path("home/", mainView.home, name="home"),
    path("UserLogin/", mainView.userlogin, name="UserLogin"),
      
    # User Views
    path("UserRegisterActions/", usr.UserRegisterActions, name="UserRegisterActions"),
    path('userbase/',usr.userbase,name='userbase'),
    path("UserLoginCheck/", usr.UserLoginCheck, name="UserLoginCheck"),
    path("UserHome/", usr.UserHome, name="UserHome"),
    path("DatasetView/", usr.DatasetView, name="DatasetView"),
    path('training/',usr.training, name="training"),
    path("prediction/",usr.prediction,name="prediction"),
    

]
