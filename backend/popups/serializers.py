from rest_framework import serializers
from .models import Popup


class PopupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Popup
        fields = ["id", "title", "message", "image", "link_url",
                  "auto_close_seconds", "delay_seconds"]