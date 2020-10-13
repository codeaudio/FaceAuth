from .pages.main_page import MainPage
from selenium.common.exceptions import NoAlertPresentException
import pytest
from selenium.webdriver.common.by import By
link = "https://www.facebook.com/" 

def test_authoriz_facebok(browser):
    page = MainPage(browser, link)
    page.open()
    page.test_auth(By.ID, 'u_0_b') 

def test_equal_page_to_url(browser):
    page = MainPage(browser, link)
    page.open() 
    page.test_loading_profile()
    