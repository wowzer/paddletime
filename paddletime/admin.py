from django.contrib import admin

from paddletime.models import Game
from paddletime.models import Player
from paddletime.models import RankChange
from paddletime.models import WeeklyRank


admin.site.register(Game)
admin.site.register(Player)
admin.site.register(RankChange)
admin.site.register(WeeklyRank)
