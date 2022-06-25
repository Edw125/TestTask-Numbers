import os
from django.db import models

from gsheets import mixins
from uuid import uuid4


class Order(mixins.SheetSyncableMixin, models.Model):
    spreadsheet_id = os.getenv('SPREADSHEET_ID')
    model_id_field = 'number'
    sheet_name = 'Sheet1'
    sheet_id_field = 'number'

    number = models.IntegerField(primary_key=True)
    order_name = models.CharField('Name', max_length=200)
    price_usd = models.IntegerField()
    price_rub = models.FloatField(blank=True, null=True)
    delivery_period = models.CharField('Date', max_length=200)

    def __str__(self):
        return f'{self.number} {self.order_name} {self.price_usd} {self.delivery_period}'
