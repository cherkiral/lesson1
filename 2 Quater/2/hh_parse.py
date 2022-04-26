import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

def parse_hh():
    base_url = 'https://api.hh.ru/vacancies'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                                            Chrome/98.0.4758.132 YaBrowser/22.3.1.892 Yowser/2.5 Safari/537.36',
    }

    pages_count = input('Введите количество страниц для парсинга:\n')
    search_text = input('Введите слова для поиска\n')

    info_list = []

    for i in range(int(pages_count)):
        params = {
            'text': search_text,
            'page': i
        }
        responce = requests.get(base_url, headers=headers, params=params)
        for i in range(responce.json()['per_page']):
            vacancy_name = responce.json()['items'][i]['name']
            vacancy_url = responce.json()['items'][i]['alternate_url']
            website_name = 'HeadHunter'
            try:
                salary_min = responce.json()['items'][i]['salary']['from']
            except TypeError:
                salary_min = ''
            try:
                salary_max = responce.json()['items'][i]['salary']['to']
            except TypeError:
                salary_max = ''
            try:
                currency = responce.json()['items'][i]['salary']['currency']
            except TypeError:
                currency = ''

            information = {
                'vacancy_name': vacancy_name,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'currency': currency,
                'vacancy_url': vacancy_url,
                'website_name': website_name,
            }

            info_list.append(information)
    while True:
        choise = input('Выберите как сохранить информацию:\n1)В файл\n2)Вывод\n')
        if int(choise) == 1:
            file_name = input('Введите название файла:\n')
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(info_list, f)
            break

        if int(choise) == 2:
            for i in info_list:
                print(f"Сайт: {i['website_name']}\nНазвание вакансии: {i['vacancy_name']}\n"
                      f"Минимальная зарплата: {i['salary_min']} {i['currency']}\nМаксимальная зарплата:"
                      f" {i['salary_max']} {i['currency']}\nСсылка на вакансию: {i['vacancy_url']}\n")
            break
        else:
            print('Вы ввели неверные данные')


if __name__ == '__main__':
    # parse_hh()
    with open('utf.txt', encoding='utf-8') as f:
        print(f.read())