from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.phome),
    path('policedetails/',views.policedetails),
    path('policefirview/',views.policefirview),
    path('viewfir/<int:id>/',views.viewfir),
]
