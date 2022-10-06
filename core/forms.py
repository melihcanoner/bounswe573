from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Comment, User, Questions, Answers


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'username']



class QuestionForm(forms.ModelForm):
    # text = forms.TextInput()
    class Meta:
        model = Questions
        fields = ['text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answers
        fields = ['text']


class CommentForm(forms.Form):
    desc = forms.CharField(label="Your Comment")
    class Meta:
       model= Comment
       fields = ['text']