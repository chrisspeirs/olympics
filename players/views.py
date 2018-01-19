from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Players, Olympics, Game, Tourney, Score, Result, Points
from django.contrib.auth.models import User
from .forms import  recordscoreForm
from django.contrib.auth.decorators import login_required


def home(request):
    olympics = Olympics.objects.all()
    return render(request, 'home.html', {'olympics' : olympics})



def olympics(request, pk):
    
    olympics = get_object_or_404(Olympics, pk=pk)
    event= get_list_or_404(Tourney, olympics__name=olympics.name)
    context = {'event': event, 'olympics': olympics }
    return render(request, 'events.html', context)

@login_required
def results(request, pk):


    olympics = get_object_or_404(Olympics, pk=pk)
    players=get_list_or_404(Players, active=True)

    


    for i in range(len(players)-1):

        
        point= Points.objects.filter(player = players[i], olympics=olympics)
        print('test')
        player= point[0]
        player.result= players[i].getTotal(olympics)
        player.save()
  

    points= get_list_or_404(Points.objects.order_by('result'), olympics=olympics)
        
    context = {'olympics': olympics, 'players': players, 'points': points}
    return render(request, 'results.html', context)

@login_required
def eventresult(request, pk, tourney_pk):

    user=request.user
    event= get_object_or_404(Tourney, olympics__pk=pk, pk=tourney_pk)
    olympics=get_object_or_404(Olympics, pk=pk)
    

    
    if olympics.isRunning:
         players=get_list_or_404(Players, active=True)
    else:
        players=get_list_or_404(Players, active=False)

    if event.isRanked:
        print('check')

        scores= list(Score.objects.filter(tourney=event))
        if not scores:
            for i in range(len(players)):
                score= Score.objects.create(player=players[i], tourney=event, score=0)

        context = {'event': event, 'players': players, 'olympics': olympics, 'scores': scores}
        return render(request, 'eventresults.html', context)

    else:

            
        if event.currentRound == 0:
                for i in range(len(players)):
                    players[i].eliminated=False
                    players[i].save()
                    
                event.currentRound=1
            
                event.save()
                games = event.getRound(players)
                print(games)
                
        else:
                games=get_list_or_404(Game, tourney=event, eventRound= event.currentRound)

              
                
        context = {'event': event, 'players': players, 'olympics': olympics, 'games': games}
        return render(request, 'tourneyresults.html', context)

@login_required
def recordscore(request, pk, tourney_pk):

    event= get_object_or_404(Tourney, olympics__pk=pk, pk=tourney_pk)
    olympics=get_object_or_404(Olympics, pk=pk)
    players=get_list_or_404(Players, active=True)
    
    

    user = request.user
    player=get_object_or_404(Players, name=user.username)
    
    print('1')
    
    if request.method == 'POST':
        
        form = recordscoreForm(request.POST)
        
        if form.is_valid():

            form.save()
 
    
            scor= form.cleaned_data.get('message')
            scor= int(scor)
            score= get_object_or_404(Score, player = player, tourney= event)
            score.score=scor
            score.save()

            player.save()
            print('got here')

            return redirect('eventresult', pk=olympics.pk, tourney_pk=event.pk)
    else:
        print('2')
        form = recordscoreForm()
   
        print('3')

    
    context = { 'form': form ,'event': event, 'players': players, 'olympics': olympics}
            

    return render(request, 'recordscore.html', context )
    

def endevent(request, pk, tourney_pk):
    print('hiya')
    event= get_object_or_404(Tourney, olympics__pk=pk, pk=tourney_pk)
    players = get_list_or_404(Players, active=True)
    

        
    scores= get_list_or_404(Score.objects.order_by('-score'), tourney=event)
    

    if len(scores) < len(players):
        return redirect('eventresult', pk, tourney_pk)
    
    else:
        
        for i in range(len(scores)):
            
            player= get_object_or_404(Players, name = scores[i].player.name)
            
            result=(Result.objects.filter(player = player, tourney= event))
            
            if not result:
                result=Result.objects.create(player=player, tourney=event, result=i+1)
                result.save()
            else:
                result[0].result=i+1
                result[0].save()
                
        


        return redirect('results', pk)

