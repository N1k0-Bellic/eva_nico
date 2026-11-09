import uuid
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='juegos')
    nombre = models.CharField(max_length=150)
    imagen_caja = models.ImageField(upload_to='cajas/', blank=True, null=True)
    precio = models.IntegerField()
    cantidad_jugadores = models.CharField(max_length=50, help_text="Ej: 2 a 4 jugadores")
    edad_minima = models.PositiveIntegerField(help_text="Edad mínima en años (ej: 10)")
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Juego"
        verbose_name_plural = "Juegos"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='pedidos')
    nombre_comprador = models.CharField(max_length=100)
    correo_comprador = models.EmailField()
    telefono_comprador = models.CharField(max_length=20)
    cantidad = models.PositiveIntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = str(uuid.uuid4()).upper()[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.codigo} - {self.juego.nombre}"