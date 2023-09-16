import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, json, request, jsonify

a = 'digikala.com'
b = 'avandprinter.com'
c = 'khaneyeprinter.com'
d = 'meghdadit.com'


def site_check(line):
    site = re.findall(r'(^.*[\.(://)])*(.+\..+)',line)
    if type(site)==list and len(site) == 1:
        if len(site[0])==2:
            site = site[0][1].lower()
            if site != a and site != b and site != c and site != d:
                return -1
            else:
                return site
        else:
            return-1
    else:
        return -1


def digikala():
    site = 'Digikala.com'
    response = requests.get('https://api.digikala.com/v1/product/1890537/')
    j = response.json()
    product = j['data']['product']['variants']
    if len(product) == 0:
        yield -1
    else:
        for i in range(len(product)):
            price = product[i]['price']['selling_price']
            price = int(price / 10)
            yield price

# function for meghdadit
def meghdadit():
    r = requests.get('https://meghdadit.com/product/74417/hp-laserjet-pro-m28w-laser-printer/')
    soup = BeautifulSoup(r.text, 'html.parser')
    check = soup.find('script',attrs={'type':'application/ld+json'})
    test = re.findall(r'^.*(price).*$',check.text)
    if len(test) == 0:
        return -1
    else:
        site = 'Meghdadit.com'
        soup = BeautifulSoup(r.text, 'html.parser')
        val = soup.find('input', attrs={'type' : 'hidden', 'id':'hfdPrices'})
        string = str(val)
        res = re.findall(r'.+"CalculatedPrice":(\d+).*',string)
        res2 = re.findall(r'.+WarrantyTitle":"(\d+).*',string)
        if len(res2) == 1:
            garanty = res2[0]
        else:
            garanty = 'garnty asli or esalat va salamat kala'
        price = int(res[0])
        return price


# #function for avandprinter
def avandprinter():
    r = requests.get('https://avandprinter.com/product/hp-laserjet-pro-m28w/')
    site = 'Avandprinter.com'
    soup = BeautifulSoup(r.text, 'html.parser')
    check = soup.find('div',attrs={'class':['prdc-price-cntr','price']})
    if check.text.strip() == 'تماس بگیرید':
        return -1
    else:
        val = soup.find('bdi')
        price = re.sub(r'تومان', '', val.text)
        price = price.strip()
        price = re.sub(r',', '', price)
        price = int(price)
        val = soup.find('div', attrs={'class' : 'col-xl-9 col-lg-11 col-md-11 col-sm-10 col-9'})
        if val is None:
            garanty = 'garanty motabar'
        else:
            garanty = re.sub(r'سال گارانتی', '', val.text)
            garanty = re.sub(r'یک', '1', garanty)
            garanty = re.sub(r'دو', '2', garanty)
            garanty = re.sub(r'سه', '3', garanty)
            garanty = re.sub(r'چهار','4',garanty)
            garanty = re.sub(r'پنج','5',garanty)
            garanty = int(garanty.strip())
            if garanty == 1 or garanty == 2 or garanty == 3:
                garanty *= 12 
            else:
                garanty = 'garanty motabar'
        
        return price
    



# #function for khaneyeprinter
def khaneyeprinter():
    r = requests.get('https://khaneyeprinter.com/%D9%BE%D8%B1%DB%8C%D9%86%D8%AA%D8%B1-%DA%86%D9%86%D8%AF%DA%A9%D8%A7%D8%B1%D9%87-%D9%84%DB%8C%D8%B2%D8%B1%DB%8C-%D8%A7%DA%86-%D9%BE%DB%8C-%D9%85%D8%AF%D9%84-hp-laserjet-pro-m28w-multifunction-laser-printer')
    site = 'khaneyeprinter.com'
    soup = BeautifulSoup(r.text, 'html.parser')
    check = soup.find('div',attrs={'class':['bg-opacity-10']})
    if check == None:
        val = soup.find('span' , attrs={'id':'new_price'})
        price = re.sub(r',','',val.text)
        price = int(price)
        val = soup.find('select' , attrs={'class':'d-none'})
        string = str(val)
        res = re.findall(r'گارانتی (\d+)* ماهه شرکتی معتبر',string)
        if len(res) == 0:
            garanty = 'garanty motabar'
        else:
            garanty = res[0]
        return price
    elif check.text.strip()=='ناموجود':
        return -1


#main#
product_list = []

site_list=[]
not_available = []
file = open('G:\expact\pr.txt', 'r')
while True:
    
    line = file.readline()
    if not line:
        break
    if len(line) > 1:
        control_site = site_check(line)
        if control_site == -1:
            not_available.append(line.strip())
        else:
            if control_site in site_list:
                continue
            else:
                site_list.append(control_site)

