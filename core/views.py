from django.shortcuts import HttpResponseRedirect, redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.views.generic.edit import FormView, CreateView,  UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from .models import Questions, Answers, User, Learningspace, Comment
from django.contrib.auth.forms import AuthenticationForm
from .forms import  RegisterForm, QuestionForm, AnswerForm, CommentForm



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
            return redirect(reverse('learningspace-list'))
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
            return redirect(reverse('learningspace-list'))
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
            return redirect(reverse('learningspace-list'))
        except Exception as e:
            content = {}
            content['form'] = AuthenticationForm
            content['error'] = 'Unable to login with provided credentials' 
            return render(request, 'login.html', content)


class LogoutView(FormView):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')



@method_decorator(login_required, name='dispatch')
class LearningspaceListView(ListView):
    model = Learningspace
    context_object_name = "objLearningspaces"
    queryset = Learningspace.objects.order_by('-created_on')

    def get_context_data(self, **kwargs):
        context = super(LearningspaceListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

@method_decorator(login_required, name='dispatch')
class LearningspaceCreate(CreateView):
    model = Learningspace
    fields = ['title','desc']
    success_url = '/core/learningspace/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class LearningspaceUserListView(ListView):
    template_name = 'core/learningspace_by_user.html'
    def get_queryset(self):
        self.user = get_object_or_404(User, username = self.kwargs['username'])
        return Learningspace.objects.filter(user = self.user)

@method_decorator(login_required, name='dispatch')
class LearningspaceDetailView(DetailView):
    model = Learningspace
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_comment'] = CommentForm()
        return context

class LearningspaceUpdateView(UpdateView):
    model = Learningspace
    fields = ['title','desc']
    template_name = 'core/learningspace_update_form.html'

class LearningspaceDeleteView( DeleteView):
    model = Learningspace
    success_url = '/core'

class CommentCreateView(CreateView):
    model = Comment
    fields = ['desc']
    success_url = '/core/learningspace/'

    def form_valid(self, form):
        _learningspace = get_object_or_404(Learningspace, id=self.kwargs['pk'])
        form.instance.user = self.request.user
        form.instance.slug = _learningspace
        return super().form_valid(form)

class CommentUpdateView( UpdateView):
    model = Comment
    fields = ['desc']
    template_name = 'core/learningspace_update_comment.html'

    success_url = '/core/learningspace/'