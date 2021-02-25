import csv

CSV_FILE = 'data.csv'


def create_data_file():
    with open(CSV_FILE, "w", newline="") as file:
        csv.writer(file)


def add_data(data: dict):
    with open(CSV_FILE, "a", newline="", encoding='utf8') as file:
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
        writer = csv.writer(file, delimiter=';')
        writer.writerow(data_list)
