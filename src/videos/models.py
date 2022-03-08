from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save

from djangoflix.db.models import PublishedStateOptions
from djangoflix.db.recievers import publish_state_pre_save, slugify_pre_save 

class VideoQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishedStateOptions.PUBLISH,
            publish_timestamp__lte= now
        )
        

class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()


class Video(models.Model):

    title = models.CharField(max_length = 255)

    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)
    video_id = models.CharField(max_length = 255, unique=True)
    active = models.BooleanField(default=True)

    updated = models.DateTimeField(
        auto_now=True
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    publish_timestamp = models.DateTimeField(
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True
    )
    state = models.CharField(
        max_length=2,
        choices=PublishedStateOptions.choices,
        default=PublishedStateOptions.DRAFT
    )

    objects = VideoManager()
    
    @property
    def is_published(self, *args, **kwargs):
        return self.active

    def get_playlist_ids(self):
        return list(self.playlist_featured.all().values_list('id', flat=True))

class VideoAllProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'All Video'
        verbose_name_plural = 'All Videos'

class VideoPublishedProxy(Video):
    class Meta:
        proxy = True
        verbose_name = 'Published Video'
        verbose_name_plural = 'Published Videos'




pre_save.connect(publish_state_pre_save, sender= Video)
pre_save.connect(slugify_pre_save, sender= Video)