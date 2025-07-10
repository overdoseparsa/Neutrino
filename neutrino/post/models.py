from neutrino.common.models import BaseModel
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Post(BaseModel):
    title = models.CharField(max_length=150 ,)
    content = models.TextField(max_length = 100, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE , related_name="posts")
    



    def __str__(self):
        return self.title

class Conection(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="Connection")
    followers = models.ManyToManyField(
        User , related_name="Followers"
    )
    followers = models.ManyToManyField(
        User , related_name="Following"
    )
    

class Comment(BaseModel):
    post = models.ForeignKey(Post, related_name="comments" , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="Comments")
    body = models.TextField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ForeignKey(User, on_delete=models.CASCADE , related_name="blogcomment", blank=True  , null=True) 
    reply = models.ForeignKey('self', null=True, related_name="replies", on_delete=models.CASCADE , blank=True)
    
    def total_clikes(self):
        return self.likes.count()

    # def __str__(self):
    #     return '%s - %s - %s' %(self.post.title, self.name, self.id)
