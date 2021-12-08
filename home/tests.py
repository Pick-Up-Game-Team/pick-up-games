from django.test import TestCase, Client, override_settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from chromedriver_py import binary_path

from django.contrib.auth.models import User
from .models import Court

class TestHomepage(TestCase):
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_homepage(self):
        chrome_options = Options()
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.implicitly_wait(10)
        browser.get("http://127.0.0.1:8000/")
        yield browser

        self.driver.find_element(By.LINK_TEXT, "Register").click()
        # 3 | click | linkText=Login |
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        # 4 | click | linkText=Register |
        self.driver.find_element(By.LINK_TEXT, "Register").click()

        browser.quit()

@override_settings(DEBUG=True)
class TestCourts(StaticLiveServerTestCase):
    def setUp(self):
        """
        Set up test environment (runs once per test function)
        """
        # Inherit setUp()
        super().setUp()
        
        # Set up Chrome web driver and test client
        self.client = Client()
        self.driver = WebDriver(executable_path=binary_path)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.implicitly_wait(5)
        self.driver.set_window_size(1936, 1056)
        self.driver.get(f'{self.live_server_url}')
        
        # Define variables
        self.username = 'testuser'
        self.password = 'Testing123!'

        # Create account
        user = User.objects.create_user(username=self.username,
                                        email=f'{self.username}@email.com',
                                        password=self.password)

    def tearDown(self):
        """
        Destroy test environment (run once per test function)
        """
        # Inherit tearDown()
        super().tearDown()
        self.driver.quit()

    def test_loginpage(self):
        """
        Test login page functionality
        """
        
        # Check courts list
        self.driver.find_element(By.LINK_TEXT, "Courts").click()
        self.driver.find_element(By.LINK_TEXT, "C.C. Jackson").click()
        court = Court.objects.get(name="C.C. Jackson")
        url = self.driver.current_url
        pk = court.pk
        self.assertEqual(url, f'{self.live_server_url}/courts/{pk}/')
        
        self.driver.find_element(By.LINK_TEXT, "Courts").click()
        self.driver.find_element(By.LINK_TEXT, "Edgewood-Lyndhurst").click()
        court = Court.objects.get(name="Edgewood-Lyndhurst")
        url = self.driver.current_url
        pk = court.pk
        self.assertEqual(url, f'{self.live_server_url}/courts/{pk}/')
        
        # Log in
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        self.driver.find_element(By.ID, "id_username").send_keys(self.username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn-outline-info").click()
        
        # Check courts list while logged in
        self.driver.find_element(By.LINK_TEXT, "Courts").click()
        self.driver.find_element(By.LINK_TEXT, "C.C. Jackson").click()
        court = Court.objects.get(name="C.C. Jackson")
        url = self.driver.current_url
        pk = court.pk
        self.assertEqual(url, f'{self.live_server_url}/courts/{pk}/')
        
        self.driver.find_element(By.LINK_TEXT, "Courts").click()
        self.driver.find_element(By.LINK_TEXT, "Edgewood-Lyndhurst").click()
        court = Court.objects.get(name="Edgewood-Lyndhurst")
        url = self.driver.current_url
        pk = court.pk
        self.assertEqual(url, f'{self.live_server_url}/courts/{pk}/')
        