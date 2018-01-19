from django.contrib import admin
from .models import Players, Olympics, Tourney, Game, Score, Result, Points

# Register your models here.

admin.site.register(Players)
admin.site.register(Tourney)
admin.site.register(Olympics)
admin.site.register(Game)
admin.site.register(Score)
admin.site.register(Result)
admin.site.register(Points)
