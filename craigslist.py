# -*- coding = utf-8 -*-
# @Time: 12/04/2022

import sys
from bs4 import BeautifulSoup
import re
import urllib
import urllib.request
import urllib.error
import xlwt
import sqlite3


def main():

    print('Start Retrieving······')

    baseurl = 'https://annarbor.craigslist.org/search/apa?s='
    pagecount = 2
    num = 120
    redlingdata = []

    try:
        with open(r'annarbor_renting_cach.txt', 'r') as fp:
            for line in fp:
                print(len(line))
                x = line[:-1]
            redlingdata.append(x)
        fp.close()
    except:
        redlingdata=[]
    
    if redlingdata:
        datalist = redlingdata
    else:
        datalist = getData(baseurl, pagecount, num)
        with open(r'annarbor_renting_cache.txt', 'w') as fp:
            for item in datalist:
                fp.write("%s\n" % item)
            print('Done')
        fp.close()

    # print(datalist[1])

    savepath = 'annarbor_renting.xls'
    saveData(datalist, pagecount, num, savepath)
    dbpath = 'annarbor_renting.db'
    saveData2DB(datalist, dbpath)
    # askURL('https://annarbor.craigslist.org/search/apa?s=0')

    print('Retrieving Complete!')


def getData(baseurl, pagecount, num):

    datalist = []

    for i in range(0, pagecount):
        url = baseurl + str(i * num)
        # print(url)

        html = askURL(url)

        soup = BeautifulSoup(html, 'html.parser')
        # print(soup)

        for item in soup.find_all('li', class_='result-row'):
            # print(item)
            data = []

            title = item.find('a', class_='result-title').get_text()
            # print(title)
            data.append(title)

            if item.find('span', class_='result-hood'):
                location = item.find('span', class_='result-hood').get_text()
                location = location.replace('(', '')
                location = location.replace(')', '')
            else:
                location = 'Lack information'
            data.append(location)

            price = item.find('span', class_='result-price').get_text()
            # print(price)
            data.append(price)

            link = item.find('a').get('href')
            info, imgLink = getInfo(link)
            data.append(info)
            data.append(imgLink)
            data.append(link)
            # print(link)
            datalist.append(data)
    # print(datalist)
    return datalist


def getInfo(url):
    tempinfo = []
    info = ''
    tempimglink = []
    imglink = ''

    findImgLink = re.compile(r'src="(.*?)"')

    html = askURL(url)
    soup = BeautifulSoup(html, 'html.parser')
    topic = soup.find_all('section', class_='body')
    # print(topic)

    tempinfo = soup.find('section', id="postingbody").get_text()
    # print(tempinfo)
    info = tempinfo.replace('\n', '')
    info = tempinfo.replace('\'', '')
    info = tempinfo.replace('\"', '')

    topic = str(topic)
    tempimglink = re.findall(findImgLink, topic)
    if tempimglink:
        imglink = " , ".join(str(v)
                             for v in tempimglink)
    else:
        imglink = "There is no picture"

    return info, imglink


def askURL(url):

    
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.37'
    }   
    request = urllib.request.Request(url, headers=head)     
    html = ''

    
    try:
        response = urllib.request.urlopen(request)          
        html = response.read().decode('utf-8')              
        # print(html)
    except urllib.error.URLError as e:                      
        if hasattr(e, 'code'):                              
            print(e.code)
        if hasattr(e, 'reason'):                            
            print(e.reason)

    return html


def saveData(datalist, pagecount, num, savepath):

    # print('saving...')
    book = xlwt.Workbook(
        encoding='utf-8', style_compression=0)     
    sheet = book.add_sheet('Apartments_Housing_for_Renting',
                           cell_overwrite_ok=True)   

    col = ('Num', 'Title', 'Location', 'Price',
           'Information', 'Image_Link', 'Link')

    for i in range(0, len(col)):
        sheet.write(0, i, col[i])

    for i in range(0, pagecount*num):
        # print('第%d条' % (i+1))
        data = datalist[i]
        sheet.write(i+1, 0, i+1)            
        for j in range(0, len(data)):

            sheet.write(i+1, j+1, data[j])  
    book.save(savepath)                     
    # print('Successful!')


def saveData2DB(datalist, dbpath):
    init_DB(dbpath)
    conn = sqlite3.connect(dbpath)

    cursor = conn.cursor()

    # Queries to INSERT records.
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'

        sql = '''
            insert into renting(
            title, location, price, information, image_link, link)
            values(%s)''' % ",".join(str(v) for v in data)
        # print(sql)
        cursor.execute(sql)

        conn.commit()

    # print("Data Inserted in the table: ")
    # data = cursor.execute('''SELECT * FROM renting''')
    # for row in data:
    #     print(row)

    # Closing the connection
    conn.close()


def init_DB(dbpath):
    connection_obj = sqlite3.connect(dbpath)

# cursor object
    cursor_obj = connection_obj.cursor()

# Drop the GEEK table if already exists.
    cursor_obj.execute("DROP TABLE IF EXISTS renting")

# Creating table
    table = """ CREATE TABLE renting (
            id integer primary key autoincrement,
            title text,
            location text,
            price text,
            information text,
            image_link text,
            link text
        ); """

    cursor_obj.execute(table)

    # print("Table is Ready")

# Close the connection
    connection_obj.close()


if __name__ == "__main__":          
    main()
    
