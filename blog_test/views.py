from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import WarriorDef, Team
from django.contrib.auth.hashers import check_password, is_password_usable, make_password
from django.db.models import OuterRef, Subquery


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
    if not request.user.is_authenticated:
        return JsonResponse({'status':'err-no-user', 'text':"No user logged in"})
    d = {'status':'ok-user-data'}
    d['name'] = request.user.username
    warriors = list(WarriorDef.objects.filter(owner_user=request.user).values())
    d['warriors'] = warriors
    teams = []
    users_by_id = User.objects.filter(id=OuterRef('updated_by_user_id'))
    for team in request.user.team_set.all():
        members = [u.username for u in team.users.all()]
        warriors = list(WarriorDef.objects.filter(owner_team=team).annotate(updated_by_name=Subquery(users_by_id.values('username')[:1])).values())
        teams.append({"name":team.name, "members":members, "warriors":warriors})        
    d['teams'] = teams
    return JsonResponse(d)
        
    
    
def create_user(request):
    username = request.POST['name']
    if username.strip() == "":
        return JsonResponse({'status':'err-need-name', 'text':"User name can't be empty"})
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status':'name-exists'})
    password = request.POST['pass']
    if password == "":
        return JsonResponse({'status':'err-need-password', 'text':"Password can't be empty"})
    if password.strip() != password:
        return JsonResponse({'status':'err-bad-password', 'text':"Password starts or ends with white-space (bad idea)"})
        
    user = User.objects.create_user(username, '', password)
    user.save()
    return JsonResponse({'status':'ok-created'})
    
    
def user_login(request):
    username = request.POST['name']
    password = request.POST['pass']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status':'ok-logged-in'})
    else:
        return JsonResponse({'status':'err-failed', 'text':"User or password are wrong"})
        
def user_logout(request):
    logout(request)
    return JsonResponse({'status':'ok-logged-out'})
    

def add_warrior_def(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':'err-no-user', 'text':"No user logged-in"})
    title = request.POST['title']
    if title.strip() == "":
        return JsonResponse({'status':'err-no-title', 'text':"Warrior needs a name"})
    code1 = request.POST['code1']
    code2 = request.POST['code2']
    wtype = request.POST['wtype']
    if 'to_team' in request.POST:
        to_team = request.POST['to_team']
        if to_team.strip() == "":
            return JsonResponse({'status':"err-need-name", 'text':"Team name can't be empty"})
        t = request.user.team_set.filter(name=to_team)
        if not t.exists():
            return JsonResponse({'status':'err-no-such-team', "text":"You are not a member of this team"})
        s = WarriorDef(owner_team=t[0], title=title, code1=code1, code2=code2, wtype=wtype, update_date=timezone.now(), updated_by_user=request.user)    
    else:
        s = WarriorDef(owner_user=request.user, title=title, code1=code1, code2=code2, wtype=wtype, update_date=timezone.now())
    s.save()
    return JsonResponse({'status':'ok-added-code'})
    
    
def create_team(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':'err-no-user', 'text':"No user logged-in"})
    name = request.POST['name']
    if name.strip() == "":
        return JsonResponse({'status':"err-need-name", 'text':"Team name can't be empty"})
    if Team.objects.filter(name=name).exists():
        return JsonResponse({'status':'err-team-exists', 'text':"Team name already exists"})
    raw_password = request.POST['pass']
    print("~~~~ `%s`" % raw_password)
    if raw_password == "":
        return JsonResponse({'status':'err-need-password', 'text':"Team password can't be empty"})
    if raw_password.strip() != raw_password:
        return JsonResponse({'status':'err-bad-password', 'text':"Team password starts or ends with white-space (bad idea)"})
    t = Team(name=name)
    t.password = make_password(raw_password)
    t.save()
    t.users.add(request.user)
    return JsonResponse({'status':'ok-created-team'})
    
    
def join_team(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status':'err-no-user', 'text':"No user logged-in"})
    name = request.POST['name']
    if name.strip() == "":
        return JsonResponse({'status':"err-need-name", 'text':"Team name can't be empty"})    
    t = Team.objects.filter(name=name)
    if not t.exists():
        return JsonResponse({'status':'err-team-exists', 'text':"Team name does not exist"})
    t = t[0]
    raw_password = request.POST['pass']
    if not check_password(raw_password, t.password, None):
        return JsonResponse({'status':'err-team-wrong-pass', 'text':"Wrong password for team"})
    if t.users.filter(id=request.user.id).exists():
        return JsonResponse({'status':'err-already-joined', 'text':"User already in this team"})
    t.users.add(request.user)    
    return JsonResponse({'status':'ok-joined-team'})
    
    
        