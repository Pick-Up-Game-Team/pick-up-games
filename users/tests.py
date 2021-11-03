from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from chromedriver_py import binary_path
from .models import Profile
from django.contrib.auth.models import User

class TestLoginpage(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'Testing123!'

        # Set up browser
        self.driver = webdriver.Chrome(executable_path=binary_path)
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1936, 1056)

        # Create account
        user = User.objects.create_user(self.username, f'{self.username}@email.com', self.password)
        self.user = Profile.objects.create(user=user)

    def tearDown(self):
        self.driver.quit()

    def test_loginpage(self):

        # Go to login page
        self.driver.find_element_by_link_text('Login').click()
        self.driver.implicitly_wait(0.1)

        # Test that the created user exists
        try:
            user_obj = Profile.objects.get(user__username=self.username)
        except Profile.DoesNotExist:
            user_obj = None
        self.assertIsNotNone(user_obj)
        
        # Test that the user is not logged in (there should not be a log out button)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element(By.LINK_TEXT, "Log Out")

        # Enter and submit login credentials to log in
        self.driver.find_element(By.ID, "id_username").send_keys(self.username)
        self.driver.find_element(By.ID, "id_password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
        
        self.driver.implicitly_wait(0.1)

        # Test that the user is logged in (there should not be a login or register button)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Login')
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Register')

        # Log out
        self.driver.find_element(By.LINK_TEXT, "Log Out").click()
        self.driver.implicitly_wait(0.1)

        # Test that the user is not logged in (there should not be a log out button)
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element_by_link_text('Log Out')
