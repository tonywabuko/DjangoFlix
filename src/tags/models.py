from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.signals import pre_save

# Tagged Item Manager for handling tags
class TaggedItemManager(models.Manager):
    def unique_list(self):
        tags_set = set(self.get_queryset().values_list('tag', flat=True))
        tags_list = sorted(list(tags_set))
        return tags_list

# Tagged Item Model
class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = TaggedItemManager()

    @property
    def slug(self):
        return self.tag

# Genre Model
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.ManyToManyField(Genre)  # Linking Genre to Movies
    description = models.TextField()
    release_date = models.DateField()

    def __str__(self):
        return self.title

# Recommendation Function (based on genres)
def recommend_movies(user):
    # Get movies the user has watched (assuming watched_movies is a relationship)
    watched_movies = user.watched_movies.all()
    
    # Get genres of watched movies
    watched_genres = Genre.objects.filter(movie__in=watched_movies)
    
    # Recommend movies of the same genres, excluding already watched movies
    recommended_movies = Movie.objects.filter(genre__in=watched_genres).exclude(id__in=watched_movies)
    
    return recommended_movies

# Signal for lowercase tags
def lowercase_tag_pre_save(sender, instance, *args, **kwargs):
    instance.tag = f"{instance.tag}".lower()

pre_save.connect(lowercase_tag_pre_save, sender=TaggedItem)
