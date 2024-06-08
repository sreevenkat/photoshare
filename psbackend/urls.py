from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserLoginView, GroupCreateView, JoinGroupView, PhotoUploadView, GroupPhotosView

# Create a router and register our viewsets with it
router = DefaultRouter()

# Registering the viewsets
router.register(r'register', UserRegistrationView, basename='register')
router.register(r'groups', GroupCreateView, basename='group')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', UserLoginView.as_view(), name='login'),
    path('api/join-group/', JoinGroupView.as_view(), name='join-group'),
    path('api/upload-photo/', PhotoUploadView.as_view(), name='upload-photo'),
    path('api/group-photos/<int:group_id>/', GroupPhotosView.as_view(), name='group-photos'),
]
