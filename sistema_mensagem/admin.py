from django.contrib import admin

from .models import Dono, Especie, Pet, Vacina, Vacinacao

# Register your models here.

admin.site.register(Dono)
admin.site.register(Especie)
admin.site.register(Pet) 
admin.site.register(Vacina)
admin.site.register(Vacinacao)