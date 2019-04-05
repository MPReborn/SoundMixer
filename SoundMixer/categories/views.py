from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from random import randint
from django.db.models import Count

from .forms import SongForm, SearchForm, TagForm, AddTagForm

from .models import Category, Song

def getrandomsongid(song_id_list):
    #this 'list' is a string so we have to process it a bit first
    song_id_list = song_id_list.replace("[", "")
    song_id_list = song_id_list.replace("]", "")
    real_list = song_id_list.split(',')
    rand_id = randint(0, len(real_list) - 1)
    return real_list[rand_id]

def taglist(request):
    tag_list = Category.objects.annotate(s_count=Count('song')).order_by('-s_count')
    context = {
        'tag_list': tag_list,
    }
    return render(request, 'categories/tags.html', context)

def songlist(request, songquerry):
    song_id_list = []
    for song in songquerry:
        song_id_list.append(song.id)
    context = {
        'song_list': songquerry,
    }
    if song_id_list:
        random_song_id = getrandomsongid(str(song_id_list))
        random_song = Song.objects.get(id = random_song_id)
        context['song_id_list'] = song_id_list
        context['random_song'] = random_song
    return render(request, 'categories/list.html', context)

def gettagsongs(request, tag_name):
    tag = Category.objects.get(name=tag_name)
    songquerry = Song.objects.filter(tags=tag)
    return songlist(request, songquerry)

def search(request):
    if (request.method == "POST"):
        form = SearchForm(request.POST)
        if form.is_valid():
            song_list = Song.objects.all()
            for tag_name in form.cleaned_data['include']:
                tag = Category.objects.get(name=tag_name)
                song_list = song_list & Song.objects.filter(tags=tag)
            for tag_name in form.cleaned_data['exclude']:
                tag = Category.objects.get(name=tag_name)
                song_list = song_list & Song.objects.exclude(tags=tag)
            return songlist(request, song_list)
    else:
        form = SearchForm()
    return render(request, 'categories/search.html', { 'form': form })


def song(request, song_id, song_id_list = ''):
    song = Song.objects.get(id=song_id)
    if song_id_list:
        random_song_id = getrandomsongid(song_id_list)
        random_song = Song.objects.get(id = random_song_id)
    if (request.method == "POST"):
        form = AddTagForm(request.POST)
        if form.is_valid():
            for tag in form.cleaned_data['tags']:
                song.tags.add(Category.objects.get(name= tag))
            song.save()
    else:
        form = AddTagForm()
    context = {
        'song': song,
        'form': form,
    }
    if song_id_list:
        context['song_id_list'] = song_id_list
        context['random_song'] = random_song
    return render(request, 'categories/song.html', context)

def submitsong(request):
    if (request.method == "POST"):
        form = SongForm(request.POST)
        if form.is_valid():
            new_song = Song(
                name = form.cleaned_data['name'],
                link = form.cleaned_data['link'],
                )
            new_song.save()
            for tag in form.cleaned_data['tags']:
                new_song.tags.add(Category.objects.get(name= tag))
            new_song.save()
            #currently returns to the main page.
            return HttpResponseRedirect('/')
    else:
        form = SongForm()
    return render(request, 'categories/submit_song.html', { 'form': form })

def submittag(request):
    if (request.method == "POST"):
        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = Category(
                name = form.cleaned_data['tag'],
                )
            new_tag.save()
            #currently returns to the main page.
            return HttpResponseRedirect('/')
    else:
        form = TagForm()
    return render(request, 'categories/submit_tag.html', { 'form': form })

class signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'categories/signup.html'
