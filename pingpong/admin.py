from django.contrib import admin

from pingpong.models import Game
from pingpong.models import Player
from pingpong.models import RankChange
from pingpong.models import WeeklyRank


admin.site.register(Game)
admin.site.register(Player)
admin.site.register(RankChange)
admin.site.register(WeeklyRank)
