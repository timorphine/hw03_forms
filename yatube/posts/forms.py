from django.forms import ModelForm
from .models import Post
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text')

    def clean_text(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError(
                'Без текста будет неинтересно :('
            )
        return data
