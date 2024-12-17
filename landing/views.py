from django.http import HttpResponseRedirect
from django.urls import reverse

def redirect(response):
    return HttpResponseRedirect(reverse("work_space:index"))
