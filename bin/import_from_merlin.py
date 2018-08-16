import urllib.request
import urllib
import re
from bs4 import BeautifulSoup
from pprint import pprint
import csv
from requests_html import HTMLSession
import os

base_url = 'http://www.merlinarchery.co.uk/'
dir_url = ''
csv_file = '../assets/Targets.csv'
target_dir = '../targets/'

pages = ['merlin-hd-target-faces.html', 'lcc-target-faces.html', 'jvd-target-faces.html', 'maximal-animal-target-faces.html',
         'delta-mckenzie-target-faces.html']


session = HTMLSession()

with open(csv_file, 'a', newline='') as csvfile:
    for page in pages:
        r = session.get("{}{}{}".format(base_url, dir_url, page))

        table = r.html.find("#super-product-table")

        tbody = table[0].find('tbody')
        rows = tbody[0].find('tr')
        for row in rows:
            cells = row.find('td')
            image = cells[0].find('a')[0].attrs['href']
            name = cells[1].find('div')[1].text
            name = name.strip()
            brand = re.match(r"^\w+",name)
            temp_name = re.sub(r"\(group \d\)", '', name, re.IGNORECASE)
            img_name = temp_name.strip().replace(' ', '-')
            img_name = img_name.replace('Merlin-HD-', '')
            img_name = img_name.replace('LCC-Target-Face-', '')
            img_name = img_name.replace('JVD-Target-Face-', '')
            img_name = img_name.replace('Maximal-Target-Faces-', '')
            img_name = img_name.replace('Delta-McKenzie-Target-Face-', '')
            img_name = img_name.replace('/', '-')
            img_name = img_name.lstrip('-')

            name = name.replace('Merlin HD ', '')
            name = name.replace('LCC Target Face ', '')
            name = name.replace('JVD Target Face ', '')
            name = name.replace('Maximal Target Faces ', '')
            name = name.replace('Delta McKenzie Target Face', '')
            name = name.lstrip(' - ')

            print("{} {} {} ==> {}".format(name, brand.group(0), image, img_name))

            if not os.path.exists("{}/{}".format(target_dir,brand.group(0))):
                os.makedirs("{}/{}".format(target_dir,brand.group(0)))

            urllib.request.urlretrieve("{}".format(image), "{}/{}/{}.jpg".format(target_dir,brand.group(0), img_name))

            this_writer = csv.writer(csvfile,delimiter=',')
            this_writer.writerow(['{}'.format(brand.group(0)),'',name.strip(),"{}.jpg".format(img_name)])