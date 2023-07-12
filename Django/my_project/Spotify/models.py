from django.db import models
from mutagen.mp3 import MP3
from datetime import datetime, date
from django.utils import timezone

import mutagen as mutagen
today = date.today()


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    birth_date = models.DateTimeField()
    gender = models.TextField(max_length=50)
    password = models.CharField(max_length=50)


class Singer(models.Model):
    singer_image = models.ImageField(upload_to='photos/singer/')
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)


class Album(models.Model):
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)
    album_name = models.TextField(max_length=50)
    album_description = models.TextField(max_length=100)
    album_image = models.ImageField(upload_to='photos/album/')


class Music(models.Model):
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    music_image = models.ImageField(upload_to='photos/music/')
    day = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to='music/')
    count = models.IntegerField()
    artist = models.CharField(null=True, max_length=50)
    is_like = models.BooleanField(default=False)
    duration = models.CharField(max_length=20, null=True)
    paginate_by = 2

    def get_time(self):
        audio = MP3(self.audio_file)
        length = audio.info.length
        return length

    def get_length(self):
        audio = MP3(self.audio_file)
        length = audio.info.length
        return int(length / 60)

    def get_second(self):
        audio = MP3(self.audio_file)
        length = audio.info.length
        return int(length % 60)

    def get_day_or_hour(self):
        now = timezone.now()
        diff = now - self.day
        days = diff.days
        hours = int(diff.seconds / 3600)
        if days > 0:
            return f"{days} дня назад"
        else:
            return f"{hours} часа назад"


class PlayList(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='photos/playlist')
    description = models.CharField(max_length=100)


class spotify_playlist(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='photos/spotify_playlist', null=True)
    description = models.CharField(max_length=100)

    def short_description(self):
        return f"{self.description[:27]}..."


class spotify_playlist_Music(models.Model):
    spotify_playlist = models.ForeignKey('spotify_playlist', on_delete=models.CASCADE)
    music = models.ForeignKey('Music', on_delete=models.CASCADE)


class Playlist_Music(models.Model):
    playlist = models.ForeignKey('PlayList', on_delete=models.CASCADE)
    music = models.ForeignKey('Music', on_delete=models.CASCADE)


class Favourite_Album(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)


class Favourite_Music(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    music = models.ForeignKey('Music', on_delete=models.CASCADE)
