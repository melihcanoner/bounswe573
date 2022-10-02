from django.contrib import admin
from django.urls import path
from .views import LoginView, RegisterView, DashboardView, LogoutView, QuestionView, AnswerView, view_post

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard-view'),
    path('login/', LoginView.as_view(), name='login-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('question/', QuestionView.as_view(), name='question-view'),
    path('answer/<int:pk>', view_post, name='answer-create'),

]