from bs4 import BeautifulSoup
import csv
import json
import requests
from datetime import datetime


def get_w_csv(id_descr=None, file_name=None, data=None, name=None, price=None,
              csv_=True):  # Запись списков в csv файл или JSON. Можно модифицировать.

    if csv_ == False:

        result_json = [{f'{file_name}':{**data}}]

        with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(result_json, file, indent=4, ensure_ascii=False)

        return print(f'Файл {file_name}.json создан')


    with open(f'{file_name}.csv', 'w', encoding='utf-8-sig', newline='') as file:

        for descr, n in data:
            flatten_line = descr, float(n)

            file = open(f'{file_name}.csv', 'a', encoding='utf-8-sig', newline='')
            writer = csv.writer(file, delimiter=';')
            writer.writerow(flatten_line)
        file.close()
    return print(f'Файл {file_name}.csv создан')


# Парсим таблицу по дате и названию компании сайта finance.yahoo.com
# на выходе получаем архив списков с датой и данными столбца Adj Close
# По умолчанию от старых к новым данным (Можем изменить указав revers=True)
# Имя Компании и дату (в формате ['YYYY-12-DD','YYYY-09-DD','YYYY-06-DD','YYYY-01-DD'],для данных за год)
# указывать обязательно.


def get_parse_fin_table(url='/', lst_date=None, name=None, revers=None):

    lst_date_unix = ([datetime(*[int(i) for i in d.split('-')]).timestamp() for d in lst_date])
    lst_date_unix = [int(str(i).replace('.0', '')) for i in lst_date_unix]

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    url_date_1_yer = []
    for i in range(len(lst_date_unix) - 1):
        url = f'https://finance.yahoo.com/quote/{name}/history?period1={lst_date_unix[i + 1]}&period2={lst_date_unix[i]}&interval=1d'
        url_date_1_yer.append(url)
    lst_item_date = []
    lst_Adj_Close = []
    for link in url_date_1_yer:
        response = requests.get(url=link, headers=headers).text
        lst_item_date.extend(
            [i.text for i in BeautifulSoup(response, 'html.parser').find_all('td', 'Py(10px) Ta(start) Pend(10px)')])
        lst_Adj_Close.extend([float(i.text.replace(',', '')) for i in
                              BeautifulSoup(response, 'html.parser').find_all('td', 'Py(10px) Pstart(10px)')[4::6]])

    res = [*zip(lst_item_date, lst_Adj_Close)]
    if revers == True:
        res = reversed([*zip(lst_item_date, lst_Adj_Close)])
    return res


# для удобства

inderval = '1d'
# Пример Названий компаний и их имен, еще не доделано
name = {'S&P500': '%5EGSPC', 'Tesla': 'TSLA', 'Aple': 'APLE', 'Amazon': 'AMZN'}

start_year = '2021' # Для сбора данных за год указываем нужный нам год
lst_date = [f'{start_year}-12-31', f'{start_year}-09-01', f'{start_year}-06-1',
            f'{start_year}-03-01', f'{start_year}-01-02']

file_name = 'Aple' # для подписи файла

data = get_parse_fin_table(lst_date=lst_date, name='APLE',revers=True) #
data = {str(i): float(n) for i, n in data} # Преобразования полученых данных для записи в JSON формат

get_w_csv(data=data, file_name=f'{file_name}_{start_year}', csv_=False) # запись в жсон формат.