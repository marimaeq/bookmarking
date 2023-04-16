from django import forms
from .models import BookmarkFolder

class FolderForm(forms.ModelForm):
    class Meta:
        model = BookmarkFolder
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # print(dir(self.fields['name']))
        for field in self.fields:
            self.fields[str(field)].label = ""

    def clean_name(self):
        data = self.cleaned_data.get('name')
        qs = BookmarkFolder.objects.filter(name=data)
        # if not itself
        if not qs.exists():
            return data
        elif qs.count() == 1 and qs.get().id is self.instance.id: # Untitled name didn't change
            return data
        else:
            raise forms.ValidationError("This name is already in use.")