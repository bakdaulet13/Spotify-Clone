from django.urls import path

from .views import *
urlpatterns = {
    path('', main),
    path('main/', main),
    path('edit/', editt),
    path('Edit', editt),
    path('add_singer', singer),
    path('add_album', album),
    path('add_music', music),
    path('add_spotify_playlist', spotify_play),
    path('add_spotify_playlist_music', spotify_playlist_musics),
    path('registration', registration_user),
    path('login', login),
    path('log_out/', logout),
    path('pl/<int:pl_id>', playlist),
    path('playlists/', PL),
    path('playlists/<str:m_name>', add_pl),
    path('playlists/<int:pl_id>', ret_pl),
    path('main/', come_back),
    path('m/', index),
    path('add_pl/', add_pl_user),
    path('search/', search_music),
    path('searching', search_music),
    path('liked_songs/', fav_music),
    path('important/', crucial),
}

