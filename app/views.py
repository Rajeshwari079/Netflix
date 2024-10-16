from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.models import *
from django.shortcuts import get_object_or_404
import re
from django.http import JsonResponse

# Create your views here.

# SIGNUP
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return redirect('/signup')
            
            elif User.objects.filter(username = username).exists():
                messages.info(request,'Username already exists')
                return redirect('/signup')
            
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('/')
        else:
            messages.info(request,'Passwords do not Match')
            return redirect('/signup')
    
    return render(request,'signup.html')


# LOGIN
def userlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request,user)
            return redirect('index/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/')
    return render(request,'userlogin.html')

# index
@login_required(login_url='/')
def index(request):
    gen = Genre.objects.all()
    movies = Movie.objects.all()
    d = {'movies':movies,'genre':gen}
    return render(request,'index.html',d)

@login_required(login_url='/')
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/')
def genre(request,pk):
    movie_genre = pk
    gen = Genre.objects.all()
    movies = Movie.objects.filter(genre=movie_genre)
    d = {'movies':movies,'gen':gen,'movie_genre':movie_genre}
    return render(request,'genre.html', d)

@login_required(login_url='/')
def movie(request,pk):
    movie_uuid=pk
    gen = Genre.objects.all()
    movie_details = Movie.objects.get(uu_id=movie_uuid)
    d={'movie_details':movie_details,'gen':gen}
    return render(request,'movie.html',d)

@login_required(login_url='/')
def search(request):
    gen = Genre.objects.all()
    if request.method == 'POST':
        search_term = request.POST['search_term']
        movies = Movie.objects.filter(title__icontains=search_term)
        d = {'movies':movies,'search_term':search_term,'genre':genre}
        return render(request,'search.html',d)
    return redirect('app/index',{'genre':gen})



def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern,movie_url_id)
        movie_id = match.group() if match else None
        movie =get_object_or_404(Movie,uu_id=movie_id)
        movie_list, created = Movielist.objects.get_or_create(owner_user = request.user, movie=movie)
        movie_list.save()
        if created:
            response_data = {'status':'success','message':'Added'}
        else:
            response_data = {'status':'success','message':'Movie Already in list'}
        return JsonResponse(response_data)
    return JsonResponse({'status':'error','message':'Invalid request'},status=400)


@login_required(login_url='/')
def my_list(request):
    gen = Genre.objects.all()
    MO = Movielist.objects.filter(owner_user = request.user)
    AMO = []
    for i in MO:
        AMO.append(i.movie)
    d={'movies':AMO,'genre':gen}
    return render(request,'my_list.html',d)
