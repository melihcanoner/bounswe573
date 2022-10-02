from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from .models import Questions, Answers, User
from django.contrib.auth.forms import AuthenticationForm
from .forms import  RegisterForm, QuestionForm, AnswerForm


class DashboardView(FormView):

    def get(self, request):
        content = {}
        if request.user.is_authenticated:
            user = request.user
            user.backend = 'django.contrib.core.backends.ModelBackend'
            ques_obj = Questions.objects.all()
            content['userdetail'] = user
            content['questions'] = ques_obj
            return render(request, 'dashboard.html', content)
        else:
            return redirect(reverse('login-view'))


class RegisterView(FormView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        content['form'] = RegisterForm
        return render(request, 'register.html', content)

    def post(self, request):
        content = {}
        form = RegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.password = make_password(form.cleaned_data['password'])
            save_it.save()
            login(request, save_it)
            return redirect(reverse('dashboard-view'))
        content['form'] = form
        template = 'register.html'
        return render(request, template, content)


class LoginView(FormView):

    content = {}
    content['form'] = AuthenticationForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        if request.user.is_authenticated:
            return redirect(reverse('dashboard-view'))
        content['form'] = AuthenticationForm
        return render(request, 'login.html', content)

    def post(self, request):
        content = {}
        username = request.POST['username']
        password = request.POST['password']
        try:
            users = User.objects.filter(username=username)
            user = authenticate(request, username=users.first().username, password=password)
            login(request, user)
            return redirect(reverse('dashboard-view'))
        except Exception as e:
            content = {}
            content['form'] = AuthenticationForm
            content['error'] = 'Unable to login with provided credentials' 
            return render(request, 'login.html', content)


class LogoutView(FormView):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')


class QuestionView(FormView):
    content = {}
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        if not request.user.is_authenticated:
            content['form'] = AuthenticationForm
            return render(request, 'login.html', content)
        content['form'] = QuestionForm
        return render(request, 'question.html', content)

    def post(self, request):
        text = request.POST['text']
        Questions.objects.create(text=text, user=request.user)
        return redirect(reverse('dashboard-view'))

class AnswerView(FormView):
    content = {}
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(QuestionView, self).dispatch(request, *args, **kwargs)


    def post(self, request):
        content = {}
        if not request.user.is_authenticated:
            content['form'] = AuthenticationForm
            return render(request, 'login.html', content)
        text = request.POST['text']
        Answers.objects.create(text=text, user=request.user)
        return redirect(reverse('dashboard-view'))


def view_post(request, pk):
    question = get_object_or_404(Questions, pk=pk)
    form = AnswerForm(request.POST or None)

    if form.is_valid():
        text = request.POST['text']
        Answers.objects.create(text=text, user=request.user, question=question)
        return redirect(reverse('dashboard-view'))
    return render(request, 'blog_post.html',{'question': question,'form': form})