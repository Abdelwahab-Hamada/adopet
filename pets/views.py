from django.views.generic import ListView, DetailView
from .models import Pet, AdoptionRequest
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView


class PetCreateView(CreateView):
    model=Pet
    fields=["name", "age", "photo"]
    success_url = reverse_lazy('pets:pet-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PetListView(ListView):
    model=Pet
    context_object_name = "pet_list"

@login_required
def request_adoption(request, pk):
    AdoptionRequest.request_adoption(user=request.user, pet=pk)
    return HttpResponse("<div class='requested'>requested</div>")

@login_required
def adoption_requests(request):
    adoption_requests = AdoptionRequest.objects.filter(pet__owner=request.user, state='p')
    adoption_requests_html = ""

    if adoption_requests.count() > 0:
        for req in adoption_requests:
            adoption_requests_html += f"""
                <div id="req-{req.id}" class='request-line'>
                    <span class="request-text">{req}</span>
                    <span id="a-{req.id}" hx-post="{ reverse('pets:request-accept', kwargs={'pk':req.id}) }" hx-trigger="click" hx-target="#req-{req.id}" hx-swap="outerHTML" class="btn-accept">Accept</span>
                    <span id="r-{req.id}" hx-post="{ reverse('pets:request-reject', kwargs={'pk':req.id}) }" hx-trigger="click" hx-target="#req-{req.id}" hx-swap="outerHTML" class="btn-reject">Reject</span>
                </div>
            """
    else:
        adoption_requests_html = """
            <div class='request-line'>
                <div class="request-text">
                    No requests
                </div>
            </div>
        """
    response = f"""
                <div id="requests" class="requests">
                    {adoption_requests_html}
                </div>
                """
    return HttpResponse(response)

@login_required
def adoption_request_accept(request, pk):
    AdoptionRequest.accept_request(pk)
    return HttpResponse("")

@login_required
def adoption_request_reject(request, pk):
    AdoptionRequest.reject_request(pk)
    return HttpResponse("")