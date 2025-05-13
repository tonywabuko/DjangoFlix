class SearchView(PlaylistMixin, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q")
        context['title'] = f"Searched for {query}" if query else 'Perform a search'
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        return Playlist.objects.all().movie_or_show().search(query=query)


class TVShowSeasonDetailView(PlaylistMixin, DetailView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        show_slug = self.kwargs.get("showSlug")
        season_slug = self.kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            return TVShowSeasonProxy.objects.get(
                state=PublishStateOptions.PUBLISH,
                publish_timestamp__lte=now,
                parent__slug__iexact=show_slug,
                slug__iexact=season_slug
            )
        except TVShowSeasonProxy.DoesNotExist:
            raise Http404
