from django.urls import path
from .views import PetListView, PetDetailView

app_name="pets"
urlpatterns = [
    path("list/", PetListView.as_view()),
    path("<pk>/", PetDetailView.as_view(), name="detail"),
]
