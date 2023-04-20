from django.urls import path
from .views import UserRetreiveUpdateListView
urlpatterns = [
    path('', UserRetreiveUpdateListView.as_view(), name='user_view' ),
]