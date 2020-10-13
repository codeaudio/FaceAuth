from selenium import webdriver
import fake_useragent, time, pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default= 'chrome',
                     help="Dedault browser: chrome. You can choose a browser: chrome/firefox")
    parser.addoption('--language_name', action='store', default= 'en',
                     help="Dedault browser: ru")

@pytest.fixture(scope="module") 
def browser(request):
    print("\nstart browser for test..")
    options = Options()
    browser_name = request.config.getoption("browser_name")
    language_name = request.config.getoption("language_name")
    #options.headless = True                                                                                                                
    #options.add_argument("--disable-gpu")
    #options.add_argument("--disable-extensions")
    user_agent = fake_useragent.UserAgent() 
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'      #фейковый юзер агент
    prefs = {'intl.accept_languages': language_name,
    "profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument(f'user-agent={user_agent}')                                                                                        #добавление фейкового юзер агента
    fp = webdriver.FirefoxProfile()
    fp_notifoff = ("profile.default_content_setting_values.notifications", 2)
    fp_lan = ('intl.accept_languages', language_name)
    fp.set_preference(fp_notifoff, fp_lan)
    print(user_agent)                                                                                      
    if browser_name == "chrome":
        print("\nstart chrome browser for test..")
        browser = webdriver.Chrome(options=options)                                                                                         #добавление опции хрому
    elif browser_name == "firefox":
        print("\nstart firefox browser for test..")
        browser = webdriver.Firefox(firefox_profile=fp)  
    else:
        raise pytest.UsageError("--browser_name should be chrome/firefox")
    browser.implicitly_wait(5)
     
    yield browser                                                                                                                           #этот код выполнится после завершения теста
    time.sleep(1)                                                                                                                           
    browser.get_screenshot_as_file('screen_last_page.png')
    print("\nquit browser...")
    browser.quit()
