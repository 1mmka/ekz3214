from typing import Any
from django.forms.models import BaseModelForm
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.views import LoginView
from main.forms import ClientLoginForm,RegisterClientForm,EditCreatePostForm
from main.models import Client,Post,Comment
from django.urls import reverse_lazy
from django.views.generic import CreateView,ListView,UpdateView,DetailView
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.template.loader import render_to_string

# login view
class ClientLoginView(LoginView):
    model = Client
    form_class = ClientLoginForm
    template_name = 'login_form.html'   

# register view
class RegisterClientView(CreateView):
    model = Client
    form_class = RegisterClientForm
    template_name = 'register_form.html'
    success_url = reverse_lazy('login-page')
    
    def form_valid(self, form):
        form_email = form.cleaned_data['email']
        
        if Client.objects.filter(email=form_email).exists():
            return HttpResponse('Пользователь с таким email-ом уже существует!')
        else:
            return super().form_valid(form)
    

# reset pass view
def ResetUserPasswordView(request):
    if request.method == 'POST':
        email = request.POST.get('email','ne nashel')
        
        if email != 'ne nashel':
            user = Client.objects.get(email = email)
            user_token = default_token_generator.make_token(user)
            create_verify_url = request.build_absolute_uri(f'/reset-pass/{user.pk}/{user_token}/')
            
            created_message = '''
            hi {0}
            your password reset url : \n\n{1}
            '''.format(user.username,create_verify_url)
            
            send_mail('reset user password',created_message,'andersonDJAGA@gmail.com',[str(user.email)])
            return HttpResponse('check your email')
    else:
        return render(request,'reset_pass.html')

# check token / set pass view
def checkResetDatas(request,user_pk,user_token):
    user = Client.objects.get(id=user_pk)
    
    if request.method == 'POST':
        if default_token_generator.check_token(user,user_token) == bool(1):
            sended_new_password = request.POST.get('password1')
            
            user.set_password(sended_new_password)
            user.save()
            
            return redirect('login-page')
        else:
            return HttpResponse('token checker said error')
    else:
        return render(request,'new_password.html')

# home view
class HomePageView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = '-created_at'
    
    def get_queryset(self):
        order = self.request.GET.get('order', self.ordering)
        return Post.objects.order_by(order)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        comments = Comment.objects.all()
        # paginator = Paginator(comments,5)
        # page_number = self.request.GET.get('page')
        # page = paginator.get_page(page_number)
        
        context['comments'] = comments
        
        return context

# create-comment view
def createComment(request,pk):
    content = request.POST.get('content')
    post = Post.objects.get(pk = pk)
    Comment.objects.create(content = content, author = request.user, post = post)
    
    return redirect('home-page')
    
# check profile view
class UserProfile(DetailView):
    model = Client
    pk_url_kwarg = 'pk'
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author = self.kwargs['pk'])
        context['posts'] = posts
        return context
    
# delete post view
def deletePost(request,pk):
    post = Post.objects.get(pk = pk)
    copy_post = post
    post.delete()
    return redirect('profile',copy_post.author.pk)

# edit-post view
class EditPostView(UpdateView):
    model = Post
    template_name = 'edit.html'
    form_class = EditCreatePostForm
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('profile')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post,pk = self.kwargs['pk'])
        context['post'] = post
        return context
    
    def get_success_url(self):
        user = Post.objects.get(pk = self.kwargs['pk']).author.pk
        success_url = reverse_lazy('profile', kwargs={'pk': user})
        return success_url
    
# create-post view
class CreatePostView(CreateView):
    template_name = 'create.html'
    form_class = EditCreatePostForm
    success_url = reverse_lazy('profile')
    
    def get_success_url(self):
        success_url = reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
        return success_url
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if form.is_valid():
            form.instance.author = self.request.user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)