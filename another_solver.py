from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from bs4 import BeautifulSoup
import speech_recognition as sr
import urllib.request
import pydub

username = 'bobsuperworker'
password = 'Argyleawesome123!'
secretAnswer = 'number42'
delayTime = 2
audioToTextDelay = 10
byPassUrl = 'https://www.upwork.com/ab/find-work/'
loginURL = 'https://www.upwork.com/ab/account-security/login'
IBMLink = 'https://speech-to-text-demo.ng.bluemix.net/'
driver = webdriver.Chrome()
driver.get(loginURL)


def login():
        try:
            driver.find_element_by_id('login_username').send_keys(username)
            time.sleep(2)
            driver.find_element_by_id('login_username').send_keys(Keys.ENTER)
            time.sleep(2)
            driver.find_element_by_id('login_password').send_keys(password)
            time.sleep(2)
            driver.find_element_by_id('login_password').send_keys(Keys.ENTER)
            getData()
        except Exception:
            breakRecaptcha()


def audioToText(mp3Path):
    
    driver.execute_script('''window.open("","_blank");''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(IBMLink)
    time.sleep(7)
    allIframesLen = driver.find_elements_by_tag_name('iframe')
    
    cookiesBtnFound = False
    
    for index in range(len(allIframesLen)):
            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[index]
            driver.switch_to.frame(iframe)
            driver.implicitly_wait(delayTime)
            try:
                cookiesBtn = driver.find_element_by_class_name('required')
                cookiesBtn.click()
                cookiesBtnFound = True
                break
            except Exception:
                pass
    
    
    if cookiesBtnFound:

    # Upload file 
        time.sleep(1)
        driver.find_element_by_id('root').find_elements_by_class_name('dropzone _container _container_large')
        btn = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
        btn.send_keys(mp3Path)
    
        # Audio to text is processing
        time.sleep(audioToTextDelay)
    
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[6]/div/div/div').find_elements_by_tag_name('span')
        result = " ".join( [ each.text for each in text ] )
    
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
        return result
    
    else:
        print('oh-oh')

def saveFile(content,filename):
    with open(filename, "wb") as handle:
        for data in content.iter_content():
            handle.write(data)

def breakRecaptcha():
    #driver = webdriver.Chrome()
    driver.get(loginURL)
    while True:
        googleClass = driver.find_elements_by_class_name('g-recaptcha')[0]
        outeriframe = googleClass.find_element_by_tag_name('iframe')
        outeriframe.click()
        
        allIframesLen = driver.find_elements_by_tag_name('iframe')
        audioBtnFound = False
        
        for index in range(len(allIframesLen)):
            driver.switch_to.default_content()
            iframe = driver.find_elements_by_tag_name('iframe')[index]
            driver.switch_to.frame(iframe)
            driver.implicitly_wait(delayTime)
            try:
                audioBtn = driver.find_element_by_id('recaptcha-audio-button') or driver.find_element_by_id('recaptcha-anchor')
                audioBtn.click()
                audioBtnFound = True
                break
            except Exception:
                pass
        
        if audioBtnFound:
            try:
                notYetSuccess = True
                while notYetSuccess:
                    driver.switch_to.default_content()
                    frames = driver.find_elements_by_tag_name("iframe")
                    driver.switch_to.frame(frames[-1])
                    time.sleep(5)
                
                    # get the mp3 audio file
                    src = driver.find_element_by_id("audio-source").get_attribute("src")
                    print("[INFO] Audio src: %s" % src)
                
                    # download the mp3 audio file from the source
                    #with urllib.request.urlopen(src) as response, open(f, 'wb') as out_file:
                     #   data = response.read() # a `bytes` object
                      #  out_file.write(data)
                    urllib.request.urlretrieve(src, os.path.normpath(os.getcwd() + "\\sample.mp3"))
                    time.sleep(5)
                    print('audio downloaded')
                
                    # load downloaded mp3 audio file as .wav
                    try:
                        notYetSuccess = False
                        sound = pydub.AudioSegment.from_mp3(os.path.normpath(os.getcwd() + "\\sample.mp3"))
                        sound.export(os.path.normpath(os.getcwd() + "\\sample.wav"), format="wav")
                        sample_audio = sr.AudioFile(os.path.normpath(os.getcwd() + "\\sample.wav"))
                        print('success_audio')
                        r = sr.Recognizer()
                        with sample_audio as source:
                            audio = r.record(source)
                        key = r.recognize_google(audio)
                        print("[INFO] Recaptcha Passcode: %s" % key)
                    
                        time.sleep(3)
                        # key in results and submit
                        driver.find_element_by_id("audio-response").send_keys(key.lower())
                        time.sleep(3)
                        driver.find_element_by_id("audio-response").send_keys(Keys.ENTER)
                        driver.switch_to.default_content()
                        login()
                    
                    except Exception:
                        print("[-] Please run program as administrator or download ffmpeg manually, "
                              "http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/")
                
                    # translate audio to text with google voice recognition
                    break
                     
            except Exception as e:
                print(e)
                driver.refresh()
                continue
        else:
            print('Button not found. Run again the bot')
        
#change this        
def getData():
        print('Success')
        time.sleep(5)
        driver.get(byPassUrl)
        html = driver.page_source
        print(html.read())
        soup = BeautifulSoup(html.read(), 'html.parser')
        print(soup)
        sections = soup.find_all("section")
        for section in sections:
            data_dict = {}
            infoA = section.find("div", {"class": "clearfix ng-scope"})
            data_dict['Title_URL'] = infoA.find('a')
        print('Finished')
        

if __name__ == "__main__":
    login()