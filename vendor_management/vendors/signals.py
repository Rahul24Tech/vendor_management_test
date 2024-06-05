from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder
from .views import PurchaseOrderViewSet

@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    PurchaseOrderViewSet().update_vendor_metrics(instance.vendor_id)
