from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Cuenta(models.Model):
    ROL_CHOICES = [
        ("donante", "Donante"),
        ("beneficiario", "Beneficiario"),
        ("admin", "Administrador"),
        ("voluntario", "Voluntario"),
    ]

    rut = models.CharField(max_length=12, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="donante")
    telefono = models.CharField(max_length=20, blank=True, default="")
    direccion = models.TextField(blank=True, default="")
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    class Meta:
        db_table = "cuentas"
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
