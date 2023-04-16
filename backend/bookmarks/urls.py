from django.urls import path
from .views import (
    BookmarkList,
    HXFolderBookmarksView,
    HXFolderCreateView,
    HXFolderUpdateView,
)

app_name = 'bookmarks'

urlpatterns = [
    path('', BookmarkList.as_view(), name="folder-list"),
    path('hx/folder-create/', HXFolderCreateView.as_view(), name="hx-folder-create"),
    path('hx/<int:id>/bookmarks', HXFolderBookmarksView.as_view(), name="hx-folder-bookmarks"),
    path('hx/<int:id>/folder-update/', HXFolderUpdateView.as_view(), name="hx-folder-update"),
]