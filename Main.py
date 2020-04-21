##IMPORTS##
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import xlsxwriter


def nextPage():
    time.sleep(speed)
    ##Scrolls down##
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    ###Changes to the next page###
    print("Next page")
    nextPage = driver.find_elements_by_xpath("//div[@class='_1m76pmy']")

    #Sometimes a popup covers the nextpage button
    try:
        nextPage[-1].click()
    except:
        #Remove the cookie bar
        cookies = driver.find_element_by_xpath("//button[@class='optanon-allow-all accept-cookies-button']").click()        
        time.sleep(speed)
        nextPage[-1].click()

def fetchName():
    time.sleep(speed)
    room = []
    rooms = driver.find_elements_by_xpath("//a[@class='_i24ijs']")
    ###Find the list of names###
    for name in rooms:
        room.append((name.get_attribute("aria-label"),name.get_attribute("href")))
    return room

def fetchPrice():
    try:
        price = driver.find_elements_by_xpath("//span[@class='_doc79r']")
        cleanText = price[0].text.replace("£","")
    except:
        price = driver.find_elements_by_xpath("//span[@class='_18ilrswp']")
        cleanText = price[0].text.replace("£","")
    return cleanText

def fetchLocation(url):
    time.sleep(speed)
    driver.get(url)
    time.sleep(5)
    locations = driver.find_elements_by_xpath("//a[@class='_abw475']")
    string = ""
    for location in locations:
        string = string + location.text
    return string

def writeTofile(Array):
    xbook = xlsxwriter.Workbook("Hoilday.xlsx")
    xsheet = xbook.add_worksheet("Villa Information")
    for index,data in enumerate(Array):
            xsheet.write_row(index,0,data)
    xbook.close()

##Global vars
global driver
global time



##SETTING##
#url = "https://www.airbnb.co.uk/s/Barcelona--Spain/homes?refinement_paths%5B%5D=%2Fhomes&current_tab_id=home_tab&selected_tab_id=home_tab&version=1.6.5&tab_id=home_tab&source=mc_search_bar&click_referer=t%3ASEE_ALL%7Csid%3Aa55b4726-8a8c-4c61-86b4-0ae98a1f0bb0%7Cst%3ALANDING_PAGE_MARQUEE&title_type=NONE&place_id=ChIJ5TCOcRaYpBIRCmZHTz37sEQ&screen_size=large&s_tag=abr2M1Tq&search_type=pagination&hide_dates_and_guests_filters=false&checkin=2020-08-20&checkout=2020-08-27&adults=5&min_beds=5&amenities%5B%5D=7&property_type_id%5B%5D=11&last_search_session_id=d0b515b6-9444-4380-8893-975bd7265699"
#url = "https://www.airbnb.co.uk/s/Paris/homes?refinement_paths%5B%5D=%2Fhomes&screen_size=large&search_type=section_navigation"
#url = "https://www.airbnb.co.uk/s/Benidorm--Spain/homes?refinement_paths%5B%5D=%2Fhomes&current_tab_id=home_tab&selected_tab_id=home_tab&screen_size=large&hide_dates_and_guests_filters=false&place_id=ChIJw3UlptwEYg0RtW7yDwypnyE&checkin=2020-08-20&checkout=2020-08-27&adults=5&property_type_id%5B%5D=11&amenities%5B%5D=7&search_type=filter_change"
rooms = []
prices = []
speed = 5


url = input("Enter URL")

##INIT##
driver = webdriver.Chrome()
driver.get(url)


count = 1
#The amounts of pages to search
searchPageLen = driver.find_elements_by_xpath("//div[@class='_1bdke5s']")[-1].text
for x in range(int(searchPageLen)):#Loops through the amount of pages present
    print("Page ",count," Out of ",searchPageLen)
    count += 1
    rooms.append(fetchName())
    nextPage()
print("Alls rooms fetched\nPages Searched ",len(rooms))

#Fetches the location
print("Fetching locations...")
roomDetails = [] #Details that need to be wrote to the
for page in rooms:
    print("Searching ",len(rooms)," Pages")
    for roomNlink in page:
        link = roomNlink[1]
        name = roomNlink[0]
        location = fetchLocation(link)
        price = fetchPrice()
        roomDetails.append([name,price,location,link])
print("Search completed")

##WRITING TO FILE##
print("Writing to file...")
writeTofile(roomDetails)
print("Scraping completed")

