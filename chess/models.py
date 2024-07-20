from django.contrib.auth.models import AbstractUser
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=5, decimal_places=2)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=200, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class TournamentParticipant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tournament.name} - {self.player.name}"


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player_1 = models.ForeignKey(Player, related_name='player_1', on_delete=models.CASCADE)
    player_2 = models.ForeignKey(Player, related_name='player_2', on_delete=models.CASCADE)
    result = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.player_1.name} vs {self.player_2.name} | {self.tournament.name}"


class Leaderboard(models.Model):
    tournament = models.OneToOneField(Tournament, on_delete=models.CASCADE, primary_key=True)
