from django.urls import path
from .views import project

urlpatterns = [
    path('receipts/', project.as_view()),
]