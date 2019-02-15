from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog_test/post_list.html', {'posts': posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog_test/post_detail.html', {'post': post})
    
    
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog_test/post_edit.html', {'form': form})
    
#-----

def get_user_data(request):
    #print("~~~", request.user.username, request.user.is_anonymous, request.user.is_authenticated )
    if request.user.is_authenticated:
        d = {'status':'ok'}
        d['name'] = request.user.username
        return JsonResponse(d)
    else:
        return JsonResponse({'status':'no-user'})
    
    
def create_user(request):
    username = request.POST['name']
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status':'name-exists'})
    password = request.POST['pass']
    user = User.objects.create_user(username, '', password)
    user.save()
    return JsonResponse({'status':'created'})
    
    
def user_login(request):
    username = request.POST['name']
    password = request.POST['pass']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status':'logged-in'})
    else:
        return JsonResponse({'status':'failed'})
        
def user_logout(request):
    logout(request)
    return JsonResponse({'status':'logged-out'})
        