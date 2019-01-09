from django.forms import ModelForm,Textarea, DateInput
from time_line.models import Post

    # titulo =  models.CharField('Titulo', max_length=128, null=False, blank=False)
#     resumo = models.CharField('Resumo', max_length=10000, null=False, blank=False)
#     tags = models.CharField('Palavra_chave', max_length=255, null=True, blank=True)
#     autor = models.ForeignKey(Perfil, null=False, blank=False, on_delete=models.CASCADE, related_name='posts')
#     curtidas = models.ManyToManyField(Perfil, related_name='posts_curtidos')
#     foto = models.ImageField('Foto', upload_to='imagens/%Y/',null=True,blank=True)
class PostModelForm(ModelForm):

    class Meta:
        model = Post
        fields = ('resumo',)
        widgets = {
            'resumo': Textarea(attrs={'cols': 80, 'rows': 20}),
        }


    # def clean(self):
    #
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get("title")
    #     text = cleaned_data.get("text")
    #
    #     if title and text:
    #         if self.data['title'].__str__().__contains__('sex'):
    #             msg = "Palavras de cunho sexual não podem aparecer no titulo"
    #             self.add_error('title', msg)
    #         if self.data['text'].__str__().__contains__('sex'):
    #             msg = "Palavras de cunho sexual não podem aparecer no corpo do texto"
    #             self.add_error('text', msg)

