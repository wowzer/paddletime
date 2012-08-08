import random
import argparse

from django.core.management import setup_environ
from pingpong import settings
setup_environ(settings)

from pingpong.models import Player
from pingpong.models import Game
from pingpong.models import RankChange

def getNames(file_name):
    f = open(file_name, 'r')
    names = []
    for l in f.readlines():
        first, last = l.strip().split(' ')
        name = (first, last, )
        names.append(name)
    f.close()

    return names

def createPlayers(names):
    Player.objects.all().delete()
    for first, last in sorted(names):
        Player.objects.create(first_name=first,
                              last_name=last)


def populateRandomGames(num_games=300):
    Game.objects.all().delete()

    players = Player.objects.all()
    num_players = len(players)
    for i in range(num_games):
        if i % 10 == 0:
            print i
        loser = winner = random.randint(0,num_players-1)
        while loser == winner:
            loser = random.randint(0,num_players-1)

        Game.objects.create(winning_player = players[winner],
                            losing_player  = players[loser],
                            winning_points = 21,
                            losing_points  = 19)

        # for i, p in enumerate(Player.objects.order_by('-rating')):
        # p.rank = i + 1
        # p.save()

def printRankedPlayers():
    for p in Player.ranked().order_by('rank'):
        print "%2d  %4d %2d %2d %2d  %-10s %-15s" % (p.rank,
                                                     p.rating,
                                                     p.num_games,
                                                     p.winning_games.count(),
                                                     p.losing_games.count(),
                                                     p.first_name,
                                                     p.last_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog = 'PingPong Populator')
    parser.add_argument('action',
                        choices=['names',
                                 'games',
                                 'print',])

    args = parser.parse_args()

    if args.action == 'names':
        names = getNames('names.txt')
        createPlayers(names)
    elif args.action == 'games':
        populateRandomGames(100)
    elif args.action == 'print':
        printRankedPlayers()
