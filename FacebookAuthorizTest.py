from selenium import webdriver
import fake_useragent
import pickle
import time
import pytest
from selenium.webdriver.chrome.options import Options
from cryptography.fernet import Fernet
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

link = "https://www.facebook.com/"                                                                                  #ссылка на тестируемую страницу

data = {                                                                                                            #словаь с данными для входа
'email': 'nicehotgame@gmail.com',                                                                                   #логин
'pass': b'gAAAAABfdDKhHAJG-J6XxjE4N-8ODSmwmU7FGZqvCPV8pjlbNUWvXad5Dg7K9mGX3AFlAGI4c2NoMumgQj3tO8Uaj77flRai_w=='     #зашифрованный пароль
}

@pytest.fixture
def browser():
    print("\nstart browser for test..")
    options = Options()
    user_agent = fake_useragent.UserAgent() 
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'       #фейковый юзер агент
    options.add_argument(f'user-agent={user_agent}')                                                                                         #добавление фейкового юзер агента
    print(user_agent)
    browser = webdriver.Chrome(options=options)                                                                                              #добавление опции хрому
    browser.implicitly_wait(5)
    browser.get(link) 
    yield browser                                                                                                                           # этот код выполнится после завершения теста
    pickle.dump(browser.get_cookies(), open('session','wb'))                                                                           #сохранение куков(сессии)
    time.sleep(2)
    browser.get_screenshot_as_file('screen.png')
    print("\nquit browser...")
    browser.quit()

class TestFacebook(): 

    def test_auth(self,browser):
        try:      
            for cookie in pickle.load(open('session','rb')):                                                             #чтение файла куков
                browser.add_cookie(cookie)
            else:
                browser.refresh()     
                print('\nИспользование прошлой сессии')    
                
        except FileNotFoundError:                                                                                        #если файла не существуетб то исполнить блок вводы данных       
            cipher_key = b'HfASIcnseLe1xKEF244_yEqV_OM9R3tQO_P4ZR7bY00='                                                 #ключ для расшифровки

            encrypted_text = data['pass']                                                                                #строка парля из словаря

            cipher = Fernet(cipher_key)
            decrypted_text = cipher.decrypt(encrypted_text)                                                              #расшифровка пароля
                                        
            email = browser.find_element_by_id('email')     
            email.send_keys(data['email'])                                                                               #ввод логина

            password = browser.find_element_by_id('pass')    
            password.send_keys(bytes.decode(decrypted_text, 'utf-8'))                                                    #ввод пароля и перевод из bytes в str

            btn =WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.ID,'u_0_b'))
                )
            btn.click()                                                                                                  #клик по кнопке вход    
            print('\nВход в профиль')

if __name__ == "__main__":

    TestFacebook()
    
