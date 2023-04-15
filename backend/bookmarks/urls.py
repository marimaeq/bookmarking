from django.urls import path
from .views import (
    BookmarkList,
    HXFolderBookmarksView,
    HXFolderCreateUpdateView,
)

app_name = 'bookmarks'

urlpatterns = [
    path('', BookmarkList.as_view(), name="folder-list"),
    path('hx/<int:id>/bookmarks', HXFolderBookmarksView.as_view(), name="hx-folder-bookmarks"),
    path('hx/<int:id>/folder-create-update/', HXFolderCreateUpdateView.as_view(), name="hx-folder-create-update"),
]