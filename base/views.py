from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .emails import send_otp_for_verification_email
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class MoviesApiViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movies.objects.all()
    
class PlatformApiViewSet(viewsets.ModelViewSet):
    serializer_class = PlatformSerializer
    queryset = Platform.objects.all()
    
class ReviewsApiViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Reviews.objects.all()
    
class ReviewsApiViewSetDetails(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        movie_id = self.kwargs['pk']
        return Reviews.objects.filter(movie_id=movie_id)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        phone = request.data.get('phone')
        if User.objects.filter(phone=phone).exists():
            return Response({'phone': ['Phone number already exists.']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate the password
            validate_password(password)
            # Save the user instance
            user = serializer.save()
            send_otp_for_verification_email(serializer.data['email'])
            return Response({'message': 'Registration Successful. Please Check your email for Email Validation OTP'}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            # If password validation fails, return the errors
            return Response({'password': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class VerifyOTP(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyAccountSerializer(data=data)
            
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                otp = serializer.validated_data.get('otp')
                
                user = User.objects.filter(email=email)
                if not user.exists():
                    return Response({
                        'status': 400,
                        'message': 'User not found',
                        'data': 'Invalid email address provided.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if user[0].otp != otp:
                    return Response({
                        'status': 400,
                        'message': 'Invalid OTP',
                        'data': 'The OTP you entered is incorrect.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = user.first()
                user.is_email_verified = True
                user.save()
                
                return Response({
                    'status': 200,
                    'message': 'Account Verified',
                    'data': {'Email Verified. Now you can login by the email and password.'}
                }, status=status.HTTP_200_OK)
            
            return Response({
                'status': 400,
                'message': 'Invalid data',
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except KeyError as ke:
            return Response({
                'status': 500,
                'message': 'Missing key in serializer data',
                'data': str(ke)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({
                'status': 500,
                'message': 'Internal server error',
                'data': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        
        if user:
            if not user.is_email_verified:
                return Response({'detail': 'Please verify your email to login.'}, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

class LogoutView(APIView):
    # For Logout in SimpleJWT, you should provide "access_token" in header with key => Authorization and value => Bearer <access_token>
    # then in Body and raw you should provide { "refresh" : "<refresh_token>"}
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # Extract the refresh token from the request data
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create a RefreshToken instance
            token = RefreshToken(refresh_token)
            
            # Blacklist the token to prevent it from being used again
            token.blacklist()
            
            # Return a successful response
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            # Handle potential errors
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)