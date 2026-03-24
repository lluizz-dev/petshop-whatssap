from django.contrib import admin

from .models import Dono, Pet, Vacina, Vacinacao

# Register your models here.

admin.site.register(Dono)
admin.site.register(Pet) 
admin.site.register(Vacina)
admin.site.register(Vacinacao)