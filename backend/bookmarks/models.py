from django.db import models
from django.urls import reverse

# Create your models here.


class BookmarkFolder(models.Model):
    name = models.CharField(max_length=50)

    def get_bookmarks_url(self):
        kwargs = {
            'id': self.id,
        }
        return reverse("bookmarks:hx-folder-bookmarks", kwargs=kwargs)


class Bookmark(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField()
    # favicon

    def __str__(self):
        return self.name