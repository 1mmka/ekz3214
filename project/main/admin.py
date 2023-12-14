from django.contrib import admin
from main.models import Client,Post,Comment

# Register your models here.
admin.site.register(Client)
admin.site.register(Post)
admin.site.register(Comment)