import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException

def save_assignment(root_dir, title, html):
    pass

def save_chapter(root_dir, title, assignments):
    pass

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


        # Check that target is a Roppers course
        assert "Roppers Academy" in driver.title


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
            chapter_title = div.find_element(By.TAG_NAME, "h2")
            print(f"- {chapter_title.text}")

            # Expand chapter
            expand_toggle = div.find_element(By.CSS_SELECTOR, 'span:nth-last-child(1)')
            expand_toggle.click()
        
            lesson_lis = div.find_elements(By.TAG_NAME, "li")
            for li in lesson_lis:
                href = li.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                text = li.find_element(By.CSS_SELECTOR, "a > *:nth-last-child(1)").text.split('\n')[0].strip()
                print(f"  - {text} => {href}")

            print()

        input()

        # TODO: throttle download
        
        #course = Course(sys.argv[1], sys.argv[2])
        #with open(f"{sys.argv[1]}.html", "w") as fp:
        #    fp.write(str(course.soup))
        #assert "No results found." not in driver.page_source
        driver.close
