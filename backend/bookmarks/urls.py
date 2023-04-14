from django.urls import path
from .views import (
    BookmarkList,
    HXFolderBookmarksView,
)

app_name = 'bookmarks'

urlpatterns = [
    path('', BookmarkList.as_view(), name="folder-list"),
     path('hx/<int:id>/bookmarks', HXFolderBookmarksView.as_view(), name="hx-folder-bookmarks"),
]