from datetime import timedelta

from django.db import models

# Create your models here.

class Dono(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.nome
    
class Especie(models.Model):
    nome = models.CharField(max_length=50)
    emojis = models.CharField(max_length=5)

    def __str__(self):
        return self.nome


class Pet(models.Model):
    nome = models.CharField(max_length=100)
    especie = models.ForeignKey(Especie, on_delete=models.CASCADE)
    dono = models.ForeignKey(Dono, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.especie})"


class Vacina(models.Model):
    nome = models.CharField(max_length=100)
    periodicidade_dias = models.IntegerField()

    def __str__(self):
        return self.nome


class Vacinacao(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE)
    
    data_aplicada = models.DateField()
    data_proxima = models.DateField(blank=True, null=True, editable=False)
    
    notificado_3_dias = models.BooleanField(default=False)
    notificado_1_dia = models.BooleanField(default=False)
    data_notificacao_3_dias = models.DateTimeField(null=True, blank=True)
    data_notificacao_1_dia = models.DateTimeField(null=True, blank=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.data_aplicada and self.vacina:
            self.data_proxima = self.data_aplicada + timedelta(days=self.vacina.periodicidade_dias)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pet.nome} - {self.vacina.nome}"