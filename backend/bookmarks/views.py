from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.views import View
from django.views.generic import (
    ListView,
    FormView,
    UpdateView,
    CreateView,
)
from .models import Bookmark, BookmarkFolder
from .forms import FolderForm, BookmarkForm
from itertools import chain


# Create your views here.
class HomeView(View):
    template_name = "bookmarks/home.html"

    def get(self, request):
        context = self.get_context_data()
        return render(request, template_name=self.template_name, context=context)

    def get_context_data(self):
        context = {}
        context['create_folder_url'] = reverse("bookmarks:hx-folder-create", kwargs={})
        context['create_bookmark_url'] = reverse("bookmarks:hx-bookmark-create", kwargs={})
        context['main_folder_content_url'] = reverse("bookmarks:main-folder-content", kwargs={})
        return context


class HXBookmarkFolderContent(ListView):
    """
    Handles content on the home page
    and "Extend" functionality
    """
    template_name = 'bookmarks/partials/folder-content.html'
    folder_id = None

    def get(self, request, *args, **kwargs):
        if not request.htmx:
            return HttpResponse("htmx requests only!!!")
        self.folder_id = kwargs.get('id')
        if self.folder_id is None:
            BookmarkFolder.objects.close_all()
        return super().get(request, *args, **kwargs)

    def get_context_data(self):
        context = super().get_context_data()
        if self.folder_id is None:
            context['opened'] = False
        else:
            try:
                parent_folder = BookmarkFolder.objects.get(id=self.folder_id)
                context['opened'] = parent_folder.get_status()
            except:
                context['opened'] = False
        return context

    def get_queryset(self):
        id = self.folder_id
        f = BookmarkFolder.objects.filter(parent_folder_id=id)
        b = Bookmark.objects.filter(parent_folder_id=id)
        qs = sorted(
            list(chain(f, b)),
            key=lambda instance: instance.name.lower()
        )
        return qs


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


class HXBookmarkCreateView(CreateView):
    """
    get: Initializes form with unique Untitled name
    post: Creates a bookmark with submitted data
    """  
    form_class = BookmarkForm
    template_name = "bookmarks/partials/bookmark-form.html"     #for get

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'name': Bookmark.new_bookmark_name()})
        return initial

    def form_valid(self, form):
        self.object = form.save()
        context = {
            'object': self.object 
        }
        data = form.cleaned_data
        response = render(self.request, template_name="bookmarks/partials/bookmark-element.html", context=context)
        if data['parent_folder'] is None:
            response['HX-Reswap'] = "outerHTML"
            return response
        return response