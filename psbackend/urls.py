from django.urls import path
from .views import (
    UserRegistrationView, 
    UserLoginView, 
    GroupCreateView, 
    JoinGroupView, 
    PhotoUploadView, 
    GroupPhotosView
)

urlpatterns = [
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/groups/', GroupCreateView.as_view(), name='group-create'),
    path('api/join-group/', JoinGroupView.as_view(), name='join-group'),
    path('api/upload-photo/', PhotoUploadView.as_view(), name='upload-photo'),
    path('api/group-photos/<int:group_id>/', GroupPhotosView.as_view(), name='group-photos'),
]
