from urllib.request import urlopen
from urllib.parse import unquote
from bs4 import BeautifulSoup
import requests 
from urllib.error import HTTPError
from urllib.error import URLError





# check if any exceptions are thrown
#   def errorCheck(URL):
#       try:
#           html = urlopen(URL)
#       except HTTPError as e:
#           print(e)
#       except URLError as e:
#           print('The server could not be found!')
#       else:
#           return True



def getAllListings(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    listingsListOld = soup.find_all("a", class_="mmm")
    listingsList = []
        # For as many listings there are on the page, add each listing to a list
    for i in range(len(listingsListOld)):
        listingsList.append("https:" + listingsListOld[i].get('href'))
    
    return listingsList
    


def htmlParse(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    numOfPages = soup.find_all('a', class_ = "pageNumbers")
    mainPageLinks = []

    if not numOfPages:
        # print("there is only a single page")
        mainPageLinks.append(URL)
    else:
        mainPageLinks.append(URL)
        for i in range(len(numOfPages)-2):
            mainPageLinks.append(URL[:-1] + str((i+2)))
            
    carList =[]
    for x in mainPageLinks:
        carList.extend(getAllListings(x))

    for y in range(len(carList)):
        print("Car #{}, link = {}".format(y, carList[y]))





    return







# https://m.mobile.bg/results?pubtype=1&marka=BMW&model=320&currency=%D0%BB%D0%B2.&year=1999&year1=2006&category=%D0%9A%D1%83%D0%BF%D0%B5
def main():
    urlLink = "https://www.mobile.bg/pcgi/mobile.cgi?act=3&slink=kz5cf5&f1=1"
    htmlParse(urlLink)





if __name__ == "__main__":
    main()