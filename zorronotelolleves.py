import requests as r
import os
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from time import sleep


client = MongoClient()
db = client.db.queue

currentPageFile = "pagefile.txt"


def products(field,page):
    result = os.popen("curl 'http://buscador.compras.imss.gob.mx/index.php' -H 'Pragma: no-cache' -H 'Origin: http://buscador.compras.imss.gob.mx' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: es-ES,es;q=0.8,en;q=0.6' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept: */*' -H 'Cache-Control: no-cache' -H 'X-Requested-With: WAJAF::Ajax - WebAbility(r) v5' -H 'Cookie: __utma=37030712.222899114.1488655887.1488656746.1488656746.1; __utmb=37030712.1.10.1488656746; __utmc=37030712; __utmz=37030712.1488656746.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __asc=9819a67f15a9ace2b0599c2b83a; __auc=9819a67f15a9ace2b0599c2b83a; _ga=GA1.3.222899114.1488655887' -H 'Connection: keep-alive' -H 'Referer: http://buscador.compras.imss.gob.mx/wrap/index.html' --data '&type=compras&message=X&filtered=1&descripcion="+field+"&proveedor=&numcompra=&delegacion=values%3D&fecha=min%3D%3Bmax%3D&procedimiento=values%3D&exact=false&numperpage=20&page=" + str(page)+"&order=fecha%20desc' --compressed").read()
    return(json.loads(result))


def writePage(number, quantity):
    f = open(currentPageFile, 'w')
    f.write(str(number)+ "\t" + str(quantity))
    f.close()
    return "ok"


def readPage():
    file = open(currentPageFile, "r")
    for line in file:
        number, quantity = line.split("\t")
    return int(number), int(quantity)


def main():
    number = 1
    quantity = 0
    try:
        number, quantity = readPage()
        if number == 1:
            errorBase()
    except:
        first_page = products(" ",number)
        sleep(1)
        print(writePage(number, quantity))
        quantity = int(first_page["result"]["quantity"])
        pages = int(int(first_page["result"]["quantity"])/20)
        db.insert_many(first_page["result"]["data"])
    for i in range(number,quantity+1):
        print(writePage(i, quantity))
        current_page = products(" ",i)
        sleep(1)
        db.insert_many(current_page["result"]["data"])


if __name__ == "__main__":
    main()
