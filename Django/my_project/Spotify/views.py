from datetime import datetime, date
import mutagen as mutagen
today = date.today()
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator

from .models import *


# Create your views here.


def singer(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        img = request.FILES['img']
        s = Singer(singer_image=img, first_name=f_name, last_name=l_name)
        s.save()
        context = {
            'temp': 1
        }
        return render(request, 'Spotify/admin_music.html', context=context)
    context = {
        'temp': 1
    }
    return render(request, 'Spotify/admin_music.html', context=context)


def album(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        s = Singer.objects.get(first_name=f_name, last_name=l_name)
        img = request.FILES['img']
        name = request.POST['name']
        desc = request.POST['desc']
        a = Album(singer_id=s.id, album_name=name, album_description=desc, album_image=img)
        a.save()
        context = {
            'temp': 2
        }
        return render(request, 'Spotify/admin_music.html', context=context)
    context = {
        'temp': 2
    }
    return render(request, 'Spotify/admin_music.html', context=context)


def music(request):
    if request.method == 'POST':
        album_name = request.POST['a_name']
        img = request.FILES['img']
        name = request.POST['name']
        audio = request.FILES['audio']
        a = Album.objects.get(album_name=album_name)
        m = Music.objects.filter(name=name, music_image=img, audio_file=audio, count=1, album_id=a.id)
        if len(m) == 0:
            m = Music(name=name, music_image=img, audio_file=audio, count=1, album_id=a.id)
            m.save()
        musics = Music.objects.all()
        context = {
            'temp': 3,
            'music': musics
        }
        return render(request, 'Spotify/admin_music.html', context=context)
    context = {
        'temp': 3
    }
    return render(request, 'Spotify/admin_music.html', context=context)


def spotify_play(request):
    if request.method == 'POST':
        playlist_name = request.POST['p_name']
        description = request.POST['description']
        img = request.FILES['img']
        sss = spotify_playlist.objects.filter(name=playlist_name, description=description, image=img)
        if len(sss) == 0:
            sss = spotify_playlist(name=playlist_name, description=description, image=img)
            sss.save()
        # playlist = spotify_playlist()
        context = {
            'temp': 4,
            'name': playlist_name,
            'desc': description,
            'img': img,

        }
        return render(request, 'Spotify/admin_music.html', context=context)
    context = {
        'temp': 4
    }
    return render(request, 'Spotify/admin_music.html', context=context)


def spotify_playlist_musics(request):
    if request.method == 'POST':
        music_name = request.POST['m_name']
        m = Music.objects.get(name=music_name)
        play_name = request.POST['p_name']
        p = spotify_playlist.objects.get(name=play_name)
        s = spotify_playlist_Music.objects.filter(music_id=m.id, spotify_playlist_id=p.id)
        if len(s) == 0:
            s = spotify_playlist_Music(music_id=m.id, spotify_playlist_id=p.id)
            s.save()
        pl_music = spotify_playlist_Music.objects.all()
        context = {
            'temp': 5,
            'playlist': pl_music
        }
        return render(request, 'Spotify/admin_music.html', context=context)
    context = {
        'temp': 5
    }
    return render(request, 'Spotify/admin_music.html', context=context)


def registration_user(request):
    if request.method == 'POST':
        email_check = False
        pass_check1 = False
        pass_check2 = False
        name_check = False
        day_check = False
        month_check = False
        year_check = False
        gender_check = False
        check3_check = False
        e_name = request.POST['e_name']
        password = request.POST['password']
        name = request.POST['name']
        day = request.POST['day']
        month = request.POST['month']
        year = request.POST['year']
        # gender = request.POST['gender']
        # check3 = request.POST['check3']
        if len(e_name) < 0:
            email_check = True
        if len(password) < 0:
            pass_check1 = True
        else:
            if not any(char.isdigit() for char in password) or not any(
                    char.isupper() for char in password) or not any(char.islower() for char in password) and len(password) < 8:
                pass_check2 = True
        if len(name) < 0:
            name_check = True
        if len(day) == 0:
            day_check = True
        if month == '777':
            month_check = True
        if len(year) == 0:
            year_check = True
        if not request.POST.getlist('gender'):
            gender_check = True
        if not request.POST.getlist('check3'):
            check3_check = True
        context = {
            'year': year
        }

        if email_check:
            context['email_error'] = 'Введите адрес электронной почты.'
        if pass_check1:
            context['password_error1'] = 'Введите пароль.'
        if pass_check2:
            context[
                'password_error2'] = 'Пароль должен содержать одну маленькую букву, одну большую букву и одну цифру.'
        if name_check:
            context['name_error'] = 'Укажите имя для своего профиля.'
        if day_check:
            context['day_error'] = 'Укажите действительный день месяца.'
        if month_check:
            context['month_error'] = 'Выберите месяц.'
        if year_check:
            context['year_error'] = 'Укажите действительный год.'
        if gender_check:
            context['gender_error'] = 'Выберите свой пол.'
        if check3_check:
            context['check3_error'] = 'Чтобы продолжить, примите Условия пользования.'
        if email_check or name_check or day_check or month_check or year_check or gender_check or check3_check or pass_check2:
            return render(request, 'Spotify/registration.html', context=context)
        else:
            gender = request.POST['gender']
            d = str(year) + '-' + str(month) + '-' + str(day)
            temp = datetime.strptime(d, '%Y-%m-%d')
            u = User(name=name, email=e_name, birth_date=temp, gender=gender, password=password)
            u.save()
            return render(request, 'Spotify/login.html')
    return render(request, 'Spotify/registration.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        u1 = User.objects.filter(name=username)
        u2 = User.objects.filter(email=username)
        singer = Singer.objects.all()
        temp_id = 0
        mmm = 0
        for s in singer:
            al = Album.objects.filter(singer_id=s.id)
            if len(al) > mmm:
                temp_id = s.id
                mmm = len(al)
        context = {
            'error': 'Неправильное имя пользователя или пароль.'
        }
        if len(u1) < 1:
            if len(u2) < 1:
                return render(request, 'Spotify/login.html', context=context)
            else:
                u = User.objects.get(email=username)
                if u.password == password:
                    request.session['user'] = u.id
                    id = request.session.get('user', None)
                    cnt = Favourite_Music.objects.filter(user_id=id)
                    pls = PlayList.objects.filter(user_id=id)
                    name = 'Мой плейлист N' + str(len(pls) + 1)
                    p = PlayList(name=name, description="it's my playlist", user_id=id)
                    p.save()
                    pls = PlayList.objects.filter(user_id=id)
                    play_list = [
                        PlayList(
                            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
                            name=p.name,
                            image=p.image,
                            description=p.description,
                            user_id=p.user_id
                        )
                        for p in pls
                    ]
                    context['singer'] = Singer.objects.get(id=temp_id)
                    context['pls'] = play_list
                    context['cnt'] = len(cnt)
                    context['temp'] = 4
                    id = request.session.get('user', None)
                    cnt = Favourite_Music.objects.filter(user_id=id)
                    context['cnt'] = len(cnt)
                    return render(request, 'Spotify/index.html', context=context)
                else:
                    return render(request, 'Spotify/login.html', context=context)
        else:
            uu = User.objects.get(name=username)
            context['temp'] = 4
            id = request.session.get('user', None)
            cnt = Favourite_Music.objects.filter(user_id=id)
            id = request.session.get('user', None)
            cnt = Favourite_Music.objects.filter(user_id=id)
            pls = PlayList.objects.filter(user_id=id)
            name = 'Мой плейлист N' + str(len(pls) + 1)
            p = PlayList(name=name, description="it's my playlist", user_id=id)
            p.save()
            pls = PlayList.objects.filter(user_id=id)
            play_list = [
                PlayList(
                    id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
                    name=p.name,
                    image=p.image,
                    description=p.description,
                    user_id=p.user_id
                )
                for p in pls
            ]
            context['singer'] = Singer.objects.get(id=temp_id)
            context['pls'] = play_list
            context['cnt'] = len(cnt)
            if uu.password == password:
                request.session['user'] = uu.id
                return render(request, 'Spotify/index.html', context=context)
            else:
                return render(request, 'Spotify/login.html', context=context)

    return render(request, 'Spotify/login.html')


def come_back(request):
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    context = {
        'temp': 1,
        'cnt': len(cnt)
    }
    return render(request, 'Spotify/index.html', context=context)

def logout(request):
    if 'user' in request.session:
        del request.session['user']
    else:
        return render(request, 'Spotify/login.html')
    pl = spotify_playlist.objects.all()[:6]
    context = {
        'pl': pl,
        'temp': 1
    }
    return render(request, 'Spotify/main.page.html', context=context)


def main(request):
    pl = spotify_playlist.objects.all()[:6]
    context = {
        'pl': pl,
        'temp': 1
    }
    return render(request, 'Spotify/main.page.html', context=context)


def playlist(request, pl_id):
    p = spotify_playlist.objects.get(id=pl_id)
    sp_pl_m = spotify_playlist_Music.objects.filter(spotify_playlist_id=pl_id)
    music_ids = []
    for s in sp_pl_m:
        music_ids.append(s.music_id)

    musics = Music.objects.filter(id__in=music_ids)
    music_list = [
        Music(
            album_id=Album.objects.get(id=m.album_id).album_name,
            name=m.name,
            music_image=m.music_image,
            day=m.get_day_or_hour(),
            audio_file=m.audio_file,
            count=m.count,
            id=seq_num
        )
        for seq_num, m in enumerate(musics, start=1)
    ]
    fav_music = Favourite_Music.objects.filter(id__in=music_ids)
    count_time = 0
    context = {
        'temp': 5,
        'musics': music_list,
        'p': p,
        'count_musics': len(musics),
        'count_likes': len(fav_music)
        }
    for m in musics:
        count_time += m.get_time()
    cnt = int(count_time/3600)
    if cnt == 0:
        cnt = int(count_time/60)
        context['tt'] = 0
    else:
        context['tt'] = 1
    context['count_duration'] = cnt
    return render(request, 'Spotify/main.page.html', context=context)


def PL(request):
    top_twenty = Music.objects.order_by('-count')[:20]
    music_list = [
        Music(
            album_id=Album.objects.get(id=m.album_id).album_name,
            name=m.name,
            music_image=m.music_image,
            day=m.get_day_or_hour(),
            audio_file=m.audio_file,
            count=m.count,
            id=seq_num,
            is_like=m.is_like
        )
        for seq_num, m in enumerate(top_twenty, start=1)
    ]
    for m in music_list:
        a = Album.objects.get(album_name=m.album_id)
        s = Singer.objects.get(id=a.singer_id)
        m.artist = s.first_name
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    pls = PlayList.objects.filter(user_id=id)
    play_list = [
        PlayList(
            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
            name=p.name,
            image=p.image,
            description=p.description,
            user_id=p.user_id
        )
        for p in pls
    ]
    context = {
        'temp': 5,
        'musics': music_list,
        'cnt': len(cnt),
        'pls': play_list,
    }
    return render(request, 'Spotify/index.html', context=context)


def add_pl(request, m_name):
    m = Music.objects.get(name=m_name)
    last_object = PlayList.objects.order_by('-id').first()
    sp_m = Playlist_Music(music_id=m.id, playlist_id=last_object.id)
    sp_m.save()
    top_twenty = Music.objects.order_by('-count')[:20]
    music_list = [
        Music(
            album_id=Album.objects.get(id=m.album_id).album_name,
            name=m.name,
            music_image=m.music_image,
            day=m.get_day_or_hour(),
            audio_file=m.audio_file,
            count=m.count,
            id=seq_num,
            is_like=m.is_like
        )
        for seq_num, m in enumerate(top_twenty, start=1)
    ]
    for m in music_list:
        a = Album.objects.get(album_name=m.album_id)
        s = Singer.objects.get(id=a.singer_id)
        m.artist = s.first_name
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    pls = PlayList.objects.filter(user_id=id)
    play_list = [
        PlayList(
            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
            name=p.name,
            image=p.image,
            description=p.description,
            user_id=p.user_id
        )
        for p in pls
    ]
    context = {
        'temp': 5,
        'musics': music_list,
        'cnt': len(cnt),
        'pls': play_list,
    }
    return render(request, 'Spotify/index.html', context=context)


def ret_pl(request, pl_id):
    top_twenty = Music.objects.order_by('-count')[:20]
    music_list = [
        Music(
            album_id=Album.objects.get(id=m.album_id).album_name,
            name=m.name,
            music_image=m.music_image,
            day=m.get_day_or_hour(),
            audio_file=m.audio_file,
            count=m.count,
            id=seq_num,
            is_like=m.is_like,
        )
        for seq_num, m in enumerate(top_twenty, start=1)
    ]
    for m in music_list:
        a = Album.objects.get(album_name=m.album_id)
        s = Singer.objects.get(id=a.singer_id)
        m.artist = s.first_name
        if 'temp' in request.session:
            if request.session['temp'] != pl_id:
                if m.id == pl_id:
                    id = request.session.get('user', None)
                    mt = Music.objects.get(name=m.name)
                    if mt.is_like:
                        mt.is_like = False
                        mt.save()
                        f_m = Favourite_Music.objects.get(music_id=mt.id, user_id=id)
                        f_m.delete()
                        m.is_like = False
                    else:
                        mt.is_like = True
                        mt.save()
                        f_m = Favourite_Music(music_id=mt.id, user_id=id)
                        f_m.save()
                        m.is_like = True
    request.session['temp'] = pl_id
    for m in music_list:
        print(m.is_like)
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    pls = PlayList.objects.filter(user_id=id)
    play_list = [
        PlayList(
            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
            name=p.name,
            image=p.image,
            description=p.description,
            user_id=p.user_id
        )
        for p in pls
    ]
    context = {
        'temp': 5,
        'musics': music_list,
        'cnt': len(cnt),
        'pl_id': pl_id,
        'pls': play_list,
    }
    return render(request, 'Spotify/index.html', context=context)


def fav_music(request):
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    temp_music = []
    for c in cnt:
        temp_music.append(c.music_id)
    cnt = Music.objects.filter(id__in=temp_music)
    music_list = [
        Music(
            album_id=Album.objects.get(id=m.album_id).album_name,
            name=m.name,
            music_image=m.music_image,
            day=m.get_day_or_hour(),
            audio_file=m.audio_file,
            count=m.count,
            id=seq_num,
            is_like=m.is_like,
        )
        for seq_num, m in enumerate(cnt, start=1)
    ]
    pls = PlayList.objects.filter(user_id=id)
    play_list = [
        PlayList(
            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
            name=p.name,
            image=p.image,
            description=p.description,
            user_id=p.user_id
        )
        for p in pls
    ]
    context = {
        'temp': 5,
        'musics': music_list,
        'cnt': len(cnt),
        'pls': play_list,
    }

    return render(request, 'Spotify/index.html', context=context)


def index(request):
    # sp_pl_m = spotify_playlist_Music.objects.filter(spotify_playlist_id=pl_id)
    # music_ids = []
    # pl_id2 = pl_id
    # for s in sp_pl_m:
        # music_ids.append(s.music_id)

    paginator = Paginator(Music.objects.order_by('-count')[:20], 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'Spotify/pleer.html', context=context)


def add_pl_user(request):
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    pls = PlayList.objects.filter(user_id=id)
    name = 'Мой плейлист N' + str(len(pls)+1)
    p = PlayList(name=name, description="it's my playlist", user_id=id)
    p.save()
    pls = PlayList.objects.filter(user_id=id)
    play_list = [
        PlayList(
            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
            name=p.name,
            image=p.image,
            description=p.description,
            user_id=p.user_id
        )
        for p in pls
    ]
    context = {
        'temp': 1,
        'cnt': len(cnt),
        'pls': play_list
    }
    return render(request, 'Spotify/index.html', context=context)


def search_music(request):
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    pls = PlayList.objects.filter(user_id=id)
    play_list = [
        PlayList(
            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
            name=p.name,
            image=p.image,
            description=p.description,
            user_id=p.user_id
        )
        for p in pls
    ]
    if request.method == 'POST':
        search_word = request.POST['search_input']
        music = Music.objects.filter(Q(name__icontains=search_word))
    else:
        music = Music.objects.all()
    music_list = [
        Music(
            album_id=Album.objects.get(id=m.album_id).album_name,
            name=m.name,
            music_image=m.music_image,
            day=m.get_day_or_hour(),
            audio_file=m.audio_file,
            count=m.count,
            id=seq_num,
            is_like=m.is_like,
        )
        for seq_num, m in enumerate(music, start=1)
    ]
    context = {
        'temp': 3,
        'cnt': len(cnt),
        'pls': play_list,
        'musics': music_list
    }
    return render(request, 'Spotify/index.html', context=context)


def crucial(request):
    id = request.session.get('user', None)
    cnt = Favourite_Music.objects.filter(user_id=id)
    pls = PlayList.objects.filter(user_id=id)
    play_list = [
        PlayList(
            id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
            name=p.name,
            image=p.image,
            description=p.description,
            user_id=p.user_id
        )
        for p in pls
    ]
    # sp = spotify_playlist.objects.all()
    # temp_list = []
    # for s in sp:
    #     temp_list.append(s.id)
    # sp_m = spotify_playlist_Music.objects.filter(spotify_playlist_id__in=temp_list)

    singer = Singer.objects.all()
    temp_id = 0
    mmm = 0
    for s in singer:
        al = Album.objects.filter(singer_id=s.id)
        if len(al) > mmm:
            temp_id = s.id
            mmm = len(al)

    context = {
     'temp': 4,
     'cnt': len(cnt),
     'pls': play_list,
     'singer': Singer.objects.get(id=temp_id)
    }
    return render(request, 'Spotify/index.html', context=context)


def editt(request):
    id = request.session.get('user', None)
    user = User.objects.get(id=id)
    context = {
        'id': id,
        'user': user
    }
    if request.method == 'POST':
        e_name = request.POST['e_name']
        password = request.POST['password']
        temp_user = User.objects.get(id=id)
        print(e_name)
        temp_user.email = e_name
        temp_user.password = password
        temp_user.save()
        singer = Singer.objects.all()
        temp_id = 0
        mmm = 0
        for s in singer:
            al = Album.objects.filter(singer_id=s.id)
            if len(al) > mmm:
                temp_id = s.id
                mmm = len(al)
        cnt = Favourite_Music.objects.filter(user_id=id)
        pls = PlayList.objects.filter(user_id=id)
        name = 'Мой плейлист N' + str(len(pls) + 1)
        p = PlayList(name=name, description="it's my playlist", user_id=id)
        p.save()
        pls = PlayList.objects.filter(user_id=id)
        play_list = [
            PlayList(
                id=len(Playlist_Music.objects.filter(playlist_id=p.id)),
                name=p.name,
                image=p.image,
                description=p.description,
                user_id=p.user_id
            )
            for p in pls
        ]
        context['singer'] = Singer.objects.get(id=temp_id)
        context['pls'] = play_list
        context['cnt'] = len(cnt)
        context['temp'] = 4
        return render(request, 'Spotify/index.html', context=context)
    return render(request, 'Spotify/edit_profile.html', context=context)
