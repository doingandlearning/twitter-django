from rest_framework import serializers
from django.contrib.auth import get_user_model
import django.contrib.auth.password_validation as validations
# This turns a plain-text pw into a hash for db storage
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from .models import Tweet, Comment
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate(self, data):
        # Grab the pw from the data (i.e., the request)
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')
        # If the pw's don't make throw an err
        if password != password_confirmation:
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match'})
        # This checks the strength of the pw + throw an err if it's not strong enough
        # For testing purposes, comment this out to quicken tests
        # try:
        #     validations.validate_password(password=password)
        # except ValidationError as err:
        #     raise serializers.ValidationError({'password': err.messages})
        # Set the existing pw proeprty on our request to be the hashed pw (the make_password hashes it)  
        data['password'] = make_password(password)
        # Return that data
        return data

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation',)




class CommentSerializer(serializers.ModelSerializer):
    class Meta:
      model = Comment
      fields = '__all__'

      def create(self, validated_data):
          comment = Comment.objects.create(**validated_data)
          return comment

      def update(self, comment, validated_data):
          comment.author = validated_data.get("author", comment.author)
          comment.comment = validated_data.get("comment", comment.comment)
          comment.tweets = validated_data.get("tweets", comment.tweets)
          comment.save()
          return comment



class TweetSerializer(serializers.ModelSerializer):
  comments = CommentSerializer(many=True, required=False)
  class Meta:
    model = Tweet
    fields = '__all__'



