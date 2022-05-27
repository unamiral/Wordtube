from webdriver_manager.firefox import GeckoDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import requests
import random
import time
from gtts import gTTS
from PIL import Image, ImageFont, ImageDraw
import os
import subprocess


def make_image(word):
    # "L": (8-bit pixels, black and white)
    img = Image.new("L", (1080, 1920), color="white")
    font = ImageFont.truetype("font/NewspaperRegular-51R0a.ttf", 200)
    font2 = ImageFont.truetype("font/NewspaperRegular-51R0a.ttf", 75)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(word, font=font)
    w1, h1 = draw.textsize("Like and Subscribe :)", font=font)
    draw.text(((1080-w)/2, (1920-h)/2), text=word, fill='black', font=font)
    draw.text((330, 1500), text="Like and Follow!", fill='black', font=font2)
    img.save('tmp/tmp.png')


def tts(name):
    x1 = gTTS(name, lang="en", slow=False)
    x2 = gTTS(name, lang="en", slow=True)
    x3 = gTTS(name, lang="en", slow=True)
    with open('bonjour_sara.mp3', 'wb') as f:
        x1.write_to_fp(f)
        x2.write_to_fp(f)
        x3.write_to_fp(f)



# =================================================

print('=====================================================================================================')
print('Heyy, you have to login manully on tiktok, so the bot will wait you 1 minute for loging in manually!')
print('=====================================================================================================')
time.sleep(8)
print('Running bot now, get ready and login manually...')
time.sleep(4)

options = webdriver.ChromeOptions()
bot = webdriver.Chrome(options=options,  executable_path=CM().install())
bot.set_window_size(1680, 900)

bot.get('https://www.tiktok.com/login')
ActionChains(bot).key_down(Keys.CONTROL).send_keys(
    '-').key_up(Keys.CONTROL).perform()
ActionChains(bot).key_down(Keys.CONTROL).send_keys(
    '-').key_up(Keys.CONTROL).perform()
print('Waiting 50s for manual login...')
time.sleep(50)
bot.get('https://www.tiktok.com/upload/?lang=en')
time.sleep(3)


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True


def upload(video_path):
    file_uploader = bot.find_element_by_xpath(
        '//*[@id="main"]/div[2]/div/div[2]/div[2]/div/div/input')

    file_uploader.send_keys(video_path)

    caption = bot.find_element_by_xpath(
        '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div/div/div/span')

    bot.implicitly_wait(10)
    ActionChains(bot).move_to_element(caption).click(
        caption).perform()
    # ActionChains(bot).key_down(Keys.CONTROL).send_keys(
    #     'v').key_up(Keys.CONTROL).perform()

    with open(r"caption.txt", "r") as f:
        tags = [line.strip() for line in f]

    for tag in tags:
        ActionChains(bot).send_keys(tag).perform()
        time.sleep(2)
        ActionChains(bot).send_keys(Keys.RETURN).perform()
        time.sleep(1)

    time.sleep(5)
    bot.execute_script("window.scrollTo(150, 300);")
    time.sleep(5)

    post = WebDriverWait(bot, 100).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="main"]/div[2]/div/div[2]/div[3]/div[5]/button[2]')))

    post.click()
    time.sleep(30)

    if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))

        reupload.click()
    else:
        print('Unknown error cooldown')
        while True:
            time.sleep(600)
            post.click()
            time.sleep(15)
            if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
                break

    if check_exists_by_xpath(bot, '//*[@id="portal-container"]/div/div/div[1]/div[2]'):
        reupload = WebDriverWait(bot, 100).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="portal-container"]/div/div/div[1]/div[2]')))
        reupload.click()




#================================================================
with open('words', 'r') as fr:
    data = fr.readlines()
    for line in data:
        tts(line)
        make_image(line)
        os.system("ffmpeg -loop 1 -i tmp/tmp.png -i bonjour_sara.mp3 -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest tmp/tmp.mp4")
        time.sleep(25)
        upload("tmp/tmp.mp4")
        os.system("rm tmp/tmp.mp4")