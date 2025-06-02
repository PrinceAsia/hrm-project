from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkPlacesViewSet, WorkingHoursCreateView, WorkingHoursDeleteView

router = DefaultRouter()
router.register('places', WorkPlacesViewSet, basename='workplaces')

urlpatterns = [
    path('', include(router.urls)),
    path('hours/create/', WorkingHoursCreateView.as_view(), name='workinghours-create'),
    path('hours/delete/<int:pk>/', WorkingHoursDeleteView.as_view(), name='workinghours-delete'),
]
