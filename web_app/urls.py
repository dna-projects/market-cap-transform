from django.urls import path
from web_app.views import InitialPageView, TransformPageView

urlpatterns = [
    path('', InitialPageView.as_view(), name='initial'),
    path('transform', TransformPageView.as_view(), name='transform')
]