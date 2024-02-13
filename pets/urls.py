from django.urls import path
from .views import PetCreateView, PetListView, request_adoption, adoption_requests, adoption_request_accept, adoption_request_reject
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

app_name = "pets"
urlpatterns = [
    path("add/", login_required(PetCreateView.as_view()), name="pet-add"),
    path("list/", login_required(PetListView.as_view()), name="pet-list"),
    path("requests/", csrf_exempt(adoption_requests), name="requests"),
    path("request/<pk>/accept/",
         csrf_exempt(adoption_request_accept), name="request-accept"),
    path("request/<pk>/reject/",
         csrf_exempt(adoption_request_reject), name="request-reject"),
    path("<pk>/", csrf_exempt(request_adoption), name="request"),
]
