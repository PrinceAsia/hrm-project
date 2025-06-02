from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView, CreateAPIView, ListAPIView, RetrieveAPIView

from .models import WorkPlaces, WorkingHours
from .serializers import WorkPlacesSerializer, WorkingHoursSerializer


class WorkPlacesViewSet(viewsets.ModelViewSet):
    queryset = WorkPlaces.objects.all()
    serializer_class = WorkPlacesSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkingHoursCreateView(CreateAPIView):
    queryset = WorkingHours.objects.all()
    serializer_class = WorkingHoursSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkingHoursDeleteView(DestroyAPIView):
    queryset = WorkingHours.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
