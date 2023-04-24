from django.urls import path
from .views import (
    HomeView,
    HXBookmarkFolderContent,
    HXFolderCreateView,
    HXFolderUpdateView,
)

app_name = 'bookmarks'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('hx/folder-content/', HXBookmarkFolderContent.as_view(), name="main-folder-content"),   
    path('hx/folder-content/<int:id>/', HXBookmarkFolderContent.as_view(), name="folder-content"),
    path('hx/folder-create/', HXFolderCreateView.as_view(), name="hx-folder-create"),
    path('hx/<int:id>/folder-update/', HXFolderUpdateView.as_view(), name="hx-folder-update"),
]

"""
# main-folder-content: on the home page
# folder-content: when "Extend" clicked     
"""