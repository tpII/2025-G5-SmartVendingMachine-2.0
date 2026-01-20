from django.db import models
from authentication.models import User

class Heladera(models.Model):
    id = models.AutoField(primary_key=True)  # ID numrico que comienza en 1
    latitud = models.DecimalField(max_digits=15, decimal_places=13)
    longitud = models.DecimalField(max_digits=15, decimal_places=13)
    en_uso = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Heladera {self.id}"

class Producto(models.Model):
    #product_id = models.PositiveIntegerField(primary_key=True)
    heladera = models.ForeignKey(Heladera, related_name='productos', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='media/productos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return self.nombre

class SesionCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    heladera = models.ForeignKey(Heladera, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Sesion de compra {self.id} de {self.usuario.username} en Heladera {self.heladera.id}"

class ProductoCompra(models.Model):
    sesion = models.ForeignKey(SesionCompra, related_name='productos', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Sesion {self.sesion.id}"
class DatosSensor(models.Model):
    temperatura = models.DecimalField(max_digits=5,decimal_places=2)
    humedad = models.DecimalField(max_digits=5, decimal_places=2)
