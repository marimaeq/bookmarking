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
    template_name = "bookmarks/partials/bookmark-list.html"


    def get(self, request, id):
        print("hxfolderbookmarksview called!!!")
        if not request.htmx:
            return HttpResponse("Page not found.")

        kwargs = {
            'id': id,
        }

        context = self.get_context_data(id=id)
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = kwargs.get('id')
        obj = self.get_folder(id)
        if obj is None:
            return HttpResponse("Folder not found.")
        context['queryset'] = obj.objects.all()
        return context

    def get_folder(self, id):
        try:
            obj = BookmarkFolder.objects.get(id=id)
        except:
            obj = None
        return obj



    

    