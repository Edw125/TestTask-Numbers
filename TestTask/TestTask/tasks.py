from api.views import objects_iteration
from .celery import app
from api.models import Order


@app.task
def update_gsheet():
    Order.sync_sheet()
    objects_iteration(Order.objects.all())



