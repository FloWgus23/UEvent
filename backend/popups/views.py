from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Popup
from .serializers import PopupSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def active_popups(request):
    popups = Popup.live().order_by("-created_at")
    return Response(PopupSerializer(popups, many=True, context={"request": request}).data)


@api_view(["GET"])
@permission_classes([AllowAny])
def preview_popup(request, token):
    popup = get_object_or_404(Popup, preview_token=token)
    return Response(PopupSerializer(popup, context={"request": request}).data)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def active_popups(request):
    ...

@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def preview_popup(request, token):
    ...    