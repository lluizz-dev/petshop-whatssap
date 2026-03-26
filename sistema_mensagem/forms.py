from django import forms
from .models import Dono, Especie, Pet, Vacina, Vacinacao

class DonoForm(forms.ModelForm):
    class Meta:
        model = Dono
        fields = ['nome', 'email', 'telefone']
        
class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = ['nome', 'emojis']
        
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nome', 'especie', 'dono']


class VacinaForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = ['nome', 'periodicidade_dias']


class VacinacaoForm(forms.ModelForm):
    class Meta:
        model = Vacinacao
        fields = ['pet', 'vacina', 'data_aplicada']