from django.test import TestCase, LiveServerTestCase
from django.urls import reverse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from .models import Fight

class PokemonsViewTest(TestCase):

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_show_pokemon(self):
        response = self.client.get(reverse('show_pokemon', args=['venusaur']))
        self.assertEqual(response.status_code, 200)

    def test_poke_fights(self):
        self.assertEqual(len(Fight.objects.all()), 0)
        response = self.client.get(reverse('poke_fights', args=['venusaur']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Fight.objects.all()[0].fightid, 1)
        self.assertEqual(Fight.objects.all()[0].fighter_f, 80)
        h = Fight.objects.all()[0].fighter_s

        response2 = self.client.post(reverse('poke_fights', args=['venusaur']),
                                    { 'hit': 3})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(Fight.objects.all()), 1)
        self.assertEqual(Fight.objects.all()[0].fightid, 1)
        self.assertEqual(Fight.objects.all()[0].fighter_f, 80)
        self.assertEqual(Fight.objects.all()[0].fighter_s, h-82)
        self.assertTemplateUsed(response, 'poke_fights.html')

class SeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_index(self):

        self.selenium.get(f"{self.live_server_url}/")
        WebDriverWait(self.selenium, 30).until(
        lambda driver: driver.find_element(By.TAG_NAME, "body")
    )
        self.assertEqual("Pokemons", self.selenium.title)
        self.assertIn("Fights", self.selenium.find_element(By.XPATH, "//*[contains(text(), 'Pokemons Fights')]").text)


    def test_show_pokemon(self):
        self.selenium.get(f"{self.live_server_url}/pokemon/venusaur")
        WebDriverWait(self.selenium, 20).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        self.assertEqual("Имя: venusaur", self.selenium.find_element(By.XPATH, ".//*[contains(text(), 'venusaur')]").text)
        self.assertEqual("Выбрать для боя",
                      self.selenium.find_element(By.XPATH, "//*[@class='btn btn-primary']").text)


    def test_fight(self):
        self.selenium.get(f"{self.live_server_url}/pokemon/venusaur/fight")
        WebDriverWait(self.selenium, 20).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )

        user_input = self.selenium.find_element(By.ID, "hit")
        user_input.send_keys("3")

        self.selenium.find_element(By.XPATH, "/html/body/div/div/div[3]/form/div[2]/input").click()

        WebDriverWait(self.selenium, 20).until(
            lambda driver:  driver.find_element(By.TAG_NAME, "body")
        )

        self.assertIn("Выйграл", self.selenium.find_element(By.XPATH, "//*[@class='me-3 fw-semibold']").text)


    def test_search(self):
        self.selenium.get(f"{self.live_server_url}/")
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        search_input = self.selenium.find_element(By.NAME, "name")
        search_input.send_keys("s")

        self.selenium.find_element(By.XPATH, "/html/body/header/div/form/button").click()
        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )
        self.assertIn("squirtle",
                      self.selenium.find_element(By.XPATH, "//*[@class='card-title']").text)