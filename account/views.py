from django.shortcuts import render, redirect
from account.models import Account
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from blog.models import BlogPost


# Create your views here.
def display_account_users(request):
    context = {}
    accounts = Account.objects.all()
    context['accounts'] = accounts
    return render(request, 'account/show_account_users.html', context)


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('form is valid, should redirect')
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            print('form is invalid')
            context['registration_form'] = form
    else:
        print('form loaded from get request')
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                'email': request.POST['email'],
                'username': request.POST['username']
            }
            form.save()
            context['message'] = 'Updated'
        context['update_account_form'] = form

    else:
        form = AccountUpdateForm(
            initial={
                'email': request.user.email,
                'username': request.user.username
            }
        )
        context['update_account_form'] = form

        blog_post = BlogPost.objects.filter(author = request.user)
        context['blog_posts'] = blog_post

    return render(request, 'account/account.html', context)
