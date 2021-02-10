from selenium.webdriver.common.by import By

class MainPageLocators:

    email = (By.ID, 'email')
    password = (By.ID, 'pass')
    btn = (By.ID, 'u_0_d')
    ico = (By.CLASS_NAME, 'p361ku9c')
    profile_ico = (By.XPATH, '//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div[3]/div/div[2]/div/div/div/div[1]/a/div[1]/div')