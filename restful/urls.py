from django.urls import path
from .views import getModuleDetail, Register, Login, Logout,rating, getView, getAverage

# Some urls for user to access
urlpatterns = [
    path('getlist/', getModuleDetail, name='getlist'),
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('logout/',Logout, name='logout'),
    path('rate/',rating,name='rating'),
    path('view/',getView, name='view'),
    path('average/', getAverage, name='average')
]
