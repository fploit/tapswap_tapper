import json
import os
from time import sleep
from threading import Thread
from selenium_driver import driver as ChromeDriver
from code_editor import generate_all_variations
from telebot import TeleBot


config = json.loads(open("./config.json", "r").read())
bot = TeleBot(config['bot_token'])
chat_id = config['chat_id']

def click(driver):
    print("======== Start Tapping ========")
    for _ in range(int(config['limit'] / config['multitap_level']) + 1):
        driver.find_element("xpath", '//*[@id="ex1-layer"]').click()


def try_close_msg(driver):
    try:
        driver.find_element("xpath", '//*[@id="app"]/div[3]/button').click()
    except:
        pass
    sleep(1)
    try:
        driver.find_element("xpath", '//*[@id="app"]/div[2]/div[1]/div/div').click()
    except:
        pass
    sleep(1)
    try:
        driver.find_element("xpath", '//*[@id="app"]/div[2]/div[1]/div/div').click()
    except:
        pass


def get_stream_link(driver):
    try:
        driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[1]').click()
        link = driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div[1]/a').get_attribute('href')
        sleep(1)
        driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/div').click()
        with open("stream.link", "w") as f:
            f.write(link)
        sleep(1)
        return link
    except:
        return "Error!"


def try_stream_code(driver, code):
    try:
        before = driver.find_element("xpath", '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div[1]/h1').text
        driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[1]').click()
        sleep(1)
        driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div[2]/input').send_keys(code)
        driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/button').click()
        sleep(12)

        btn = driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/button')
        btn_text = btn.text
        try_code_list = True

        possible_cases = generate_all_variations(code)
        print(possible_cases)

        if btn_text == "Claim":
            btn.click()
            try_code_list = False
            sleep(2)
            after = driver.find_element("xpath", '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div[1]/h1').text
            bot.send_photo(chat_id, open("./code.png", "rb"), caption=f'{code}\n\nStream code entered successfully\nbefore apply code => {before}\nafter apply code => {after}')
        
        if try_code_list:
            bot.send_photo(chat_id, open("./code.png", "rb"), caption=f'try code list\n\n{str(possible_cases)}')
        for c in possible_cases:
            if try_code_list:
                driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div[2]/input').clear()
                driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[2]/div[2]/div[2]/input').send_keys(c)
                driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/button').click()
                sleep(12)
                btn = driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/button')
                btn_text = btn.text
                if btn_text == "Claim":
                    btn.click()
                    try_code_list = False
                    sleep(2)
                    after = driver.find_element("xpath", '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/div[1]/h1').text
                    bot.send_photo(chat_id, open("./code.png", "rb"), caption=f'{code}\n\nStream code entered successfully ==> {c}\nbefore apply code => {before}\nafter apply code => {after}')
        
        if try_code_list:
            bot.send_photo(chat_id, open("./code.png", "rb"), caption=f'try code list Unsuccessful\n\n{str(possible_cases)}')
        try:
            driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div[2]/div[1]/div/div').click()
        except:
            pass

        with open("./code.txt", "w") as f:
            f.write("0")
        print("stream code entered...")
    except:
        print("stream code apply error")

def main():
    driver = ChromeDriver()
    driver.get(config['url'])

    sleep(5)
    try_close_msg(driver)

    print(f'Stream Youtube Link ===> ', get_stream_link(driver))

    refresh_time = 0

    while True:
        try:
            print("Check Energy ...")
            energy = driver.find_element("xpath", '//*[@id="app"]/div[1]/div[3]/div/div[1]/div/div[1]/div[2]/h4').text
            energy = int(energy)
            if energy > config['limit'] - 10:
                click(driver)
            
            code = open("./code.txt", "r").read()
            if not code == "0":
                try_stream_code(driver, code)
            sleep(10)
            refresh_time = refresh_time + 1
            if refresh_time > 60:
                print("Refresh Page, Waiting ...")
                driver.get(config['url'])
                refresh_time = 0
                sleep(15)

                try_close_msg(driver)
        except:
            driver.get(config['url'])
            sleep(15)
            try_close_msg(driver)
            print("Check Energy or Tapping Proccess Error !!")



    driver.quit()



Thread(target=main).start()
Thread(target=os.system("python3 youtube_stream.py"))