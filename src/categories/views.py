from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import render
from playlists.mixins import PlaylistMixin
from playlists.models import Playlist
from .models import Category

class CategoryListView(ListView):
    queryset = Category.objects.filter(active=True).annotate(pl_count=Count('playlists')).filter(pl_count__gt=0)

class CategoryDetailView(PlaylistMixin, ListView):
    """
    Display playlists by category.
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Category.objects.filter(slug=self.kwargs.get('slug')).first()
        if not obj:
            raise Http404
        context['object'] = obj
        context['title'] = obj.title
        return context

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return Playlist.objects.filter(category__slug=slug).movie_or_show()


