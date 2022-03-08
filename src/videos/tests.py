from django.test import TestCase
from .models import Video
from django.utils import timezone
from django.utils.text import slugify
from djangoflix.db.models import PublishedStateOptions

class VideoModelsTestCase(TestCase):
    def setUp(self):
        self.first = Video.objects.create(
            title="Title is a tut",
            video_id = "o n e"
        )
        self.second = Video.objects.create(
            title="Title is a tut",
            state= PublishedStateOptions.PUBLISH,
            video_id = "t w o" 
        )

    def test_slug_field(self):
        title = self.first.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.first.slug)



    def test_valid_title(self):
        """tests the created vid title is correct"""
        title = 'Title is a tut'
        qs = Video.objects.filter(title=title)
        self.assertTrue(qs.exists())


    def test_created_count(self):
        """tests the created object was created once"""
        qs= Video.objects.all()
        self.assertEqual(qs.count(),2)

    def test_draft_case(self):
        """test the created vid gets created as DRAFT"""
        qs = Video.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        """test the timezone for the publiushed vid is the current date"""
        qs = Video.objects.filter(state=PublishedStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Video.objects.filter(
            state=PublishedStateOptions.PUBLISH,
            publish_timestamp__lte= now
            )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = Video.objects.all().published()
        published_qs2 = Video.objects.published()

        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs2.count() )

