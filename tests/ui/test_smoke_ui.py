import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

@pytest.mark.ui
def test_ui_smoke_homepage_title(base_url):
    """Simple smoke test: proves Selenium + driver works locally."""
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    try:
        driver.get(f"{base_url}/products")
        assert "Tiny Shop" in driver.title
        # Verify at least one product card renders
        cards = driver.find_elements(By.CSS_SELECTOR, "[data-testid='product-card']")
        assert len(cards) >= 1
    finally:
        driver.quit()
