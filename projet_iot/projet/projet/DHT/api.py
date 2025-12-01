from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .utils import send_telegram  # ← Import correct depuis le même dossier
from twilio.rest import Client 


@api_view(['GET'])
def Dlist(request):
    all_data = Dht11.objects.all()
    data = DHT11serialize(all_data, many=True).data
    return Response({'data': data})

class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize

    def perform_create(self, serializer):
        instance = serializer.save()
        temp = instance.temp

        if temp > 25:
            # 1) Email (si tu veux le garder)
            try:
                send_mail(
                    subject="⚠️ Alerte Température élevée",
                    message=f"La température a atteint {temp:.1f} °C à {instance.dt}.",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=["noureddine.saadaoui.ensao@ump.ac.ma"],  # ⚠️ ton adresse
                    fail_silently=True,
                )
            except Exception:
                pass

# 2) Telegram
            msg = f"⚠️ Alerte DHT11: {temp:.1f} °C (>25) à {instance.dt}"
            send_telegram(msg)

            """
#3) WhatsApp via Twilio (sécurisé)

import os
from twilio.rest import Client

# Variables d'environnement (à définir dans Windows)
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token  = os.getenv("TWILIO_AUTH_TOKEN")

if account_sid and auth_token:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Il y a une alerte importante sur votre Capteur : la température dépasse le seuil !',
        to='whatsapp:+212644600320'
    )

    print(message.sid)
else:
    print("⚠️ TWILIO NON CONFIGURÉ : variables d'environnement manquantes.")
"""
