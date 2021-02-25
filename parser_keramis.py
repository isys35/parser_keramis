import requests
from bs4 import BeautifulSoup
from typing import List
import db

HOST = 'https://www.keramis.com.ua'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'
}


def save_page(response: str, file_name='page.html'):
    """
    Сохранение ответа на завпрос в html файл
    """
    with open(file_name, 'w', encoding='utf-8') as html_file:
        html_file.write(response)


def get_response(url: str) -> str:
    """
    Получение ответа на запрос
    """
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print('[ERROR] Response status code: {}'.format(response.status_code))


def parse_products(response: str) -> List[str]:
    """
    Парсинг ссылок на товары
    """
    soup = BeautifulSoup(response, 'lxml')
    product_titles = soup.select('.prd-title')
    if not product_titles:
        return []
    else:
        urls = [HOST + product_title.select_one('a')['href'] for product_title in product_titles]
        return urls


def parse_max_page(response: str) -> int:
    """
    Парсинг макимальной страницы в категории
    """
    soup = BeautifulSoup(response, 'lxml')
    nav = soup.select_one('.nav.bottom')
    if nav:
        max_page = int(nav.select('a')[-2].text)
        return max_page
    else:
        return 1


def parse_sub_categories(response: str) -> List[str]:
    """
    Парсинг ссылок на подкатегории из ответа на запрос
    """
    soup = BeautifulSoup(response, 'lxml')
    menu = soup.select_one('.menu-line')
    ul = menu.select_one('ul')
    urls = []
    for li in ul.select('div.sub_sub_cat_bl'):
        urls.append(HOST + li.select_one('a')['href'])
    return urls


def parse_product(response: str) -> dict:
    """
    Парсинг данных продукта
    """
    soup = BeautifulSoup(response, 'lxml')
    name = soup.select_one('h1').text
    price = soup.select_one('.totalPrice').text
    description = soup.select_one('.description_block_content').text.strip()
    soup_params = soup.select_one('.cpt_product_params_selectable')
    characteristiks = []
    trs = soup_params.select('tr')
    for tr in trs:
        characteristiks.append(tr.text.strip().replace('\n', ''))
    main_photo = HOST + soup.select_one('#main_image')['src']
    additional_photo = [HOST + el['data-link'] for el in soup.select('a.product-thumb')]
    photos = additional_photo + [main_photo]
    data = {'name': name,
            'price': price,
            'description': description,
            'photos': photos,
            'characteristiks': characteristiks}
    print(data)
    return data


def get_sub_categories() -> List[str]:
    """
    Получение ссылок на подкатегории с сайта
    """
    response = get_response(HOST)
    sub_categories = parse_sub_categories(response)
    return sub_categories


def get_urls_products(sub_category_url: str) -> List[str]:
    """
    Получение ссылок на продукты из категории
    """
    print(f'[INFO] Получение ссылок на продукты из категории {sub_category_url}')
    response = get_response(sub_category_url)
    max_page = parse_max_page(response)
    products = parse_products(response)
    if max_page > 1:
        for page in range(2, max_page + 1):
            print(f'[INFO] Страница {page}/{max_page}')
            url_page = sub_category_url + f'?page={page}'
            response_page = get_response(url_page)
            products_from_page = parse_products(response_page)
            products.extend(products_from_page)
    return products


def get_product_data(product_url: str) -> dict:
    """
    Получение данных о продукте
    """
    print(f'[INFO] Получение данных о продукте {product_url}')
    response = get_response(product_url)
    product_data = parse_product(response)
    product_data['url'] = product_url
    return product_data


def parser_1():
    """
    Первый режим работы парсера
    """
    db.create_data_file()
    categories_urls = get_sub_categories()
    for categorie_url in categories_urls:
        products_urls = get_urls_products(categorie_url)
        for product_url in products_urls:
            product_data = get_product_data(product_url)
            db.add_data(product_data)


if __name__ == '__main__':
    parser_1()
