"""My new documentation"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('findcar', views.findcar, name="findcar"),
    path('bookings', views.bookings, name="bookings"),
    path('cancellings', views.cancellings, name="cancellings"),
    path('seebookings', views.seebookings, name="seebookings"),
    path('deleterecord', views.deleterecord, name="deleterecord"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('success', views.success, name="success"),
    path('signout', views.signout, name="signout"),
]
