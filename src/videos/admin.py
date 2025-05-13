from django.contrib import admin
from .models import VideoAllProxy, VideoPublishedProxy
from django.utils.timezone import localtime

class VideoAllAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'state', 'video_id', 'is_published', 'get_playlist_ids', 'duration']
    search_fields = ['title']
    list_filter = ['state', 'active']
    readonly_fields = ['id', 'is_published', 'publish_timestamp', 'get_playlist_ids']
    actions = ['mark_as_published']

    def mark_as_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, "Selected videos marked as published.")
    mark_as_published.short_description = "Mark selected videos as published"
    
    def duration(self, obj):
        return f"{obj.duration_in_seconds // 60} min {obj.duration_in_seconds % 60} sec"
    duration.short_description = 'Duration'

    class Meta:
        model = VideoAllProxy

admin.site.register(VideoAllProxy, VideoAllAdmin)


class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id', 'publish_timestamp']
    search_fields = ['title']
    
    def get_queryset(self, request):
        return VideoPublishedProxy.objects.filter(active=True).order_by('-publish_timestamp')

admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)
