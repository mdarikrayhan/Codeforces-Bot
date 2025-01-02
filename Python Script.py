import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import logging

# Configure Logging
logging.basicConfig(
    filename="codeforces_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure WebDriver
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument(f"user-data-dir=/Users/mdarikrayhan/Library/Application Support/Google/Chrome") 
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
#chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

# User credentials
USERNAME = ""
PASSWORD = ""


def delay(min_seconds=1, max_seconds=3):
    """Introduce a random delay to mimic human behavior."""
    time.sleep(random.uniform(min_seconds, max_seconds))


def codeforces_login(driver, username, password):
    """Login to Codeforces and verify success."""
    logging.info("Starting login process...")
    driver.get("https://google.com")
    #driver.get("https://codeforces.com/enter")
    time.sleep(300)
    try:
        # Input credentials
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "handleOrEmail"))
        ).send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "submit").click()

        # Wait for the login to complete
        delay(2)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "lang-chooser")))

        # Confirm login by checking username visibility
        if username in driver.page_source:
            logging.info("Login successful.")
            return True
        else:
            logging.error("Login failed. Please check credentials.")
            return False

    except Exception as e:
        logging.error(f"Login failed with error: {e}")
        return False


def get_problems(url):
    """Fetch problems from a given Codeforces problemset page."""
    logging.info(f"Fetching problems from: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        problem_links = soup.find_all('a', href=lambda href: href and "/problemset/problem" in href)

        problems = []
        for link in problem_links:
            href = link['href']
            parts = href.split("/")
            number, problem_code = parts[-2], parts[-1]
            problems.append((f"https://codeforces.com/problemset/status/{number}/problem/{problem_code}",
                             f"{number}{problem_code}"))

        logging.info(f"Found {len(problems)} problems.")
        return problems
    except Exception as e:
        logging.error(f"Error fetching problems: {e}")
        return []


def submit_codeforces_solution(driver, language_value, problem_code, source_code):
    """Submit a solution to Codeforces."""
    logging.info(f"Attempting submission for problem: {problem_code}")
    driver.get("https://codeforces.com/problemset/submit")
    delay()

    try:
        # Select language
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "programTypeId"))
        ).send_keys(language_value)

        # Enter problem code
        driver.find_element(By.NAME, "submittedProblemCode").send_keys(problem_code)

        # Expand editor and enter source code
        driver.find_element(By.ID, "toggleEditorCheckbox").click()
        driver.execute_script("document.getElementById('sourceCodeTextarea').value = arguments[0];", source_code)

        # Submit the solution
        driver.find_element(By.ID, "singlePageSubmitButton").click()
        delay(2)

        # Confirm submission success
        if "My submissions" in driver.page_source:
            logging.info(f"Submission successful for problem: {problem_code}")
        else:
            logging.error(f"Submission may have failed for problem: {problem_code}")

    except Exception as e:
        logging.error(f"Error submitting solution for problem {problem_code}: {e}")


def main():
    if not codeforces_login(driver, USERNAME, PASSWORD):
        logging.error("Exiting script due to login failure.")
        driver.quit()
        return

    # Iterate through problem pages
    for page in range(1, 3):  # Adjust the range as needed
        url = f"https://codeforces.com/problemset/page/{page}?order=BY_RATING_ASC"
        problems = get_problems(url)

        for problem_url, problem_code in problems:
            logging.info(f"Processing problem: {problem_code}")

            # Use a dummy source code for testing
            source_code = (
                "#include <iostream>\nusing namespace std;\nint main() { cout << 'Hello, World!'; return 0; }"
            )

            try:
                submit_codeforces_solution(driver, "50", problem_code, source_code)
            except Exception as e:
                logging.error(f"Failed to process problem {problem_code}: {e}")

    driver.quit()


if __name__ == "__main__":
    main()