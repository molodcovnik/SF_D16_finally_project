from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea

from .models import Item, Reply


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            # 'user',
            'header',
            'description',
            'category',
            'image',
            'video',
        ]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
             'text',
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows': 3})
