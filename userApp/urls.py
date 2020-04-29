from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.uhome),
    path('firformpage/',views.firformpage),
    path('complaintformpage/',views.complaintformpage),
    path('userdetails/',views.userdetails),
    path('firsession/',views.firsession),
    path('userfirview/',views.userfirview),
    path('deletefir/<int:id>/',views.deletefir,name='deletefir'),
    path('uviewfir/<int:id>/',views.uviewfir,name='uviewfir'),
]
