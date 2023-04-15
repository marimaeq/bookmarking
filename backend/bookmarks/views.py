from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import ListView
from .models import BookmarkFolder
from .forms import FolderForm

# Create your views here.


class BookmarkList(ListView):
    model = BookmarkFolder
    template_name = 'bookmarks/list.html'

    def get(self, request, *args, **kwargs):
        print("bookmarklistview called!")
        self.model.objects.close_all()
        return super().get(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['create_update_folder_url'] = \
                reverse("bookmarks:hx-folder-create-update", kwargs={'id': 0})
                # kwargs={'id': None}, but you can't pass None(or even -1)
                # probably because of <int:id>   (only positive integers)
        return context


class HXFolderBookmarksView(ListView):
    """
    accepts only hx-get requests
    returns template of bookmarks to given folder
    """
    template_name = "bookmarks/partials/bookmark-list.html"
    folder_obj = None

    def get(self, request, id):
        # print("hxfolderbookmarksview called!!!")
        if not request.htmx:
            return HttpResponse("Page not found.")

        self.object_list = self.get_queryset(id=id)
        context = self.get_context_data()
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['opened'] = self.folder_obj.get_status()
        print(context['opened'])
        return context

    def get_queryset(self, **kwargs):
        id = kwargs.get('id')
        try:
            self.folder_obj = obj = BookmarkFolder.objects.get(id=id)
        except:
            obj = None
        if obj is None:
            return HttpResponse("Folder not found.")
        return obj.bookmark_set.all()


class HXFolderCreateUpdateView(View):
    # get
    # creates folder with "Untitled #number" name
    # and returns template with form for folder editin
    # post
    # handle post request from folder-edit form

    # template_name = "partials/...folder-edit.html"
    model = BookmarkFolder

    def get(self, request, id):
        print("hxfoldercreateupdateview called!!!")
        if not request.htmx:
            return HttpResponse('Only htmx requests, id should be None when creating!!!')

        # untitled folder
        obj = BookmarkFolder.objects.create()
        form = FolderForm(initial={'name': obj.name})
        context = self.get_context_data(obj=obj, form=form)
        return render(request, "bookmarks/partials/folder-edit-form.html", context=context)
        # return HttpResponse("TEST TRY")

    def get_context_data(self, **kwargs):
        return kwargs

    def post(self, request, id):
        print("hxfoldercreateupdateview.post called!!!")
        if not request.htmx:
            return HttpResponse('Only htmx requests allowed!!!')
        form = FolderForm(request.POST)
        obj = BookmarkFolder.objects.get(id=id)
        if form.is_valid():
            # print(form.cleaned_data)
            # print(dir(obj))
            obj.name = form.cleaned_data.get('name')
            obj.save()
            return 

        return HttpResponse("TEST TRY")