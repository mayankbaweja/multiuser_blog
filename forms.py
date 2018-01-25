from django import forms
from myapp.models import User, PostModel, Like, Comment

class SignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","full_name","email","password"]


class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields= ["username", "password"]


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['image', 'caption', 'text']


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['post']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', 'post']