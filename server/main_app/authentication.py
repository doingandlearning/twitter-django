from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
# This returns the User model that's active in this project
# We're importing this bc Django has a default built-in user model
# If you want to grab django's user model it has a func set up for you
from django.contrib.auth import get_user_model
from django.conf import settings # for the secret key
import jwt
# Initialise a variable called User and set it to the get user model to so we can retrieve the user model 
User = get_user_model()

# This class will inherit from the BasicAuthentication class
class JWTAuthentication(BasicAuthentication):
  # This method will take the self and request object
    def authenticate(self, request):
      # We'll store the header of the request object inside this header variable
        header = request.headers.get('Authorization')
        # If the header doesn't exist, return None - user continues as unauthorised w/o ability to do authorised actions
        if not header:
            return None
        # If there's a header but it doesn't start w/ Bearer - permission is denied and err msg sent
        if not header.startswith('Bearer'):
            raise PermissionDenied({'message': 'Invalid authorization header'})
        # If the header is good, remove the Bearer part
        token = header.replace('Bearer ', '')
        try:
          # Get the payload by decoding the token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # We'll find the user whose primary key equals the payload's sub property and store in a var
            user = User.objects.get(pk=payload.get('sub'))
        # If the jwt is invalid or the user doesn't exist, throw an err
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied({'message': 'Invalid Token'})
        except User.DoesNotExist:
            raise PermissionDenied({'message': 'User not found'})
        # Return a tuple with the user and token elements
        return (user, token)

