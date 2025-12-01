# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Dht11

def dashboard(request):
    # Rend juste la page; les données sont chargées via JS
    return render(request, "dashboard.html")

def latest_json(request):
    # Fournit la dernière mesure en JSON (sans passer par api.py)
    last = Dht11.objects.order_by('-dt').values('temp', 'hum', 'dt').first()
    if not last:
        return JsonResponse({"detail": "no data"}, status=404)
    return JsonResponse({
        "temperature": last["temp"],
        "humidity":    last["hum"],
        "timestamp":   last["dt"].isoformat()
    })

    # Dans votre fichier views.py, ajoutez ces imports si vous ne les avez pas déjà
from rest_framework import generics
from .models import Dht11  # Assurez-vous que c'est le bon nom de modèle
from .serializers import DHT11serialize # Assurez-vous que c'est le bon nom de serializer

# ... gardez votre code existant (Dlist, Dhtviews) ...

# NOUVELLE VUE POUR LE DASHBOARD
class LatestMesureListAPIView(generics.ListAPIView):
    """
    API endpoint qui renvoie les dernières mesures pour le dashboard.
    """
    # On récupère tous les objets, triés par date décroissante (le plus récent en premier)
    queryset = Dht11.objects.all().order_by('-dt') 
    serializer_class = DHT11serialize

    
# NOUVELLE VUE POUR AFFICHER LA PAGE HTML
def dashboard_view(request):
    return render(request, 'dashboard.html')


  
class Dhtviews(generics.ListCreateAPIView):
    queryset = Dht11.objects.all().order_by('-dt')
    serializer_class = DHT11serialize


