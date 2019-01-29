from .models import Justificativa
from django.forms import ModelForm,Textarea, DateInput

class JusificativaForm(ModelForm):

    class Meta:

        model = Justificativa
        fields = ('descricao',)
        widgets = {
            'descricao': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


