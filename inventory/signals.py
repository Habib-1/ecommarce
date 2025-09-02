from django.db.models.signals import post_save
from django.dispatch import receiver
from .services import stock_update
from .models import StockLog

@receiver(post_save,sender=StockLog)
def create_stockLog(sender,instance,created,**kwargs):
    if created:
        stock_update(
            product=instance.product,
            change_type=instance.change_type,
            quantity=instance.quantity,
            note=instance.note,
            flag=False,
        )