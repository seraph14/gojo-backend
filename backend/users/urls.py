from django.urls import path
from .views import UserRetrieveUpdateListView
urlpatterns = [
    path('', UserRetrieveUpdateListView.as_view(), name='user_view' ),
]