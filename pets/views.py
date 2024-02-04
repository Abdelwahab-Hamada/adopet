from django.views.generic import ListView, DetailView
from .models import Pet

class PetListView(ListView):
    model=Pet
    context_object_name = "pet_list"

class PetDetailView(DetailView):
    model=Pet