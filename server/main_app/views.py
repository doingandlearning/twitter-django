from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import TweetSerializer, CommentSerializer, UserSerializer
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt
from .models import Tweet, Comment
User = get_user_model()

# Create your views here.

# This class will inherit from the APIView
class RegisterView(APIView):

    def post(self, request):
      #  As the data object we'll pass in the request.data
        serializer = UserSerializer(data=request.data)
        # If the serializer is valid, save it and return a msg
        if serializer.is_valid():
              user = serializer.save()
              token = jwt.encode(
                {'sub': user.id}, settings.SECRET_KEY, algorithm='HS256')
              return Response({'message': 'Registration successful', 'token': token})
        # If it's unsuccessful, return the err from the serializer
        return Response(serializer.errors, status=422)


# This class will inherit from the APIView
class LoginView(APIView):

    def get_user(self, email):
        try:
          # Retrieve the user from our db, search by email property
            return User.objects.get(email=email)
          # If the user doens't exist, throw an err
        except User.DoesNotExist:
            raise PermissionDenied({'message': 'Invalid credentials'})

    def post(self, request):
        # Extract the email and pw from the form
        email = request.data.get('email')
        password = request.data.get('password')
        # Find the user by using the helper func we defined above
        user = self.get_user(email)
        # If the pw and pw confirmation don't match, raise an err
        if not user.check_password(password):
            raise PermissionDenied({'message': 'Invalid credentials'})
        # If it's ok, create the token
        token = jwt.encode({'sub': user.id}, settings.SECRET_KEY, algorithm='HS256')
        print('user in views:', user)
        # Once we have the token, respond with it + include a msg
        return Response({'token': token, 'message': f'Welcome back {user.username}!'})






class TweetListCreateGen(generics.ListCreateAPIView):
      queryset = Tweet.objects.all()
      serializer_class = TweetSerializer

      # Kevin notes these method and the one below aren't necessary - insomnia test confirms this
      # def get(self, request, *args, **kwargs):
      #     return self.list(request, *args, **kwargs)


      # def post(self, request, *args, **kwargs):
      #     return self.create(request, *args, **kwargs)


class TweetRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
      queryset = Tweet.objects.all()
      serializer_class = TweetSerializer

      # def get(self, request, *args, **kwargs):
      #     return self.retrieve(request, *args, **kwargs)


      # def put(self, request, *args, **kwargs):
      #     return self.update(request, *args, **kwargs)


      # def delete(self, request, *args, **kwargs):
      #     return self.destroy(request, *args, **kwargs)


class CreateListView(generics.ListCreateAPIView):
      queryset = Comment.objects.all()
      serializer_class = CommentSerializer



class RUDView(generics.RetrieveUpdateDestroyAPIView):
      queryset = Comment.objects.all()
      serializer_class = CommentSerializer







# ---------------------------------------------- #

# Class/APIView version:
# class TweetListCreate(APIView):

#   def get(self, request):
#       tweets = Tweet.objects.all()
#       serializer = TweetSerializer(tweets, many=True)
#       return Response(serializer.data)
  
#   def post(self, request, *args, **kwargs):
#       new_tweet = Tweet.objects.create(
#         name=request.data['name'],
#         description=request.data['description']
#       )
#       new_tweet.save()
#       serializer = TweetSerializer(new_tweet)
#       return Response(serializer.data)


# class TweetDetailUpdateDelete(APIView):

#     def get(self, request, pk):
#         tweet = Tweet.objects.get(id=pk)
#         serializer = TweetSerializer(tweet)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         tweet = Tweet.objects.get(id=pk)
#         serializer = TweetSerializer(tweet, request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         tweet = Tweet.objects.get(id=pk)
#         tweet.delete()
#       # If you want to refetch the data/redirect - this shows all tweets
#         tweets = Tweet.objects.all()
#         serializer = TweetSerializer(tweets, many=True)
#         return Response(serializer.data)

# ---------------------------------------------- #

# @api_view version:
# @api_view(['GET'])
# def tweets_list(request):
#     tweets = Tweet.objects.all()
#     serializer = TweetSerializer(tweets, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def tweet_create(request):
#     serializer = TweetSerializer(data=request.data)

#     if serializer.is_valid():
#       serializer.save()
#     return Response(serializer.data)


# @api_view(['GET'])
# def tweet_detail(request, pk):
#     tweet = Tweet.objects.get(id=pk)
#     serializer = TweetSerializer(tweet)
#     return Response(serializer.data)


# @api_view(['PUT'])
# def tweet_update(request, pk):
#     tweet = Tweet.objects.get(id=pk)
#     serializer = TweetSerializer(tweet, request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def tweet_delete(request, pk):
#     tweet = Tweet.objects.get(id=pk)
#     tweet.delete()
#     # If you want to refetch the data/redirect - this shows all tweets
#     tweets = Tweet.objects.all()
#     serializer = TweetSerializer(tweets, many=True)
#     return Response(serializer.data)


def home(request):
  data = {
    'app': 'Django'
  }

  return JsonResponse(data)


