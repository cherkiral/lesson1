import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = 'HeadHunter'
MONGO_COLLECTION = 'HH_Vacancies'

def parse_hh_to_mongo(pages_count, search_text):
    base_url = 'https://api.hh.ru/vacancies'

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                                            Chrome/98.0.4758.132 YaBrowser/22.3.1.892 Yowser/2.5 Safari/537.36',
    }

    pages_count = pages_count
    search_text = search_text

    count = 0
    for page_number in range(1, int(pages_count) + 1):
        params = {
            'text': search_text,
            'page': page_number
        }
        responce = requests.get(base_url, headers=headers, params=params)
        vac_per_page = responce.json()['per_page']
        for vacancy_number in range(vac_per_page):
            vacancy_name = responce.json()['items'][vacancy_number]['name']
            vacancy_url = responce.json()['items'][vacancy_number]['alternate_url']
            website_name = 'HeadHunter'
            try:
                salary_min = responce.json()['items'][vacancy_number]['salary']['from']
            except TypeError:
                salary_min = ''
            try:
                salary_max = responce.json()['items'][vacancy_number]['salary']['to']
            except TypeError:
                salary_max = ''
            try:
                currency = responce.json()['items'][vacancy_number]['salary']['currency']
            except TypeError:
                currency = ''

            filter_data = {
                'vacancy_name': vacancy_name,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'currency': currency,
                'vacancy_url': vacancy_url,
                'website_name': website_name,
            }

            info_for_mongo = {
                '$set' : {
                'vacancy_name': vacancy_name,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'currency': currency,
                'vacancy_url': vacancy_url,
                'website_name': website_name,
                }
            }
            with MongoClient(MONGO_HOST, MONGO_PORT) as client:
                db = client[MONGO_DB]
                hh_collection = db[MONGO_COLLECTION]
                hh_collection.update_many(filter_data, info_for_mongo, upsert=True)
        count += 1

def find_by_salary(min_salary):
    filter_data = {
        'salary_min': {'$gte': int(min_salary)}
    }
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        hh_collection = db[MONGO_COLLECTION]
        cursor = hh_collection.find(filter_data)
        for i in cursor:
            pprint(i)


if __name__ == '__main__':
    parse_hh_to_mongo(3, 'кассир')
    find_by_salary(300000)


