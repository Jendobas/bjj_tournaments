from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import random
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from myapp.models import Quotes
from .forms import TutorForm
import time

headers = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"}

cities = {
    'Волгоград': ['Волгоград', 'Volgograd'],
    'Воронеж': ['Воронеж', 'Voronej', 'Voronezh'],
    'Казань': ['Казань', 'Kazan'],
    'Кемерово': ['Кемерово', 'Kemerovo'],
    'Краснодар': ['Краснодар', 'Krasnodar'],
    'Красногорск': ['Москва', 'Красногорск', 'Moscow'],
    'Москва': ['Москва', 'Красногорск', 'Moscow'],
    'Новосибирск': ['Новосибирск', 'Novosibirsk'],
    'Ростов-на-Дону': ['Ростов-на-Дону', 'Rostov-na-Donu', 'Rostov-na-Dony'],
    'Санкт-Петербург': ['Санкт-Петербург', 'Санкт Петербург', 'Saint Petersburg'],
    'Самара': ['Самара', 'Samara'],
    'Тверь': ['Тверь', 'Tver'],
    'Уфа': ['Уфа', 'Ufa'],
    'Хабаровск': ['Хабаровск', 'Habarovsk'],
    'Ярославль': ['Ярославль', 'Yaroslavl']
}


def index_page(request):
    url = 'https://vk.com/everydaydanaher'
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')  # получаем обработанный html код страницы
    data = soup.find_all('div', class_='wall_post_text')

    for i in data:
        name = i.text
        Quotes.objects.create(quote=name)
    for quote in Quotes.objects.values_list('quote', flat=True).distinct():  # удаляем дубликаты из бд
        Quotes.objects.filter(pk__in=Quotes.objects.filter(quote=quote).values_list('id', flat=True)[1:]).delete()

    quotes = Quotes.objects.all()
    quote_random = random.choice(quotes)

    return render(request, 'myapp/index.html', {'context': quote_random})


def tutor_page(request):
    if request.method == 'POST':
        resp = request.POST['city_form']
        city = cities[resp]
        context = {}
        urls = ['https://shakasports.com/bjj', 'https://ajptour.com/en/federation/1/events',
                'https://acbjj.smoothcomp.com/en/federation/2/events/upcoming']

        for url in urls:
            resp_tutor = requests.get(url, headers=headers)
            soup_tutor = BeautifulSoup(resp_tutor.text, 'lxml')

            if 'shakasports' in url:
                name = soup_tutor.find_all('div', class_='col-sm-6 col-lg-3')
            elif 'ajptour' in url:
                name = soup_tutor.find_all('p', class_='muted margin-bottom-xs-8')
            elif 'acbjj' in url:
                options = Options()
                options.headless = True
                driver = webdriver.Chrome(options=options)

                driver.get(url)
                time.sleep(1)
                name = driver.find_elements(By.CSS_SELECTOR, '.panel-body')

            for c in city:
                for i in name:
                    if c in i.text:
                        context[i.text] = url

        if len(context):
            return render(request, 'myapp/resp.html', {'context': context})
        else:
            return render(request, 'myapp/zero_tutor.html', {'context': resp})

    form = TutorForm()
    return render(request, 'myapp/tutor.html', {'form': form})
