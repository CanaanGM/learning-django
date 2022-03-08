from .models import PublishedStateOptions
from django.utils.text import slugify
from django.utils import timezone


def slugify_pre_save(sender, instance, *args, **kwargs):
    title = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(title)


def publish_state_pre_save(sender, instance,*args, **kwargs ):
    is_publish:bool = instance.state == PublishedStateOptions.PUBLISH
    is_draft:bool = instance.state == PublishedStateOptions.DRAFT

    if is_publish and instance.publish_timestamp is None :
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None