mojodi_avand = 1
mojodi_digikala = 1
mojodi_meghdad = 1
mojodii_khaneyeprinter = 1
# #Extracting information
for site in site_list:
    if site == 'meghdadit.com':
        info = meghdadit()
        if info == -1:
            mojodi_meghdad = 0
        else:

            price= info
            product_dic= {'product_name':'printer hp jet laser m28w','price':price,'site':'meghdadit.com'}
            product_list.append(product_dic)
    
    if site == 'avandprinter.com':
        info = avandprinter()
        if info == -1:
            mojodi_avand = 0
        else:
            price= info
            product_dic= {'product_name':'printer hp jet laser m28w','price':price,'site':'avandprinter.com'}
            product_list.append(product_dic)
    
    
    
    if site == 'khaneyeprinter.com':
        info = khaneyeprinter()
        if info == -1:
            mojodii_khaneyeprinter = 0
        else:
            price= info
            product_dic= {'product_name':'printer hp jet laser m28w','price':price,'site':'khaneyeprinter.com'}
            product_list.append(product_dic)
    if site == 'digikala.com':
        for info in digikala():
            if info == -1:
                mojodi_digikala = 0
            else:
                price= info
                product_dic= {'product_name':'printer hp jet laser m28w','price':price,'site':'digikala.com'}
                product_list.append(product_dic)



app = Flask(__name__)
app.secret_key = "caircocoders-endalan-2020"
@app.route('/min_all')
def min_all():
    newlist = sorted(product_list, key=lambda d: d['price'])
    if len(newlist) !=0:
        return jsonify(
            data = newlist[0],
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )

@app.route('/digikala')
def digikala():
    digikala_list = []
    for item in product_list:
        if item['site'] == 'digikala.com':
            digikala_list.append(item)
    newlist = sorted(digikala_list, key=lambda d: d['price'])
    if len(digikala_list) != 0:
        return jsonify(
            all_data = digikala_list,
            min = newlist[0],
            max = newlist[(len(newlist)-1)],
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )
@app.route('/avandprinter')
def avandprinter():
    avandprinter_list = []
    for item in product_list:
        if item['site'] == 'avandprinter.com':
            avandprinter_list.append(item)
    newlist = sorted(avandprinter_list, key=lambda d: d['price'])
    if len(avandprinter_list) != 0:
        return jsonify(
            all_data = avandprinter_list,
            min = newlist[0],
            max = newlist[(len(newlist)-1)],
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )


@app.route('/meghdadit')
def meghdadit():
    meghdadit_list = []
    for item in product_list:
        if item['site'] == 'meghdadit.com':
            meghdadit_list.append(item)
    newlist = sorted(meghdadit_list, key=lambda d: d['price'])
    if len(meghdadit_list) != 0:
        return jsonify(
            all_data = meghdadit_list,
            min = newlist[0],
            max = newlist[(len(newlist)-1)],
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )

@app.route('/khaneyeprinter')
def khaneyeprinter():
    khaneyeprinter_list = []
    for item in product_list:
        if item['site'] == 'khaneyeprinter.com':
            khaneyeprinter_list.append(item)
    newlist = sorted(khaneyeprinter_list, key=lambda d: d['price'])
    if len(khaneyeprinter_list) != 0:
        return jsonify(
            all_data = khaneyeprinter_list,
            min = newlist[0],
            max = newlist[(len(newlist)-1)],
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )

@app.route('/mojodi')
def mojodi():
    product = []
    content={}
    if mojodi_avand != 0: 
        content = {'mojodi Avandprinter.com':0}
        product.append(content)
    else:
        content = {'mojodi Avandprinter.com':-1}
        product.append(content)
    
    if mojodii_khaneyeprinter != 0: 
        content = {'mojodi khaneyeprinter.com':0}
        product.append(content)
    else:
        content = {'mojodi khaneyeprinter.com':-1}
        product.append(content)
    if mojodi_meghdad != 0: 
        content = {'mojodi meghdadit.com':0}
        product.append(content)
    else:
        content = {'mojodi meghdadit.com':-1}
        product.append(content)
    if mojodi_digikala != 0: 
        content = {'mojodi digikala.com':0}
        product.append(content)
    else:
        content = {'mojodi digikala.com':-1}
        product.append(content)
    for one in not_available:
        content = {one:-2}
        product.append(content)
        content = {}
    return jsonify(
        mojodi = product
        )

@app.route('/max_all')
def max_all():
    newlist = sorted(product_list, key=lambda d: d['price'])
    if len(newlist) !=0:
        return jsonify(
            data = newlist[(len(newlist)-1)],
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )
    
@app.route('/all')
def all():    
    if len(product_list) !=0:
        return jsonify(
            data = product_list,
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )
    
@app.route('/avrage')
def avg():
    sum = 0
    count = len(product_list)
    for item in product_list:
        sum += item['price']


    if len(product_list) !=0:
        return jsonify(
            data = {'avrage':sum/count},
            status_code = 0
        )
    else:
        return jsonify(
            status_code = -1,
            message = 'not found product'
                       )

if __name__ =='__main__':
     app.run(debug =True)



