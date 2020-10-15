from selenium import webdriver
import pickle, time, pytest, os
from cryptography.fernet import Fernet
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
from .locators import MainPageLocators
from .cockieweb import MainPageCookie
                                                                                
data = {                                                                                                            #словаь с данными для входа
'email': 'nicehotgame@gmail.com',                                                                                   #логин
'pass': b'gAAAAABfdDKhHAJG-J6XxjE4N-8ODSmwmU7FGZqvCPV8pjlbNUWvXad5Dg7K9mGX3AFlAGI4c2NoMumgQj3tO8Uaj77flRai_w=='     #зашифрованный пароль
}

class MainPage(BasePage): 
    
    @pytest.mark.smoke 
    def test_auth(self, how, what, timeout = 0):                                                                                     #тест входа на страницу и сохранение сессии 
        try:      
            MainPageCookie.read_cookie(self)
        except FileNotFoundError:                                                                                        #если файла не существует, то исполнить блок вводы данных       
            cipher_key = b'HfASIcnseLe1xKEF244_yEqV_OM9R3tQO_P4ZR7bY00='                                                 #ключ для расшифровки
            encrypted_text = data['pass']                                                                                #строка парля из словаря
            cipher = Fernet(cipher_key)
            decrypted_text = cipher.decrypt(encrypted_text)                                                              #расшифровка пароля
                                        
            email = self.browser.find_element(*MainPageLocators.email)  
            email.send_keys(data['email'])                                                                               #ввод логина

            password = self.browser.find_element(*MainPageLocators.password)    
            password.send_keys(bytes.decode(decrypted_text, 'utf-8'))                                                    #ввод пароля и перевод из bytes в str

            btn = WebDriverWait(self.browser, 4).until(
                EC.element_to_be_clickable((how, what)))
            btn.click()                                                                                                  #клик по кнопке вход  
            try:                                                                                                         
                assert self.browser.find_element(*MainPageLocators.ico)
                pickle.dump(self.browser.get_cookies(), open('session','wb'))                                            #сохранение куков(сессии)
                self.browser.get_screenshot_as_file('screen_start_page.png')
                print('\nВход в профиль')
                print('\nСохранение сессии')
            except NoSuchElementException:
                raise
                
    @pytest.mark.smoke
    def test_loading_profile(self):                                                                                      #тест загрузки профиля
        try:
            assert os.path.isfile('session')                                                                             #проверка сохраненной сессии
            MainPageCookie.read_cookie(self)
            print('\nИспользование прошлой сессии') 
            time.sleep(1)  
            profile_ico = self.browser.find_element(*MainPageLocators.profile_ico)
            profile_ico.click()                                                                                          #на страницу профиля
            time.sleep(1)
            current_page_url = self.browser.current_url
            assert current_page_url == "https://www.facebook.com/profile.php?id=100009451024270"                         #проверка соотвествия url
            print('\nСтраница профиля загружена') 
        except (AssertionError, NoSuchElementException, FileNotFoundError):                                              #обработка исключений 
            try:
                os.remove(r'session')                                                                                    #удаление куков
                raise
            except FileNotFoundError:                                                                                    #проверка отсутвия файла куков
                pytest.skip('Тест загрузки страницы пропущен')                                                           #пропуск теста
           


    


