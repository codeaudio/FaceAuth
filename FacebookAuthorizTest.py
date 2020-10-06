from selenium import webdriver
import fake_useragent, pickle, time, pytest, os
from selenium.webdriver.chrome.options import Options
from cryptography.fernet import Fernet
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
link = "https://www.facebook.com/"                                                                                  #ссылка на тестируемую страницу

data = {                                                                                                            #словаь с данными для входа
'email': 'nicehotgame@gmail.com',                                                                                   #логин
'pass': b'gAAAAABfdDKhHAJG-J6XxjE4N-8ODSmwmU7FGZqvCPV8pjlbNUWvXad5Dg7K9mGX3AFlAGI4c2NoMumgQj3tO8Uaj77flRai_w=='     #зашифрованный пароль
}

@pytest.fixture(scope="class")
def browser():
    print("\nstart browser for test..")
    options = Options()
    #options.headless = True                                                                                                                
    #options.add_argument("--disable-gpu")
    #options.add_argument("--disable-extensions")
    user_agent = fake_useragent.UserAgent() 
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'      #фейковый юзер агент
    notific = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",notific)
    options.add_argument(f'user-agent={user_agent}')                                                                                        #добавление фейкового юзер агента
    print(user_agent)
    browser = webdriver.Chrome(options=options)                                                                                             #добавление опции хрому
    browser.implicitly_wait(5)
    browser.get(link) 
    yield browser                                                                                                                           #этот код выполнится после завершения теста
    time.sleep(1)                                                                                                                           
    browser.get_screenshot_as_file('screen_last_page.png')
    print("\nquit browser...")
    browser.quit()

class TestFacebook(): 

    def test_auth(self, browser):                                                                                         #тест входа на страницу и сохранение сессии 
        try:      
            for cookie in pickle.load(open('session', 'rb')):                                                             #чтение файла куков
                    browser.add_cookie(cookie)                                         
            else:
                browser.refresh()
                print('\nИспользование прошлой сессии')  
        except FileNotFoundError:                                                                                        #если файла не существует, то исполнить блок вводы данных       
            cipher_key = b'HfASIcnseLe1xKEF244_yEqV_OM9R3tQO_P4ZR7bY00='                                                 #ключ для расшифровки

            encrypted_text = data['pass']                                                                                #строка парля из словаря

            cipher = Fernet(cipher_key)
            decrypted_text = cipher.decrypt(encrypted_text)                                                              #расшифровка пароля
                                        
            email = browser.find_element_by_id('email')     
            email.send_keys(data['email'])                                                                               #ввод логина

            password = browser.find_element_by_id('pass')    
            password.send_keys(bytes.decode(decrypted_text, 'utf-8'))                                                    #ввод пароля и перевод из bytes в str

            btn = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.ID,'u_0_b'))
                )
            btn.click()                                                                                                  #клик по кнопке вход  
            try:                                                                                                         
                assert browser.find_element_by_class_name('p361ku9c')
                pickle.dump(browser.get_cookies(), open('session','wb'))                                                 #сохранение куков(сессии)
                browser.get_screenshot_as_file('screen_start_page.png')
                print('\nВход в профиль')
                print('\nСохранение сессии')
            except NoSuchElementException:
                raise
                
    def test_loading_profile(test_auth, browser):                                                                        #тест загрузки профиля
        try:
            assert os.path.isfile('session')
            time.sleep(2)  
            profile_ico = browser.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[3]/div/div[2]/div/div/div/div[1]/a/div[1]/div')
            profile_ico.click()
            time.sleep(1)
            current_page_url = browser.current_url
            assert current_page_url == "https://www.facebook.com/profile.php?id=100009451024270"
            print('\nСтраница профиля загружена') 
        except (AssertionError, NoSuchElementException, FileNotFoundError):
            try:
                os.remove(r'session')
                raise
            except FileNotFoundError:
                pytest.skip('Тест загрузки страницы пропущен')
           
if __name__ == "__main__":

    TestFacebook()
