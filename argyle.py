import time
import json
from selenium import webdriver  
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

#Opens the browser. You will have 30 seconds to enter the login credentials.
def openBrowser():
    browser = webdriver.Chrome(ChromeDriverManager().install())
    link = "https://www.upwork.com/ab/find-work/"
    loginLink = "https://www.upwork.com/ab/account-security/login"
    browser.get(loginLink)
    time.sleep(30)
    
    browser.get(link)
    time.sleep(5)
    html = browser.page_source
    browser.close()
    organizeData(html)


#Use BeautifulSoup to organize the data
def organizeData(html):
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all("section")
    listOfAllInfo = []
    for section in sections:
        data_dict = {}
        
        title = section.find("h4",{"class" : "job-title m-0 p-sm-right ng-isolate-scope"})
        data_dict['title_link'] = title.find('a')['href']
        data_dict['title_text'] = title.text
        
        getAllSpans = section.find_all("span",{"class" : "ng-isolate-scope"})
        
        data_dict['payment_method'] = getAllSpans[0].text
        
        data_dict['level'] = getAllSpans[1].text
        
        data_dict['time/budget'] = getAllSpans[2].text
        
        posted = section.find("time", {"class" : "ng-isolate-scope"})
        data_dict['posted'] = posted.text
        
        description = section.find("div", {"class" : "m-sm-bottom ng-isolate-scope"})
        data_dict['description'] = description.text
            
        spent = section.find("span", {"class" : "client-spendings display-inline-block"})
        data_dict['spent'] = spent.text
        
        location = section.find("strong", {"class" : "text-muted client-location ng-binding"})
        data_dict['location'] = location.text
                
        listOfAllInfo.append(data_dict)
        
        storeJsonData(listOfAllInfo)
  
#Store the data in a file called data.json in json format. The file will be stored in your working directory.
def storeJsonData(listOfAllInfo):
    
    with open('data.json', 'w') as f:
        json.dump(listOfAllInfo, f)
    
if __name__ == "__main__":
    openBrowser()