from django.db import models

# Create your models here.


class Tweet(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField(max_length=300)

  def __str__(self):
      return f"{self.name}'s tweet says: {self.description}"



class Comment(models.Model):
      tweets = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
      author = models.CharField(max_length=50)
      comment = models.TextField(max_length=300)

      def __str__(self):
            return f"{self.author}'s comment"



