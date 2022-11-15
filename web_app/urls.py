from django.urls import path
from web_app.views import BaseView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
]