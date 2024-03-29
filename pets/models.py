from django.db import models
from django.conf import settings
from django.utils import timezone

import uuid
import os

import humanize
import datetime


def path(_, filename):
    _, extension = os.path.splitext(filename)
    return settings.DEFAULT_PETS_PHOTOS_PATH.format(uuid=uuid.uuid4(), extension=extension)


class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    age = models.IntegerField(verbose_name="Age(Days)")
    photo = models.ImageField(upload_to=path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='pets', on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        choices=(
            ('r',"Adoption requested"),
            ('a',"Adoption accepted"),
        )
    )
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']

    @property
    def created_time_ago(self):
        return humanize.naturaltime(timezone.now() - self.created_on)

    @property
    def humanized_age(self):
        return humanize.precisedelta(datetime.timedelta(days=self.age))


class AdoptionRequest(models.Model):
    potintialOwner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='requests', on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, related_name='requests',
                            on_delete=models.CASCADE)
    state = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        choices=(
            ('p',"Request pending"),
            ('r',"Request rejected"),
            ('a',"Request accepted"),
        ),
        default="p",
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.potintialOwner} is requesting to adopt {self.pet}'

    class Meta:
        ordering = ['-created_on']

    @property
    def created_time_ago(self):
        return humanize.naturaltime(timezone.now() - self.created_on)
    
    def request_adoption(user, pet):
        adoption_request = AdoptionRequest(potintialOwner=user,pet_id=pet)
        adoption_request.save()
        pet = Pet.objects.get(pk=pet)
        pet.state = 'r'
        pet.save()

    def accept_request(pk):
        adoption_request = AdoptionRequest.objects.get(pk=pk)
        adoption_request.state = 'a'
        adoption_request.save()
        adoption_request.pet.state = 'a'
        adoption_request.pet.save()

    def reject_request(pk):
        adoption_request = AdoptionRequest.objects.get(pk=pk)
        adoption_request.state = 'r'
        adoption_request.save()
        adoption_request.pet.state = None
        adoption_request.pet.save()