from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('manager', 'Gestionnaire de stock'),
        ('viewer', 'Utilisateur simple'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du produit")
    category = models.CharField(max_length=100, verbose_name="Catégorie")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Quantité en stock")
    low_stock_threshold = models.PositiveIntegerField(default=10, verbose_name="Seuil de réapprovisionnement")

    def __str__(self):
        return self.name

    def is_low_stock(self):
        return self.quantity < self.low_stock_threshold


class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Produit")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    movement_type = models.CharField(
        max_length=10,
        choices=[('entry', 'Entrée'), ('exit', 'Sortie')],
        verbose_name="Type de mouvement"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, verbose_name="Utilisateur")

    def __str__(self):
        return f"{self.movement_type} - {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Validation du stock avant enregistrement
        if self.movement_type == 'exit' and self.quantity > self.product.quantity:
            raise ValueError("La quantité demandée est supérieure au stock disponible.")
        super().save(*args, **kwargs)


@receiver(post_save, sender=StockMovement)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if instance.movement_type == 'entry':
            product.quantity += instance.quantity
        elif instance.movement_type == 'exit':
            product.quantity -= instance.quantity
        product.save()