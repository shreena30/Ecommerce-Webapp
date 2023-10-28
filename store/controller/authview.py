from multiprocessing import context
from pydoc import render_doc
from pyexpat.errors import messages
from unicodedata import category, name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from store.forms import CustomUserForm
# Create your views here.


def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Registered successfully! Login to Continue')
            return redirect('/login')
    context = {'form': form}
    return render(request, "store/auth/register.html", context)


def loginpage(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(request, username=name, password=passwd)

            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/login')
        return render(request, "store/auth/login.html")


def logoutpage(request):
   # print(request.user.is_authenticated)
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("/")
