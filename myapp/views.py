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


def index_page(request):
    url = 'https://vk.com/everydaydanaher'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')  # получаем обработанный html код страницы
    data = soup.find_all('div', class_='pi_text')

    for i in data:
        name = i.text.replace('Показать ещё', '')
        if Quotes.objects.filter(Quotes.quote == name):
            continue
        else:
            Quotes.objects.create(quote=name)

    quotes = Quotes.objects.all()
    quote_random = random.choice(quotes)

    return render(request, 'myapp/index.html', {'context': quote_random})


def tutor_page(request):
    if request.method == 'POST':
        city = request.POST['city_form']
        context = {}
        urls = ['https://shakasports.com/bjj', 'https://ajptour.com/en/federation/1/events',
                'https://acbjj.smoothcomp.com/en/federation/2/events/upcoming']
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) "
                "Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)"}

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

            for i in name:
                if city in i.text:
                    context[i.text] = url

        if len(context):
            return render(request, 'myapp/resp.html', {'context': context})
        else:
            return render(request, 'myapp/zero_tutor.html', {'context': city})

    form = TutorForm()
    return render(request, 'myapp/tutor.html', {'form': form})
