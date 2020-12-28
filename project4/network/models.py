from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    # def __str__(self):
    #     return(f"{self.pk} user {self.username}" )
    
    def serialize(self):
        return{
            "id": self.pk,
            "username": self.username,
            "email": self.email
        }

class Actions(models.Model):
    postID = models.ForeignKey("Post", on_delete = models.CASCADE)
    actionUserID = models.ForeignKey("User", on_delete = models.CASCADE, related_name="action_user")
    liked = models.BooleanField(default=False)
    
    def __str__(self):
        return(f"post {self.postID} liked by {self.actionUserID} and {self.liked} ")
    
    def serialize(self):
        return{
            "id": self.pk,
            "postID": self.postID,
            "actionUserID": self.actionUserID,
            "liked": self.liked
        }
    

class Post(models.Model):
    user = models.ForeignKey("User", on_delete = models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(f"{self.user} posted: {self.body}, likes:{Actions.objects.filter(postID=self.pk, liked=True).count()} pk{self.pk}")
    

    def serialize(self, request):
        if request.user.is_anonymous:
            return{
            "id": self.pk,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": Actions.objects.filter(postID=self.pk, liked=True).count(),
            # "liked": likedSet

        }
        if(request != False):
            likedSet = Actions.objects.filter(postID=self.id, actionUserID=request.user).first()
        else:
            likedSet = False

        print(likedSet)
        if likedSet is None:
            likedSet = False
        elif likedSet == False:
            print('skip others')
            
        elif likedSet.liked:
            likedSet = True
        else:
            likedSet = False

        # print(f'{request.user.username == self.user.username}')
    
        return{
            "id": self.pk,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "likes": Actions.objects.filter(postID=self.pk, liked=True).count(),
            "liked": likedSet,
            "canEdit": request.user.username == self.user.username

        }

class Follower(models.Model):
    followedUser = models.ForeignKey("User", on_delete = models.CASCADE, related_name="followed_user")
    follower = models.ForeignKey("User", on_delete = models.CASCADE, related_name="follower")

    def __str__(self):
        return f"{self.followedUser} is followed by {self.follower}"
    
    def serialize(self):
        return{
            "followedUser": self.followedUser,
            "follower": self.follower
        }
    