from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, Group, Membership, Photo
from .serializers import UserSerializer, GroupSerializer, PhotoSerializer, MembershipSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage

# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User created successfully. Now you can login."
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Login View
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# Group Creation View
class GroupCreateView(generics.CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(admin=self.request.user)

# Join Group View
class JoinGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        group_id = request.data.get("group_id")
        try:
            group = Group.objects.get(id=group_id)
            Membership.objects.create(user=request.user, group=group)
            return Response({"message": f"Joined group {group.name} successfully"})
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"error": "Already a member of this group"}, status=status.HTTP_400_BAD_REQUEST)

# Photo Upload View
class PhotoUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        group_id = request.data.get("group_id")
        caption = request.data.get("caption")
        photo = request.data.get("photo")

        try:
            group = Group.objects.get(id=group_id)
            if not Membership.objects.filter(user=request.user, group=group).exists():
                return Response({"error": "You are not a member of this group"}, status=status.HTTP_403_FORBIDDEN)
            
            # Save photo to S3
            file_name = default_storage.save(photo.name, photo)
            file_url = default_storage.url(file_name)
            
            # Create Photo object
            Photo.objects.create(user=request.user, group=group, image_url=file_url, caption=caption)
            return Response({"message": "Photo uploaded successfully"})
        
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

# View Photos in Group
class GroupPhotosView(generics.ListAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group = Group.objects.get(id=group_id)
        if Membership.objects.filter(user=self.request.user, group=group).exists():
            return Photo.objects.filter(group=group)
        else:
            return Photo.objects.none()
