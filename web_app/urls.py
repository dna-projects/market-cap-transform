from django.urls import path
from web_app.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]