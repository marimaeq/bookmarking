from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import ListView
from .models import BookmarkFolder

# Create your views here.


class BookmarkList(ListView):
    model = BookmarkFolder
    template_name = 'bookmarks/list.html'

    # def get(self, request):
    #     print(self.model._meta.app_label)
    #     return super().get(request)


class HXFolderBookmarksView(View):
    """
    accepts only hx-get requests
    returns template of bookmarks to given folder
    """
    model = BookmarkFolder

    def get(self, request, id):
        if not request.htmx:
            return HttpResponse("Page not found.")
        obj = self.get_folder(id)
        if obj is None:
            return HttpResponse("Folder not found.")

        
        print('hello world')
        return HttpResponse("htmx working!", headers=headers)

    def get_folder(self, id)
        try:
            obj = BookmarkFolder.objects.get(id=id)
        except:
            obj = None
        return obj

    def get_queryset(self):


    

    