from django.contrib import admin

from .models import Video, VideoPublishedProxy, VideoAllProxy

class VideoAllProxyAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'video_id', 'is_published']
    search_fields = ['title']
    list_filter = ['state','active']
    readonly_fields = ['id', 'is_published']
    class Meta:
        model = Video



class VideoPublishedProxyAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_id']
    search_fields = ['title']
    class Meta:
        model = Video

    def get_queryset(self, request) :
        return VideoPublishedProxy.objects.filter(active=True)
        # return super().get_queryset(request)
    

admin.site.register(VideoAllProxy, VideoAllProxyAdmin)
admin.site.register(VideoPublishedProxy, VideoPublishedProxyAdmin)
