from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import ListView, FormView, UpdateView
from .models import BookmarkFolder
from .forms import FolderForm

# Create your views here.


class BookmarkList(ListView):
    model = BookmarkFolder
    template_name = 'bookmarks/list.html'

    def get(self, request, *args, **kwargs):
        self.model.objects.close_all()
        return super().get(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        context['create_folder_url'] = reverse("bookmarks:hx-folder-create", kwargs={})
        return context


class HXFolderBookmarksView(ListView):
    """
    accepts only hx-get requests
    returns template of bookmarks to given folder
    """
    template_name = "bookmarks/partials/bookmark-list.html"
    folder_obj = None

    def get(self, request, id):
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


class HXFolderUpdateView(UpdateView):
    """
    Handles form for folder editing
    """
    model = BookmarkFolder
    form_class = FolderForm
    pk_url_kwarg = "id"     # pk
    template_name = "bookmarks/partials/folder-form.html"
    context_object_name = "obj"

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'name': self.object.name})
        return initial

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data()
        return render(self.request, "bookmarks/partials/folder-element.html", context=context)


class HXFolderCreateView(View):
    """
    creates Untitled folder to pass to edit form
    only htmx post request
    """

    def post(self, request):
        print("hxfoldercreateview.post called!!!")
        if not request.htmx:
            return HttpResponse("only for htmx post requests!!!")

        obj = BookmarkFolder.objects.create()
        context = {
            'obj': obj,
        }
        return render(request, "bookmarks/partials/mid-create-edit.html", context=context)    