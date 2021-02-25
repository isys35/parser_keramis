import csv

CSV_FILE = 'data.csv'


def create_data_file(file_name=None):
    if file_name is None:
        file_name = CSV_FILE
    with open(file_name, "w", newline="") as file:
        csv.writer(file, delimiter=';')


def get_data_list(data: dict) -> list:
    data_list = [data['url'], data['name'], data['price'], data['description']]
    for i in range(0, 10):
        try:
            data_list.append(data['photos'][i])
        except IndexError:
            data_list.append(None)
    for i in range(0, 20):
        try:
            data_list.append(data['characteristiks'][i])
        except IndexError:
            data_list.append(None)
    return data_list


def add_data(data: dict, file_name=None):
    if file_name is None:
        file_name = CSV_FILE
    with open(file_name, "a", newline="", encoding='utf8') as file:
        data_list = get_data_list(data)
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data_list)


def update_data(data: dict, file_name=None):
    if file_name is None:
        file_name = CSV_FILE
    init_data = get_data(file_name)
    remastered_data = []
    for row in init_data:
        if row[0] == data['url']:
            data_list = get_data_list(data)
            remastered_data.append(data_list)
        else:
            remastered_data.append(row)
    with open(file_name, "w", newline="", encoding='utf8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(remastered_data)


def get_data(file_name=None):
    if file_name is None:
        file_name = CSV_FILE
    with open(file_name, "r", encoding='utf8') as file:
        file_reader = csv.reader(file, delimiter=";")
        data = [row for row in file_reader]
        return data


def get_parsed_urls(file_name=None):
    data = get_data(file_name)
    urls = []
    for row in data:
        urls.append(row[0])
    return urls
