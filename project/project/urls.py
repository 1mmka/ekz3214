from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main.views import ClientLoginView,HomePageView,RegisterClientView,ResetUserPasswordView,checkResetDatas,createComment,EditPostView,UserProfile,deletePost,CreatePostView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # login,register,forgot pass,logout 
    path('',ClientLoginView.as_view(),name='login-page'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('register',RegisterClientView.as_view(),name='register-page'),
    path('reset',ResetUserPasswordView,name='reset-password'),
    path('reset-pass/<int:user_pk>/<str:user_token>/',checkResetDatas,name='check-datas'),
    
    # home,create-comment,edit-post,user-profile,delete-post
    path('home',HomePageView.as_view(),name='home-page'),
    path('create/<int:pk>',createComment,name='create-comment'),
    path('edit/<int:pk>',EditPostView.as_view(),name='edit-post'),
    path('profile/<int:pk>',UserProfile.as_view(),name='profile'),
    path('delete/<int:pk>',deletePost,name='delete-post'),
    path('create-post',CreatePostView.as_view(),name='create-post'),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
