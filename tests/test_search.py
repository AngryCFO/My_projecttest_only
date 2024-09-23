import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="session")
def browser():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()


# Логин на сайт
def login(browser):
    browser.get("https://kobor.teslaserver.ru/")
    browser.find_element(By.NAME, "login").send_keys("only")
    browser.find_element(By.NAME, "password").send_keys("dev123only456" + Keys.RETURN)


# Тестирование функции поиска
@pytest.mark.parametrize("search_query", [
    "название товара",  # Полное совпадение
    "артикул товара",  # Поиск по артикулу
    "описание товара",  # Поиск по описанию
    "ошибочное слово",  # Тестирование исправления опечаток
    "tovar",  # Транслитерация
])
def test_search_functionality(browser, search_query):
    login(browser)

    # Найдем поле поиска
    search_field = browser.find_element(By.NAME, "search")  # Заменяем на реальный селектор поля поиска
    search_field.send_keys(search_query + Keys.RETURN)

    # Подождем и проверим результаты поиска
    results = browser.find_elements(By.CSS_SELECTOR, ".search-result")  # Заменяем на реальный селектор результатов
    assert len(results) > 0, f"По запросу '{search_query}' не найдено результатов"
