import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_uz_number
from .utils import generate_otp_code

ROLE_CHOICES = (
    (1, 'USER'),
    (2, 'ADMINISTRATOR')
)


class User(AbstractUser):
    username = models.CharField(max_length=14, unique=True, validators=[validate_uz_number])
    is_verified = models.BooleanField(default=False)

    role = models.IntegerField(choices=ROLE_CHOICES, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.IntegerField(default=generate_otp_code)
    otp_key = models.UUIDField(default=uuid.uuid4)

    attempts = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.user


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



