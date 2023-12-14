from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Client(AbstractUser):
    avatar = models.ImageField(upload_to='static/images/avatars',blank=True)

class Post(models.Model):
    title = models.CharField(max_length=128,verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(Client,on_delete=models.CASCADE,related_name='posts')
    image = models.ImageField(upload_to='static/images/posts',null=True,blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=128)
    author = models.ForeignKey(Client,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    
    def __str__(self):
        return self.content