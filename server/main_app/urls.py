from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home),
  # Paths below are for Token Authentication
  path('signup/', views.RegisterView.as_view()),
  path('login/', views.LoginView.as_view()),

  # Tbhe paths below use generics
  path('tweets-list-create-generics/', views.TweetListCreateGen.as_view()),
  path('tweets-retrieve-update-delete/<int:pk>/', views.TweetRetrieveUpdateDestroy.as_view()),
  path('tweets-comments', views.CreateListView.as_view()),
  path('tweets-read-update-delete/<int:pk>/', views.RUDView.as_view())

  # Class-based APIView
  # path('tweets-list-create-api/', views.TweetListCreate.as_view()),
  # path('tweets-detail-update-delete-api/<int:pk>/', views.TweetDetailUpdateDelete.as_view())

  # @api_view paths
  # path('tweets-list/', views.tweets_list),
  # path('tweets-create/', views.tweet_create),
  # path('tweets-detail/<int:pk>/', views.tweet_detail),
  # path('tweets-update/<int:pk>/', views.tweet_update),
  # path('tweets-delete/<int:pk>/', views.tweet_delete)
]

