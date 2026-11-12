from django.urls import path
from . import views

urlpatterns = [
    path("active/", views.active_popups),
    path("preview/<uuid:token>/", views.preview_popup),
]