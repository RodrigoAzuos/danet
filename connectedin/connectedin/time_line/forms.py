from django.forms import ModelForm,Textarea, DateInput
from time_line.models import Post
from django import forms

class PostModelForm(forms.Form):

    resumo = forms.CharField(required=True)
    foto = forms.ImageField(required=False)
    tags = forms.CharField(required=False)

    # class Meta:
    #     model = Post
    #     fields = ('resumo','foto','tags',)
    #     widgets = {
    #         'resumo': Textarea(attrs={'cols': 80, 'rows': 20}),
    #     }

