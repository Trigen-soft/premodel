from django.contrib import admin
from django.urls import path
from .views import signupview, loginview, logoutview, listview, graphview, creatclass, stock

urlpatterns = [
    path('create/', creatclass.as_view(), name="create"),
    path('signup/', signupview, name="signup"),
    path('login/', loginview, name="login"),
    path('logout/', logoutview.as_view(), name="logout"),
    path('list/', listview, name="list"),
    path('graph/', graphview, name="graph"),
    path('stock/', stock, name='stock'),
]
