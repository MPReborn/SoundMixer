from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from .forms import SongForm, SearchForm, TagForm

from .models import Category, Song

def taglist(request):
    tag_list = Category.objects.all()
    context = {
        'tag_list': tag_list,
    }
    return render(request, 'categories/tags.html', context)

def songlist(request, songquerry):
    context = {
        'song_list': songquerry,
    }
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

def song(request, song_id):
    song = Song.objects.get(id=song_id)
    context = {
        'song': song,
    }
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
