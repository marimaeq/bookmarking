from django.db import models
from django.urls import reverse


# class Element(models.Model):
#     # by default, root folder
#     folder = models.ForeignKey(BookmarkFolder, on_delete=models.SET_NULL)     # change me
#     name = models.CharField(max_length=50, blank=True)


class FolderManager(models.Manager):
    # closes all folders
    def close_all(self):
        self.update(opened=False)

    def untitled_folders(self):
        return self.filter(name__contains="Untitled")


class BookmarkFolder(models.Model):
    name = models.CharField(max_length=50, blank=True, unique=True)
    opened = models.BooleanField(default=False)
    # folder = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)

    objects = FolderManager()

    def get_bookmarks_url(self):
        kwargs = {
            'id': self.id,
        }
        return reverse("bookmarks:hx-folder-bookmarks", kwargs=kwargs)

    def get_update_url(self):
        return reverse("bookmarks:hx-folder-update", kwargs={'id': self.id})
    
    # def get_create_url(self):
    #     return reverse("bookmarks:hx-folder-create", kwargs={})
    
    def get_status(self):
        # i think it changes opened's value on given instance
        self.opened = not(self.opened)
        self.save()
        return not(self.opened)

    def new_folder_name(self):
        qs = self._meta.model.objects.untitled_folders()
        untitles = [obj.name for obj in qs]
        if "Untitled" not in untitles:
            return "Untitled"
        else:
            count = 1
            name = f"Untitled {count}"
            while name in untitles:
                count += 1
                name = f"Untitled {count}"
            return name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.new_folder_name()
        print(f"folder's name is {self.name}")
        super().save()
    
    def __str__(self, *args, **kwargs):
        return self.name


class Bookmark(models.Model):
    folder = models.ForeignKey(BookmarkFolder, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50)
    url = models.URLField()
    # favicon
    # date: created, last opened

    def __str__(self):
        return self.name