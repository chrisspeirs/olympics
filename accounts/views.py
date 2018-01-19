from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from players.models import Players, Olympics, Game, Tourney, Score

# Create your views here.

def signup(request):

    print('got here')
    if request.method == 'POST':
        print('passed first if')
        form= SignUpForm(request.POST)
        if form.is_valid():
            print('passed 2nd if')
            user= form.save()
            auth_login(request, user)
            player=Players.objects.create(user=user, name= user.username)
            player.save()
            return redirect('home')
    else:
        print('passed else')
        form = SignUpForm()
 
    print('left else')
    
    return render(request, 'signup.html', {'form': form })
