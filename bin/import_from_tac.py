import urllib.request
import urllib
import re
import csv
from requests_html import HTMLSession
import os
from pprint import pprint

base_url = 'http://www.thearcherycompany.com/'
dir_url = 'shop/'
csv_file = '../assets/Targets.csv'
target_dir = '../targets/'

pages = ['products.asp?cat=49']


session = HTMLSession()

with open(csv_file, 'a', newline='') as csvfile:
    for page in pages:
        r = session.get("{}{}{}".format(base_url, dir_url, page))
        products = r.html.find(".products")
        product_list = products[0].find(".product")
        pprint(product_list)
        for product in product_list:
            p = product.find('img')
            image = product.find('img')[0].attrs['src']
            name = product.find('.prodname')[0].find('a')[0].text
            name = name.strip()
            if 'JVD' not in name:
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

                name = name.replace('Bjorn ', '')
                name = name.replace('Martin ', '')
                name = name.replace('NFAA ', '')
                name = name.replace('Group 1 Target Face', '')
                name = name.replace('Group 1 Traget Face', '')
                name = name.replace('Group 2 Target Face', '')
                name = name.replace('Group 3 Target Face', '')
                name = name.replace('Group 4 Target Face', '')
                name = name.replace('(Group 1) Target Face', '')
                name = name.replace('(Group 2) Target Face', '')
                name = name.replace('(Group 2)Target Face', '')
                name = name.replace('(Group 3) Target Face', '')
                name = name.replace('(Group 3)Target Face', '')
                name = name.replace('(Group 4) Target Face', '')
                name = name.replace(' - ','')

                print("{} / {} / {} ==> {}".format(name, brand.group(0), image, img_name))

                if not os.path.exists("{}/{}".format(target_dir,brand.group(0))):
                    os.makedirs("{}/{}".format(target_dir,brand.group(0)))
    
                urllib.request.urlretrieve("{}{}{}".format(base_url,dir_url,image), "{}/{}/{}.jpg".format(target_dir,brand.group(0), img_name))
    
                this_writer = csv.writer(csvfile,delimiter=',')
                this_writer.writerow(['{}'.format(brand.group(0)),'',name.strip(),"{}.jpg".format(img_name)])