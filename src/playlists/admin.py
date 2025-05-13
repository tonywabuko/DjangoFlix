from django.contrib import admin
from tags.admin import TaggedItemInline
from .models import MovieProxy, TVShowProxy, TVShowSeasonProxy, Playlist, PlaylistItem, PlaylistRelated

class BaseProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ['title']
    fields = ['title', 'description', 'state', 'category', 'video', 'slug']
    class Meta:
        abstract = True

    def get_queryset(self, request):
        return self.model.objects.all().select_related('category', 'video')

class MovieProxyAdmin(BaseProxyAdmin):
    class Meta:
        model = MovieProxy

admin.site.register(MovieProxy, MovieProxyAdmin)

class TVShowSeasonProxyAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline, SeasonEpisodeInline]
    list_display = ['title', 'parent']
    class Meta:
        model = TVShowSeasonProxy
    
    def get_queryset(self, request):
        return TVShowSeasonProxy.objects.all().select_related('parent')

admin.site.register(TVShowSeasonProxy, TVShowSeasonProxyAdmin)

class TVShowProxyAdmin(BaseProxyAdmin):
    inlines = [TaggedItemInline, TVShowSeasonProxyInline]
    class Meta:
        model = TVShowProxy

admin.site.register(TVShowProxy, TVShowProxyAdmin)

class PlaylistAdmin(admin.ModelAdmin):
    inlines = [PlaylistRelatedInline, PlaylistItemInline, TaggedItemInline]
    fields = ['title', 'description', 'slug', 'state', 'active']
    class Meta:
        model = Playlist

    def get_queryset(self, request):
        return Playlist.objects.filter(type=Playlist.PlaylistTypeChoices.PLAYLIST).prefetch_related('items')

admin.site.register(Playlist, PlaylistAdmin)
