from django import forms
from .models import Image, Property, Advertising, Category


class NewAdForm(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = ['title', 'description', 'category']


class ImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = Image
        fields = ('image',)


class AddPropsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(AddPropsForm, self).__init__(*args, **kwargs)
        for title in extra:
            self.fields[f'custom_{title}'] = forms.CharField(label=title)

    def get_values(self):
        for name, value in self.cleaned_data.items():
            if name.startswith('custom_'):
                yield (self.fields[name].label, value)
