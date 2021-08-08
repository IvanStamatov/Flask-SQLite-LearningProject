from urllib.request import urlopen
from urllib.parse import unquote
from bs4 import BeautifulSoup
import requests 
from urllib.error import HTTPError
from urllib.error import URLError
import sqlite3
from sqlite3 import Error





def htmlParse(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    linkPagesNew = [str(URL)]

    for name in soup.find_all("a", {"class": "pageNumbers"}):
        linkPagesNew.append("https:" + name.get('href'))
    linkPagesNew = set(linkPagesNew)
    linkPagesNew = list(linkPagesNew)
    listingsList = []
    
    for x in linkPagesNew:
        print(x)
        page = requests.get(x)
        soup = BeautifulSoup(page.content, "html.parser")
        listingsListOld = soup.find_all("a", class_="mmm")
        for i in range(len(listingsListOld)):
            listingsList.append("https:" + listingsListOld[i].get('href'))
    return listingsList



def extractDetails(carlist):
    carYear = "None"
    carHorsepower = "None"
    carType = "None"
    carMilage = "None"
    carColor = "None"

    conn = sqlite3.connect("pythonsqlite.db")
    cursor = conn.cursor()

    for z in range(len(carlist)):
        page = requests.get(carlist[z])
        soup = BeautifulSoup(page.content, "html.parser")
        carLink = carlist[z]
        carTitle = soup.find_all('h1')[0].text
        carPrice = soup.find(id="details_price").text
        carDetails_UL_Dic = {}
        car_Details = soup.find_all("ul", {"class": "dilarData"})[0]
        listItems = car_Details.find_all('li')
        num = 0
        for c in listItems:
            if c.text == "Дата на производство":
                carYear = listItems[num + 1].text
            elif c.text == "Мощност":
                carHorsepower = listItems[num + 1].text
            elif c.text == "Категория":
                carType =  listItems[num + 1].text
            elif c.text == "Пробег":
                carMilage = listItems[num + 1].text
            elif c.text == "Цвят":
                carColor = listItems[num + 1].text
            num += 1

        carViews = soup.find("span", {"class": "advact"}).text
        descriptionCheck = soup.find_all('div', string='Допълнителна информация:')
        if descriptionCheck:
            carDescription = soup.find_all('td', attrs={'style':'line-height:24px; font-size:14px; color: #444;'})[0].text
        else:
            carDescription = "None"
        carSellerPhone = soup.find("div", {"class": "phone"}).text
        carSellerAddress = soup.find("div", {"class": "adress"}).text\


        cursor.execute("INSERT INTO cars VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (carLink,carTitle,carPrice,carYear,carHorsepower,carType,carMilage,carColor,carViews,carDescription,carSellerPhone,carSellerAddress))
        conn.commit()
    return 



def main():
    urlLink = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=l0wsso&f1=1"
    # urlLink = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=l0ywb3&f1=1"
    carlist = htmlParse(urlLink)
    
    conn = sqlite3.connect("pythonsqlite.db")
    cursor = conn.cursor()
    sql_create_table = """ CREATE TABLE IF NOT EXISTS cars (
                            "carLink" text,
                            "carTitle" text,
                            "carPrice" text,
                            "carYear" text,
                            "carHorsepower" text,
                            "carType" text,
                            "carMilage" text,
                            "carColor" text,
                            "carViews" text,
                            "carDescription" text,
                            "carSellerPhone" text,
                            "carSellerAddress" text
                                    ); """
    cursor.execute(sql_create_table)

    extractDetails(carlist)
    conn.close()
    print("end")



if __name__ == "__main__":
    main()