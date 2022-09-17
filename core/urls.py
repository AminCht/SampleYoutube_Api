from django.urls import path
from . import views

urlpatterns = [
    path('notif/', views.notify),
    path('code/', views.ActivationCodeApi.as_view()),
    path('red/', views.RedeemCode.as_view())
]