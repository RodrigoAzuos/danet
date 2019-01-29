from django.forms import ModelForm,Textarea, DateInput
from time_line.models import Post


class PostModelForm(ModelForm):

    class Meta:
        model = Post
        fields = ('resumo','foto',)
        widgets = {
            'resumo': Textarea(attrs={'cols': 80, 'rows': 20}),
        }

