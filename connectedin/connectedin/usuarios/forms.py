# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User



class RegistrarUsuarioForm(forms.Form):

    CHOICES_SEXO = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )


    usuario = forms.CharField(required=True)
    foto = forms.ImageField(required=False)
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    data_nascimento = forms.DateField(required=True)
    sexo = forms.ChoiceField(choices = CHOICES_SEXO, required=True)
    nome_empresa = forms.CharField(required=True)



    def is_valid(self):
        valid = True

        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        user_exists = User.objects.filter(username=self.data['usuario']).exists()
        email_exists = User.objects.filter(email=self.data['email']).exists()

        if user_exists:
            self.adiciona_erro('Usuario já existente')
            valid = False

        if email_exists:
            self.adiciona_erro('Email já existe')
            valid = False

        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)