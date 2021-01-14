from django.db import models

class Order(models.Model):  
    order_id = models.CharField(max_length=20)  
    marketplace = models.CharField(max_length=100)  
    amount = models.FloatField()
    currency = models.CharField(max_length=10, blank=True, null=True)
    marketplace_status = models.CharField(max_length=30)
    lengow_status = models.CharField(max_length=30, blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    class Meta:  
        db_table = "orders"  
