from selenium import webdriver
import time
import fake_useragent
import pickle
from selenium.webdriver.chrome.options import Options
from cryptography.fernet import Fernet
link = "https://www.facebook.com/"

data = {
'email': '89031106963',
'pass': b'gAAAAABfdDKhHAJG-J6XxjE4N-8ODSmwmU7FGZqvCPV8pjlbNUWvXad5Dg7K9mGX3AFlAGI4c2NoMumgQj3tO8Uaj77flRai_w=='
}
cipher_key = b'HfASIcnseLe1xKEF244_yEqV_OM9R3tQO_P4ZR7bY00='
print(cipher_key) 

encrypted_text = data['pass']

cipher = Fernet(cipher_key)
decrypted_text = cipher.decrypt(encrypted_text)

decode_pass = bytes.decode(decrypted_text, 'utf-8')

try:
    options = Options()
    user_agent = fake_useragent.UserAgent()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(chrome_options=options)
    print(user_agent)
    browser.get(link)
    try:
        for cookie in pickle.load(open('session','rb')):
           browser.add_cookie(cookie)
    except FileNotFoundError:
        
        email = browser.find_element_by_id('email')
        email.send_keys(data['email'])

        password = browser.find_element_by_id('pass')
        password.send_keys(decode_pass)

        btn = browser.find_element_by_id('u_0_b')
        btn.click()
        time.sleep(3)
        pickle.dump(browser.get_cookies(), open('session','wb'))
    
    else:
        
        browser.refresh()
    
    time.sleep(3)
    
finally:

    time.sleep(5)

    browser.quit()