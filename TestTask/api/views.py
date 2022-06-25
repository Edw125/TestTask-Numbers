import datetime
import os

import requests

import xml.etree.ElementTree as xml

from django.shortcuts import render

from .models import Order

from sitemessage.shortcuts import schedule_telegram_message
from sitemessage.messengers.telegram import TelegramMessenger
from sitemessage.utils import register_messenger_objects


register_messenger_objects(TelegramMessenger(os.getenv('BOT_TOKEN')))


def index(request):
    template = 'api/index.html'
    title = 'Numbers'
    text = 'Добро пожаловать на главную страницу'
    # Синхронизация при запросе, можно отключить, так как есть регулярный таск
    Order.sync_sheet()
    orders = Order.objects.all()
    objects_iteration(orders)
    # -------------------
    context = {
        'user': request.user,
        'title': title,
        'text': text,
        'page_obj': orders,
    }
    return render(request, template, context)


def objects_iteration(orders):
    result = orders.values()
    last_value = 0
    for row in result:
        xml_obj = xml_parse(row)
        if len(xml_obj):
            price_rub = xml_obj[0].find('Value').text
            last_value = round(row['price_usd'] * string_to_float(price_rub), 2)
        Order.objects.filter(number=row['number']).update(price_rub=last_value)
        date = datetime.date.today().strftime('%d.%m.%Y')
        if row['delivery_period'] < date:
            send_message()


def string_to_float(string):
    result = string.replace(',', '.')
    return float(result)


def xml_parse(row):
    date = row['delivery_period'].split('.')
    api_url = f'https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=' \
              f'{date[0]}/{date[1]}/{date[2]}&date_req2={date[0]}/{date[1]}/{date[2]}&VAL_NM_RQ=R01235'
    response = requests.get(api_url).content
    tree = xml.fromstring(response)
    return tree


def send_message():
    schedule_telegram_message('Срок поставки нарушен', os.getenv('TELEGRAM_ID'))
