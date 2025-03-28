import logging
import time
from pathlib import Path

import clerk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

logging.basicConfig(level=logging.INFO, handlers=[clerk.rich_handler()])
log = logging.getLogger(__name__)
# config driver
download_dir = Path(__file__).parents[2] / "temp" / "pureref"
options = EdgeOptions()
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": str(download_dir),
        "download.directory_upgrade": True,
        "download_parallel": True,  # Enable parallel downloads
        "download_max_connections": 8,  # Number of parallel connections
    },
)
options.add_argument("--force-device-scale-factor=0.5")
options.add_argument("--headless=new")
driver = webdriver.Edge(options=options)
driver.set_window_size(2160, 4096)

# open web
driver.get("https://www.pureref.com/download.php")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[@id='buildSelect']/label/div/span/select")
    )
)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "amount")))
element = driver.find_element(By.ID, "personalSelector")
driver.execute_script("arguments[0].scrollIntoView();", element)
time.sleep(5)

# choose win portable
element = driver.find_element(
    By.XPATH, "//div[@id='buildSelect']/label/div/span/select"
)
log.info("click drop down menu")
select_element = Select(element)
select_element.select_by_index(1)
log.info("select windows portable")

# set price
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "customAmount")))
element = driver.find_element(By.ID, "customAmount")
element.click()
log.info("click custom amount")
element = driver.find_element(By.NAME, "amount")
element.clear()
element.send_keys("0")
log.info("set amount to zero")
driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", element)

# download
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, """//*[@id="freeDownload"]/button"""))
)
element = driver.find_element(By.XPATH, """//*[@id="freeDownload"]/button""")
element.click()
log.info("start download")

# Wait for file to appear
max_wait = 100  # seconds
waited = 0
while waited < max_wait:
    if len(list(download_dir.glob("*.zip"))):
        break
    time.sleep(1)
    waited += 1
else:
    raise TimeoutError("File didn't download in time")
log.info("finish download")
