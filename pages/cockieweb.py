import pickle
from selenium import webdriver
from .base_page import BasePage

class MainPageCookie(BasePage):
    
    def read_cookie(self):
        for cookie in pickle.load(open('session', 'rb')):                                                           #чтение файла куков
            self.browser.add_cookie(cookie)                                         
        else:
            self.browser.refresh()
            print('\nИспользование прошлой сессии')