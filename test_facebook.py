from pages.main_page import MainPage
import pytest
from selenium.webdriver.common.by import By

link = "https://www.facebook.com/"


@pytest.mark.user_login
class TestGoToUserPage:

    def test_authoriz_facebok(self, browser):
        page = MainPage(browser, link)
        page.open()
        page.test_auth(By.ID, 'u_0_d')

    def test_equal_page_to_url(self, browser):
        page = MainPage(browser, link)
        page.open()
        page.test_loading_profile()
