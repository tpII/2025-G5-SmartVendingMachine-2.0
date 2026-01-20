from django.db import models
from django.conf import settings


class CreditCard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_cards')
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
    card_holder_name = models.CharField(max_length=100)
    favourite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.card_holder_name} - {self.card_number[-4:]}"

class Compra(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="compras")
    heladera = models.ForeignKey('fridge.Heladera', on_delete=models.CASCADE, related_name="compras")
    tarjeta = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True, blank=True, related_name="compras")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Compra #{self.id} por {self.usuario.username} el {self.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')}"
