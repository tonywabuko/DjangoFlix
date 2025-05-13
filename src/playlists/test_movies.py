from django.test import TestCase
from django.utils.text import slugify
from djangoflix.db.models import PublishStateOptions
from videos.models import Video
from .models import MovieProxy

class MovieProxyTestCase(TestCase):
    def setUp(self):
        self.video_a, self.video_b, self.video_c = self.create_videos()
        self.movie_title = 'This is my title'
        self.movie_a = MovieProxy.objects.create(title=self.movie_title, video=self.video_a)
        self.movie_a_dup = MovieProxy.objects.create(title=self.movie_title, video=self.video_a)
        self.movie_b = self.create_published_movie()

    def create_videos(self):
        return (
            Video.objects.create(title='My title', video_id='abc123'),
            Video.objects.create(title='My title', video_id='abc1233'),
            Video.objects.create(title='My title', video_id='abc1234')
        )

    def create_published_movie(self):
        movie = MovieProxy.objects.create(title='This is my title', state=PublishStateOptions.PUBLISH, video=self.video_a)
        movie.videos.set(Video.objects.all())
        movie.save()
        return movie

    def test_movie_video(self):
        self.assertEqual(self.movie_a.video, self.video_a)

    def test_movie_clip_items(self):
        self.assertEqual(self.movie_b.videos.count(), 3)

    def test_movie_slug_unique(self):
        self.assertNotEqual(self.movie_a_dup.slug, self.movie_a.slug)

    def test_slug_field(self):
        self.assertEqual(slugify(self.movie_title), self.movie_a.slug)

    def test_valid_title(self):
        self.assertTrue(MovieProxy.objects.filter(title=self.movie_title).exists())

    def test_draft_case(self):
        self.assertEqual(MovieProxy.objects.filter(state=PublishStateOptions.DRAFT).count(), 2)

    def test_publish_manager(self):
        published_qs = MovieProxy.objects.published()
        self.assertTrue(published_qs.exists())
        self.assertEqual(published_qs.count(), 1)
