from django.contrib import admin

from .models import Bookmark, BookmarkFolder
# Register your models here.


admin.site.register(Bookmark)
admin.site.register(BookmarkFolder)