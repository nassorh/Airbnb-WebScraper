##OOP##
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import xlsxwriter

class webScrap():
    def __init__(self,url):
        self.url = url
        self.rooms = []
        self.prices = []
        self.roomDetails = [] 
        self.speed = 5

        #start up
        driver = webdriver.Chrome()
        self.driver.get(url)

    def fetchSearchPageLen(self):
        searchPageLen = int(driver.find_elements_by_xpath("//div[@class='_1bdke5s']")[-1].text)
        return searchPageLen

    def nextPage(self):
        time.sleep(self.speed)
        ##Scrolls down##
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        ###Changes to the next page###
        print("Next page")
        nextPage_ = self.driver.find_elements_by_xpath("//div[@class='_1m76pmy']")

        #Sometimes a popup covers the nextpage button
        try:
            nextPage_[-1].click()
        except:
            #Remove the cookie bar
            cookies = self.driver.find_element_by_xpath("//button[@class='optanon-allow-all accept-cookies-button']").click()        
            time.sleep(self.speed)
            nextPage_[-1].click()

    def fetchLocation(self,url):
        time.sleep(self.speed)
        self.driver.get(url)
        time.sleep(5)
        locations = driver.find_elements_by_xpath("//a[@class='_abw475']")
        string = ""
        for location in locations:
            string = string + location.text
        return string

    def fetchPrice(self):
    try:
        price = self.driver.find_elements_by_xpath("//span[@class='_doc79r']")
        cleanText = price[0].text.replace("£","")
    except:
        price = self.driver.find_elements_by_xpath("//span[@class='_18ilrswp']")
        cleanText = price[0].text.replace("£","")
    return cleanText

    def searchAllPages(self):
        count = 1
        searchPageLen = self.fetchSearchPageLen()
        for x in range(searchPageLen):
            print("Page ",count," Out of ",searchPageLen)
            rooms.append(fetchName())
            count += 1
            web.nextPage()
        print("Alls rooms fetched\nPages Searched ",len(rooms))

    def fetchLocations(self):
        print("Fetching locations...")
        #Details that need to be wrote to the
        for page in rooms:
            print("Searching ",len(rooms)," Pages")
            for roomNlink in page:
                link = roomNlink[1]
                name = roomNlink[0]
                location = self.fetchLocation(link)
                price = self.fetchPrice()
                self.roomDetails.append([name,price,location,link])
        print("Search completed")

    def writeToFile(self):
        print("Writing to file...")

        xbook = xlsxwriter.Workbook("Hoilday.xlsx")
        xsheet = xbook.add_worksheet("Villa Information")
        for index,data in enumerate(self.roomDetails):
                xsheet.write_row(index,0,data)
        xbook.close()

        print("Scraping completed")

url = input("Enter URL")
web = webScrap(url)
web.searchAllPages()
web.fetchLocations()
web.writeToFile()


