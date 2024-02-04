from django.contrib import admin
from .models import Pet,AdoptionRequest

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "humanized_age", "owner")

@admin.register(AdoptionRequest) 
class AdoptionRequest(admin.ModelAdmin):
    list_display = ("pet", "potintialOwner", "created_time_ago")