def win(request, pk, tourney_pk):

    event= get_object_or_404(Tourney, olympics__pk=pk, pk=tourney_pk)
    olympics=get_object_or_404(Olympics, pk=pk)
    players=get_list_or_404(Players, active=True)
    user = request.user
    player=get_object_or_404(Players, name=user.username)
    games= get_list_or_404(Game, tourney= event, eventRound=event.currentRound)

    for i in range(len(games)):
        if i > 4:
            if games[i].player1.name == player.name:
                games[i].winner= player
                games[i].save()
            
        else:
            if games[i].player1.name == player.name or games[i].player2.name== player.name:
                games[i].winner= player
                games[i].save()
            
    return redirect('eventresult', pk, tourney_pk)

def lose(request, pk, tourney_pk):

    event= get_object_or_404(Tourney, olympics__pk=pk, pk=tourney_pk)
    olympics=get_object_or_404(Olympics, pk=pk)
    players=get_list_or_404(Players, active=True)
    user = request.user
    player=get_object_or_404(Players, name=user.username)
    games= get_list_or_404(Game, tourney= event, eventRound=event.currentRound)

    for i in range(len(games)):
        if i > 4:
            if games[i].player1.name == player.name:
                if event.currentRound==1:
                    
                    result= Result.objects.create(player=player, tourney= event, result = 9)
                    result.save()
                    player.eliminated=True
                    player.save()
            
        else:
            if games[i].player1.name == player.name or games[i].player2.name== player.name:
                if event.currentRound==1:
                    
                    result= Result.objects.create(player=player, tourney= event, result = 8)
                    result.save()
                    player.eliminated=True
                    player.save()
                elif event.currentRound==2:
                    result= Result.objects.create(player=player, tourney= event, result = 6)
                    result.save()
                    player.eliminated=True
                    player.save()
                elif event.currentRound==3:
                    result= Result.objects.create(player=player, tourney= event, result = 4)
                    result.save()
                    player.eliminated=True
                    player.save()
                elif event.currentRound==4:
                    result= Result.objects.create(player=player, tourney= event, result = 2)
                    result.save()
                    player.eliminated=True
                    player.save()
            
    return redirect('eventresult', pk, tourney_pk)
    
    
    

def nextround(request, pk, tourney_pk):
 
    event= get_object_or_404(Tourney, olympics__pk=pk, pk=tourney_pk)
    
    

    if event.currentRound == 1 :
        
        results= get_list_or_404(Result, tourney=event)
        if len(results) < 5:
            return redirect('eventresult', pk, tourney_pk)
        else:
            players= get_list_or_404(Players, eliminated=False)
            event.currentRound = 2
            event.save()
            for i in range(4):
                game=Game.objects.create(player1=players[i], player2=players[len(players)-1-i], eventRound=2, tourney=event)
                game.save()
            return redirect('eventresult', pk, tourney_pk)

    elif event.currentRound == 2:

        results= get_list_or_404(Result, tourney=event)
        if len(results) < 9:
            return redirect('eventresult', pk, tourney_pk)
        else:
            players= get_list_or_404(Players, eliminated=False)
            event.currentRound = 3
            event.save()
            for i in range(2):
                game=Game.objects.create(player1=players[i], player2=players[len(players)-1-i], eventRound=3, tourney=event)
                game.save()
            return redirect('eventresult', pk, tourney_pk)
      
    elif event.currentRound == 3:
            players= get_list_or_404(Players, eliminated=False)
            event.currentRound = 4
            event.save()
            game=Game.objects.create(player1=players[0], player2=players[1], eventRound=4, tourney=event)
            game.save()
            return redirect('eventresult', pk, tourney_pk)
    elif event.currentRound == 4:
            players= get_list_or_404(Players, eliminated=False)
            player=players[i]
            event.winner=player
            event.isRunning=False
            event.save()
            result= Result.objects.create(player=players[0], tourney= event, result = 1)
            result.save()

    return redirect('home')

def tourneyresult(request, pk, tourney_pk):
    
    event= get_object_or_404(Tourney, olympics__pk=pk, pk=tourney_pk)
    if event.currentRound==4:
        event.currentRound=3
        event.save()
    elif event.currentRound==3:
        event.currentRound=2
        event.save()
    elif event.currentRound==2:
        event.currentRound=1
        event.save()
    elif event.currentRound==1:
        event.currentRound=4
        event.save()
        
    return redirect('eventresult', pk, tourney_pk)
    
            

    
