import sys
import time
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def save_file(path: Path, filename: str, data):
    with Path(path, filename).open("w") as fp:
        fp.write(data)

def save_lesson_as_html(dir, chapter_title, lesson_title, html):
    path = Path(f'./{dir}/{chapter_title}/')
    path.mkdir(parents=True, exist_ok=True)
    save_file(path, f"{lesson_title}.html", html)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ./scrape.py dir https://www.roppers.org")
        print("Provide login creds via env vars THINKFIC_USER and THINKFIC_PASS")
    else:
        try:
            THINKFIC_USER = os.environ["THINKFIC_USER"]
            THINKFIC_PASS = os.environ["THINKFIC_PASS"]
        except KeyError:
            print("[!] A username and password are required to login to the course page.")
            print("[!] Please provide values for the env vars THINKFIC_USER and THINKFIC_PASS and try again.")
            exit(1)

        save_dir = sys.argv[1]
        course_url = sys.argv[2]

        # Intialize Selenium browser driver
        opts = ChromeOptions()
        opts.add_argument("--window-size=1600,900")
        driver = webdriver.Chrome(options=opts)
        driver.implicitly_wait(1)
        driver.get(course_url)


        # Navigate to sign in page
        sign_in_btn = driver.find_element(By.LINK_TEXT, "SIGN IN")
        sign_in_btn.click()


        # Login in to target Thinkfic course page
        user_input = driver.find_element(By.ID, "user[email]")
        user_input.send_keys(THINKFIC_USER)
        pass_input = driver.find_element(By.ID, "user[password]")
        pass_input.send_keys(THINKFIC_PASS)

        submit_btn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        print("Waiting for login process...")
        submit_btn.click()
        input("Press ENTER when courses page has loaded.")


        # Select Thinkfic course from dashboard
        course_anchors = driver.find_elements(By.CSS_SELECTOR, 'ul[class="products__list"] div[class="card__header"] > a')
        print(course_anchors)

        print("The following courses were found:")
        for i,anchor in enumerate(course_anchors):
            href = anchor.get_attribute("href")
            text = anchor.get_attribute("text")
            print(f"- {i}: {text.strip()} => {href}")


        index = input("Select a course number: ")

        print("Navigating to course...")
        driver.get(course_anchors[int(index)].get_attribute("href"))
        input("Press ENTER when the course page has loaded.")
        

        # Navigate lessons by chapter and save source files
        chapter_divs = driver.find_elements(By.CSS_SELECTOR, 'div[class="course-player__chapters-menu "] > div')

        for div in chapter_divs:
            chapter_title = div.find_element(By.TAG_NAME, "h2").text
            # print(f"- {chapter_title}")

            # Expand chapter
            expand_toggle = div.find_element(By.CSS_SELECTOR, 'span:nth-last-child(1)')
            expand_toggle.click()

            # TODO: replace time.sleep with Explicit Wait
            time.sleep(1)

            lesson_lis = div.find_elements(By.TAG_NAME, "li")
            for li in lesson_lis:
                href = li.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                title = li.find_element(By.CSS_SELECTOR, "a > *:nth-last-child(1)").text.split('\n')[0].strip()
                #print(f"  - {title} => {href}")

                li.click() # open lesson content
                ## TODO: replace time.sleep with Explicit Wait
                time.sleep(0.25)

                html = driver.find_element(By.ID, "content-inner").get_attribute("innerHTML")
                save_lesson_as_html(save_dir, chapter_title, title, html)

            print(f"[!] Saved chapter: {chapter_title}")

        # TODO: throttle download
        driver.close
