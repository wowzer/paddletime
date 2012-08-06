from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import Q

from sorl.thumbnail import ImageField

class Player(models.Model):
    first_name     = models.CharField(max_length=60)
    last_name      = models.CharField(max_length=60)

    head_shot      = ImageField(upload_to='head_shots', null=True, blank=True)

    rating         = models.PositiveSmallIntegerField(default=1600)
    rank           = models.PositiveSmallIntegerField(null=True, blank=True)

    last_game      = models.DateField(null=True, blank=True)
    num_opponents  = models.PositiveSmallIntegerField(default=0)
    num_games      = models.PositiveSmallIntegerField(default=0)
    num_wins       = models.PositiveSmallIntegerField(default=0)
    num_losses     = models.PositiveSmallIntegerField(default=0)

    create_date    = models.DateTimeField(auto_now=True)

    def gameUpdate(self, opponent, won):
        games = Game.objects.filter(Q(winning_player=self)|Q(losing_player=self))
        self.num_games  = games.count()
        self.num_wins   = self.winning_games.count()
        self.num_losses = self.losing_games.count()
        self.last_game  = games.latest()

        opponents = set([g.losing_player.id for g in self.winning_games.all()] +
                        [g.winning_player.id for g in self.losing_games.all()])
        self.num_opponents = len(opponents)

        self.rating = self.calcRating(opponent, won)

    def winProbability(self, opponent):
        difference = opponent.rating - self.rating
        return 1/(10**(difference/400.0) + 1)

    def calcRating(self, opponent, won, k=32):
        scoring_point = 1 if won else 0
        return self.rating + (k * (scoring_point - self.winProbability(opponent)))

    @classmethod
    @transaction.commit_on_success
    def updateRankings(cls):
        num_ranked = Player.objects.filter(num_opponents__gte=3).count()
        for i, p in enumerate(Player.objects.filter(num_opponents__gte=3).order_by('rating')):
            new_rank = num_ranked - i
            if p.rank and p.rank != new_rank:
                RankChange.objects.create(player   = p,
                                          rank_old = p.rank,
                                          rank_new = new_rank)
            p.rank = new_rank
            p.save()

    @classmethod
    def ranked(cls):
        return Player.objects.filter(num_opponents__gte=3)

    @classmethod
    def unranked(cls):
        return Player.objects.filter(num_opponents__lt=3)

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)


class RankChange(models.Model):
    player         = models.ForeignKey(Player)
    rank_old       = models.PositiveSmallIntegerField(null=True, blank=True)
    rank_new       = models.PositiveSmallIntegerField()
    timestamp      = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s: %d --> %d" % (self.player, self.rank_old, self.rank_new)

class Game(models.Model):
    winning_player = models.ForeignKey(Player, related_name='winning_games')
    losing_player  = models.ForeignKey(Player, related_name='losing_games')
    winning_points = models.PositiveSmallIntegerField()
    losing_points  = models.PositiveSmallIntegerField()
    timestamp      = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by  = "timestamp"

    def save(self, *args, **kwargs):
        super(Game, self).save(*args, **kwargs)

        self.winning_player.gameUpdate(self.losing_player, True)
        self.losing_player.gameUpdate(self.winning_player, False)
        self.winning_player.save()
        self.losing_player.save()

        Player.updateRankings()

    def __unicode__(self):
        return u"%s %d | %s %d" % (self.winning_player.first_name, self.winning_points,
                                   self.losing_player.first_name,  self.losing_points)

class WeeklyRank(models.Model):
    player         = models.ForeignKey(Player)
    week           = models.DateField()
    rank           = models.PositiveSmallIntegerField()
