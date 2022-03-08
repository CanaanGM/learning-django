from django.contrib import admin

from .models import Playlist


class PlaylistAllProxyAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'video_id', 'is_published']
    search_fields = ['title']
    list_filter = ['state','active']
    readonly_fields = ['id', 'is_published']
    class Meta:
        model = Playlist



class PlaylistPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    class Meta:
        model = Playlist

    def get_queryset(self, request) :
        return Playlist.objects.filter(active=True)
        # return super().get_queryset(request)
    

admin.site.register(Playlist, PlaylistAllProxyAdmin)
# admin.site.register(Playlist, VideoPublishedProxyAdmin)