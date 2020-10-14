import argparse
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape

def get_spirit(fraction):
    separated_spirit = fraction.split(':')
    spirit = separated_spirit[1]
    return spirit.strip()

def get_wines_of_this_kind(wine_description):
    wines = []
    wine_specification = {}
    separated_description = wine_description.split('\n')
    for fraction in reversed(separated_description): # order matters!
        if 'Название' in fraction:
            wine_specification['title'] = get_spirit(fraction)
            wines.append(wine_specification)
            wine_specification = {}
        elif 'Сорт' in fraction:
            wine_specification['sort'] = get_spirit(fraction)
        elif 'Цена' in fraction:
            wine_specification['price'] = get_spirit(fraction)
        elif 'Картинка' in fraction:
            wine_specification['image'] = get_spirit(fraction)
        elif 'Выгодное предложение' in fraction:
            wine_specification['discount'] = True
    return wines


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Site of elite wines')
    parser.add_argument("TEXT_FILE", help="path to txt file with beverages description")
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    year_of_foundation = 1920
    now = datetime.datetime.now()
    current_year = now.year
    winery_age = current_year - year_of_foundation

    txt_file = args.TEXT_FILE

    try:
        with open(txt_file, 'r', encoding='UTF-8-sig') as file:
            raw_data = file.read()
    except FileNotFoundError:
        print('''
        Can not find txt file or wrong file path.
        Please read README.MD.
        ''')
        exit()


    assortment_of_beverages = raw_data.split('#')
    del assortment_of_beverages[0]

    kinds_of_beverages = []

    for kind in assortment_of_beverages:
        separated_kind = kind.split('\n')
        kind_of_beverages = separated_kind[0].strip()
        kinds_of_beverages.append(kind_of_beverages)

    total_beverages_info = {}

    for beverage in assortment_of_beverages:
        for kind in kinds_of_beverages:
            if kind in beverage:
                wines = get_wines_of_this_kind(beverage)
                total_beverages_info[kind] = wines

    total_beverages_elements = total_beverages_info.items()

    rendered_page = template.render(
        winery_age=winery_age,
        total_beverages_elements = total_beverages_elements,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()