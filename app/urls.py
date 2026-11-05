from django.urls import path
from .views import * 


urlpatterns = [
   path("become-partner/", become_partner, name="become_partner"),
   path("contact/", contact, name="contact"),
]
