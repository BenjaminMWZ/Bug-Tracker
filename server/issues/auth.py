from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
import logging

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Converts User instances to JSON, exposing only safe, non-sensitive fields
    for API responses.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles validation and creation of new user accounts, including password
    confirmation to prevent typos during registration.
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        """
        Validate that the two password fields match.
        
        Args:
            data: Dictionary containing the registration form data
            
        Returns:
            Dictionary of validated data
            
        Raises:
            ValidationError: If passwords don't match
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.
        
        Removes the confirmation password field and uses Django's create_user
        method to properly hash the password.
        
        Args:
            validated_data: Dictionary containing validated registration data
            
        Returns:
            Newly created User instance
        """
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

import logging
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger('bug_tracker')

class LoginView(APIView):
    """
    API view for user authentication.
    
    Handles login requests by validating credentials and returning
    an authentication token for valid users.
    """
    def post(self, request):
        """
        Process a login request.
        
        Args:
            request: HTTP request object containing username and password
            
        Returns:
            Response: Authentication token and user details on success,
                     error message on failure
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            logger.info(f"Login attempt for user '{username}'")
            
            user = authenticate(username=username, password=password)
            
            if user:
                token, created = Token.objects.get_or_create(user=user)
                logger.info(f"Login successful for user '{username}'")
                return Response({
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
            
            logger.warning(f"Login failed for user '{username}' - invalid credentials")
            return Response(
                {'error': 'Invalid Credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.error(f"Login error for user '{username}': {str(e)}")
            return Response(
                {'error': 'An error occurred during login'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class RegistrationView(APIView):
    """
    API view for user registration.
    
    Handles the creation of new user accounts and generates
    an authentication token for immediate login after registration.
    """
    permission_classes = [permissions.AllowAny]  # Allow unauthenticated access

    def post(self, request):
        """
        Process a registration request.
        
        Args:
            request: HTTP request object containing registration data
            
        Returns:
            Response: Authentication token and user details on success,
                     validation errors on failure
        """
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    API view for retrieving the current user's profile.
    
    Requires authentication and returns the details of the
    currently authenticated user.
    """
    permission_classes = [IsAuthenticated]  # Require valid authentication
    
    def get(self, request):
        """
        Retrieve the authenticated user's profile.
        
        Args:
            request: HTTP request object with authentication credentials
            
        Returns:
            Response: User profile data
        """
        # Add some logging
        print(f"Auth headers: {request.headers.get('Authorization')}")
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"User: {request.user}")
        
        serializer = UserSerializer(request.user)
        return Response(serializer.data)