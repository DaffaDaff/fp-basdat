from django.shortcuts import render, redirect
from django.contrib.auth import logout as log_out

from .forms import SignupForm

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    else:
        return redirect('/dashboard/')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {
        'form': form
    })

def logout(request):
    log_out(request)

    return redirect('/login/')