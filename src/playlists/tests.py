from django.test import TestCase
from .models import Playlist
from django.utils import timezone
from django.utils.text import slugify
from djangoflix.db.models import PublishedStateOptions
from videos.models import Video


class PlaylistModelsTestCase(TestCase):
    def create_vids(self):
        video_a = Video.objects.create(title="a title", video_id = "o n e")
        self.video_a = video_a
        video_b = Video.objects.create(title="a title", video_id = "t w o")
        self.video_b = video_b
        video_c = Video.objects.create(title="a title", video_id = "t h r e e")
        self.video_c = video_c



    def setUp(self):
        self.create_vids()
        self.first = Playlist.objects.create(
            title="Title is a tut",
            video = self.video_a
        )
        self.second = Playlist.objects.create(
            title="Title is a tut",
            state= PublishedStateOptions.PUBLISH,
            video = self.video_a
        )
        self.second.videos.set( [ self.video_c, self.video_b, self.video_a]) 
        self.second.save()

    def test_playlist_items(self):
        count  = self.second.videos.all().count()
        self.assertEqual(count, 3)

    def test_video_playlist_ids_property(self):
        ids = self.first.video.get_playlist_ids()
        actual_ids = list(Playlist.objects.filter(video=self.video_a)
        .values_list('id', flat=True))
        self.assertEqual(ids, actual_ids)


    def test_playlist_video(self):
        """tests the connection between playlist and video"""
        self.assertEqual(self.first.video_id, self.video_a.id)

    def test_video_playlist(self):
        """test the connection between video and playlist"""
        qs = self.video_a.playlist_featured.all()
        self.assertEqual(qs.count(), 2)

    def test_slug_field(self):
        """test the slug field was set correctly"""
        title = self.first.title
        test_slug = slugify(title)
        self.assertEqual(test_slug, self.first.slug)



    def test_valid_title(self):
        """tests the created vid title is correct"""
        title = 'Title is a tut'
        qs = Playlist.objects.filter(title=title)
        self.assertTrue(qs.exists())


    def test_created_count(self):
        """tests the created object was created once"""
        qs= Playlist.objects.all()
        self.assertEqual(qs.count(),2)

    def test_draft_case(self):
        """test the created vid gets created as DRAFT"""
        qs = Playlist.objects.filter(state=PublishedStateOptions.DRAFT)
        self.assertEqual(qs.count(), 1)

    def test_publish_case(self):
        """test the timezone for the publiushed vid is the current date"""
        qs = Playlist.objects.filter(state=PublishedStateOptions.PUBLISH)
        now = timezone.now()
        published_qs = Playlist.objects.filter(
            state=PublishedStateOptions.PUBLISH,
            publish_timestamp__lte= now
            )
        self.assertTrue(published_qs.exists())

    def test_publish_manager(self):
        published_qs = Playlist.objects.all().published()
        published_qs2 = Playlist.objects.published()

        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), published_qs2.count() )

