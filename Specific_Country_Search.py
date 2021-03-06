import requests
import time
import colorama
from collections import OrderedDict
from bs4 import BeautifulSoup as soup
from datetime import datetime
import matplotlib.pyplot as plt
from lib import table


def main(option):
    if option.casefold() in table.options_container:
        # Grab connection and Parse HTML
        try:
            start = time.time()
            print('\n\nSending Request...\n')
            ref_req = 'https://www.worldometers.info/coronavirus/' + \
                table.options_container.get(option.casefold())
            req = requests.get(
                ref_req.replace("'", '').replace('None', ''), timeout=1
            )
            req.raise_for_status()
            page_soup = soup(req.text, "html.parser")
            end = time.time()
        
            print(colorama.Fore.GREEN, '\nScraping took ' +
                  convert(end - start) + '\n', colorama.Style.RESET_ALL)

            getInfo(option, page_soup)
        except requests.exceptions.RequestException as err:
            print(colorama.Fore.RED, 'Something went wrong! ',
                  err, colorama.Style.RESET_ALL)
            with open('Errors.txt', 'a', encoding='utf-8') as f:
                f.write(dt_string_time + ' Searching For: ' +
                        option.capitalize() + ' ' + str(err) + '\n\n')
            main(option)
    elif option.casefold() == 'cancel':
        quit()
    else:
        raise KeyError(option + ' does not exist in the Dictionary')


def createChart(country, data):
    colors = ['#66b3ff', '#ff9999', '#99ff99', '#f98aff']
    plt.figure(figsize=(6, 3))
    plt.gcf().canvas.set_window_title('Coronavirus ' + country.capitalize() + ' View')

    active_cases = int(data[0]) - int(data[1]) - int(data[2])

    labels = ["Cases: " + "{:,}".format(int(data[0])), "Deaths: " + "{:,}".format(int(data[1])),
              "Recoveries: " + "{:,}".format(int(data[2])), "Active Cases: " + "{:,}".format(active_cases)]
    values = [data[0], data[1], data[2], active_cases]
    explode = (0.05, 0.05, 0.05, 0.05)

    plt.pie(values, colors=colors, startangle=90, shadow=True,
            explode=explode, pctdistance=0.85, autopct='%1.1f%%')
    plt.legend(labels=labels)
    plt.xlabel('Date: ' + dt_string)

    center_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)

    plt.axis('equal')
    plt.title(country.capitalize() + ' Coronavirus Chart')

    plt.show()


def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return "%d:%02d:%02d" % (hour, min, sec)


def getInfo(country, locator):
    data_container = []
    for container in locator.findAll('div', {'class': 'content-inner'})[0:]:
        records = [records.text for records in container.findAll(
            'div', {'class': 'maincounter-number'})[0:]]
        print(colorama.Fore.LIGHTMAGENTA_EX, country.capitalize() + ' - {' + dt_string_time + '} | Cases: ' + records[0].strip().replace('N/A', '0') + ' | Deaths: ' + records[1].strip(
        ).replace('N/A', '0') + ' | Recoveries: ' + records[2].strip().replace('N/A', '0'), colorama.Style.RESET_ALL)

        total_cases = records[0].replace(',', '').replace('N/A', '0')
        total_deaths = records[1].replace(',', '').replace('N/A', '0')
        total_recoveries = records[2].replace(',', '').replace('N/A', '0')

        data_container.extend((total_cases, total_deaths, total_recoveries))
        createChart(country, data_container)


if __name__ == '__main__':
    colorama.init()
    start = time.time()
    now = datetime.now()
    year, month = now.strftime('%Y'), now.strftime('%B')
    dt_string, dt_string_time = now.strftime(
        "%B %d-%Y"), now.strftime("%B %d-%Y | %H:%M:%S")

    i = 0
    sorted_dict = OrderedDict(sorted(table.options_container.items()))
    for key in sorted_dict:
        i += 1
        print(str(i) + '. ' + key.capitalize() + '\n')

    country = input('Select View Options: ')
    main(country)
    end = time.time()
    print(colorama.Fore.GREEN, '\n\nWhole Program ran for: ' +
          convert(end-start) + '\n\n', colorama.Style.RESET_ALL)
