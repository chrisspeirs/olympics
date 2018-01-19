from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
import random

# Create your models here.

class Players(models.Model):

##need to come back to user to define what happens when created
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    name=models.CharField(max_length=50, unique=True)
    eventPoints =models.IntegerField(default = 0)
    totalPoints =models.IntegerField(default=0)
    active= models.BooleanField(default= False)
    eliminated= models.BooleanField(default= False)

    

    def __str__(self):
        return self.name

    def joinOlympics(self, olympics):
        self.active= True
        olympics.totalPlayers= olympics.totalPlayers+1
        points = Points.objects.create(player = self, olympics = olympics, result=0)
        points.save()
        

    def getTotal(self, olympics):

        results = get_list_or_404(Result.objects.order_by('result'), tourney__olympics=olympics, player = self )
        total = 0
        for i in range(len(results)-1):
            total = total + results[i].result
        return total
            
        
    
class Olympics(models.Model):

    name=models.CharField(max_length=50, unique=True, default="")
    year = models.IntegerField(default = 2017, unique=True)
    totalPlayers=models.IntegerField(default = 0)
    isRunning=models.BooleanField(default= False)
   

    def __str__(self):
        return self.name




class Tourney(models.Model):

    name=models.CharField(max_length=50, default='Bowling')
    olympics=models.ForeignKey(Olympics, related_name='olympics',null=True, on_delete=models.SET_NULL)
    winner= models.ForeignKey(Players, related_name='touneywinner', null=True,on_delete=models.SET_NULL)
    isRanked=models.BooleanField(default=True)
    currentRound=models.IntegerField(default=0)
    isRunning=models.BooleanField(default=True)
    def __str__(self):
        
        return self.name

    def getRound(self, players):

        games=[]
        random.shuffle(players)
        print(len(players))
        
        for i in range(8):
            
            if i>4:
                game=Game.objects.create(player1=players[i], eventRound=self.currentRound, tourney=self)
                game.save()
                games.append(game)

            else:
                
                game= Game.objects.create(player1= players[i], player2= players[len(players)-1-i],eventRound=self.currentRound, tourney=self)
                game.save()
                games.append(game)
            
        return games







class Game(models.Model):

    
    player1= models.ForeignKey(Players, related_name='player1', null= True, on_delete=models.CASCADE)
    player2= models.ForeignKey(Players, related_name='player2', null= True, on_delete=models.CASCADE)
    eventRound=models.IntegerField(default=1, null=True)    
    winner= models.ForeignKey(Players, related_name='game', null=True,on_delete=models.CASCADE)
   

    tourney= models.ForeignKey(Tourney, related_name='tourney',null=True,on_delete=models.CASCADE)

    def __str__(self):
       
        return self.player1.name

    
class Score(models.Model):

    player= models.ForeignKey(Players, related_name='player',null=True,on_delete=models.SET_NULL)
    tourney= models.ForeignKey(Tourney, related_name='olympic', null=True,on_delete=models.SET_NULL)
    score = models.IntegerField(default = 0)

    class Meta:
        unique_together = (("player", "tourney"),)

class Result(models.Model):

    player= models.ForeignKey(Players, related_name='playerr',null=True,on_delete=models.SET_NULL)
    tourney= models.ForeignKey(Tourney, related_name='olympic1', null=True,on_delete=models.SET_NULL)
    result = models.IntegerField(default = 0)

    class Meta:
        unique_together = (("player", "tourney"),)

class Points(models.Model):

    player= models.ForeignKey(Players, related_name='playerrs',null=True,on_delete=models.SET_NULL)
    olympics= models.ForeignKey(Olympics, related_name='olympicss', null=True,on_delete=models.SET_NULL)
    result = models.IntegerField(default = 0)

    class Meta:
        unique_together = (("player", "olympics"),)

    
    



    
