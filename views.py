# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from myapp.forms import SignUpForm, LoginForm, PostForm, LikeForm, CommentForm
from myapp.models import User, SessionToken, PostModel, Like, Comment
from django.contrib import messages
from mublog.settings import BASE_DIR
from django.contrib.auth.hashers import make_password, check_password
from imgurpython import ImgurClient
from django.template import RequestContext

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form= SignUpForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data["susername"]
            password = form.cleaned_data["spassword"]
            full_name = form.cleaned_data["full_name"]
            email = form.cleaned_data["email"]
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken, Choose any other username')
                return redirect('index.html')
            else:
                user=User(full_name=full_name,password=make_password(password),email=email,username=username)
                user.save()
                messages.info(request,'Signup Successfull!!!')
                return render(request, 'index.html', {'form': form})
    else:
        form=SignUpForm
    return render(request,"index.html",{"form":form})



def login_view(request):
    response_data = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()

            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response

                else:
                    response_data['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    response_data['form'] = form
    return render(request, 'login.html', response_data)



def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        for post in posts:
            existing_like = Like.objects.filter(post_id=post, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'post': posts})
    else:
        return redirect('/')



def post_view(request):
    user = check_validation(request)

    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                text = form.cleaned_data.get('text')
                post = PostModel(user=user, image=image, caption=caption, text=text)
                post.save()

                path = str(BASE_DIR + '/' + post.image.url)

                client = ImgurClient('37e25d0cbc857c0', 'f7a8c883baef922700e185d6b987a607c7a56840')
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()
                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'feed.html', {'form': form})
    else:
        return redirect('/')

def like_view(request):

    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = Like.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                Like.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            Like.objects.filter(user=user, post_id=post_id).exists()
            posts = PostModel.objects.all().order_by('created_on')
            return redirect('/feed/')

    else:
        return redirect('/login/')

def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = Comment.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            comment.save()
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')

def logout_view(request):
    user = check_validation(request)
    if user:
        token=SessionToken.objects.get(session_token=request.COOKIES.get("session_token"))
        token.is_valid=False
        token.save()
    return redirect('127.0.0.1:8000')







def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
           return session.user
    else:
        return None

