from __future__ import annotations

import re
import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import check_content_question


class LinkareerCoverLetterScraper:
    """
    A class to scrape cover letters from a website.

    """

    def __init__(self, log, background):
        """
        Initializes the scraper with a logger and necessary data structures.

        Parameters:
            log (logging.Logger): The logger for logging messages.
        """
        self.options = webdriver.ChromeOptions()
        if background:
            self.options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.options)
        self.log = log
        self.wait = WebDriverWait(self.driver, 10)
        self.questions = []
        self.cover_letter_contents = []
        self.college_category = []
        self.company = []
        self.job = []
        self.period = []
        self.major = []
        self.grade = []
        self.language = []
        self.experience = []
        self.etc = []
        self.data_path = []
        self.pass_data = []

    def open_website(self, url):
        """
        Opens the given URL in the browser.

        Parameters:
            url (str): The URL of the website to open.
        """
        self.driver.get(url)
        self.log.info(f"Website opened: {url}")

    def close_browser(self):
        """
        Closes the browser.
        """
        self.driver.quit()
        self.log.info("Browser closed")

    def scrape_data(self):
        """
        Scrapes data from the website and processes each cover letter.
        """
        page = 2
        total_page = 1

        try:
            # Move to the first cover letter page
            try:
                next_button_xpath = '//*[@id="__next"]/div[1]/div/div[4]/div/div/section[1]/div[2]/div/div[3]/div[1]/div[1]/div[1]/a/div/div'
                next_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, next_button_xpath))
                )
                next_button.click()
                self.log.info("Base Page Loaded")
                time.sleep(2)
            except Exception:
                ActionChains(self.driver).scroll_by_amount(0, 20).perform()
                time.sleep(1)
            # airflow_test
            airflow_test_flag = True
            while airflow_test_flag:
                self.driver.implicitly_wait(10)

                # Move to the next page
                while True:
                    try:
                        next_page_xpath = '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div/div[1]/div/div[2]/div[20]/a/div'

                        next_page_button = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, next_page_xpath))
                        )
                        time.sleep(2)
                        self.log.info("Scrolled down")
                        break
                    except Exception:
                        ActionChains(self.driver).scroll_by_amount(0, 20).perform()
                        time.sleep(1)

                time.sleep(1)
                self.log.info("Page Scrolled")

                page_xpath = f'//*[@id="__next"]/div[1]/div[4]/div/div[2]/div/div[1]/div/div[2]/div[21]/div/div[1]/button[{page}]'
                page_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, page_xpath))
                )
                page_button.click()
                time.sleep(1)
                self.log.info("Moving on to the next page")
                self.driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                # Find out all cover letter in the page
                for i in range(1, 21):
                    self.driver.implicitly_wait(1)
                    while True:
                        try:
                            next_page_xpath = f'//*[@id="__next"]/div[1]/div[4]/div/div[2]/div/div[1]/div/div[2]/div[{i}]/a/div'
                            next_page_button = self.wait.until(
                                EC.element_to_be_clickable((By.XPATH, next_page_xpath))
                            )
                            next_page_button.click()
                            time.sleep(2)
                            self.log.info("Moving on to the next cover letter example")
                            break
                        except Exception:
                            ActionChains(self.driver).scroll_by_amount(0, 20).perform()
                            time.sleep(1)

                    info, cover_letter_content = self.extract_info()
                    self.process_info(info, cover_letter_content)

                self.log.info(f"page: {total_page} data crawling is done")
                page = (page + 1) % 8
                total_page += 1
                if page == 1 or page == 0:
                    page = 3
                    
                airflow_test_flag = False 

        except NoSuchElementException:
            ActionChains(self.driver).scroll_by_amount(0, 20).perform()
            self.log.error(
                "All requested data scraping tasks have been successfully completed"
            )

    def extract_info(self):
        """
        Extracts personal information from the current cover letter page.

        Returns:
            tuple: Contains the extracted information(Career, University, language, certificate, etc) and cover letter content.
        """
        info = None
        cover_letter_content = None
        while True:
            try:
                # company, period, job
                info_xpath = '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/h1'
                info = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, info_xpath))
                ).text.split(" / ")
                break
            except TimeoutException:
                self.scroll_page()

        while True:
            try:
                # university, major, grade, certificate, language, experience, etc,
                personal_info_xpath = '//*[@id="__next"]/div[1]/div[4]/div/div[2]/div/div[2]/div[1]/div/div/div[3]/h3'
                personal_info = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, personal_info_xpath))
                ).text.split(" / ")
                info += personal_info
                break
            except TimeoutException:
                self.scroll_page()

        while True:
            try:
                # Setup for the cover letter and question division
                cover_letter_xpath = '//*[@id="coverLetterContent"]/main'
                cover_letter_content = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, cover_letter_xpath))
                ).text.split("\n")
                break
            except TimeoutException:
                self.scroll_page()

        return [item for item in info if item], [
            item for item in cover_letter_content if item
        ]

    def scroll_page(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        ActionChains(self.driver).scroll_by_amount(0, 20).perform()
        time.sleep(1)

    def process_info(self, info, cover_letter_content):
        """
        Processes the extracted information for csv file and adds it to the respective lists.

        Parameters:
            info (list): List of extracted information.
            cover_letter_content (list): List of cover letter content.
        """
        question_content_dict = dict()
        index = ""
        for text in cover_letter_content:
            if check_content_question(text):
                question_content_dict[text] = ""
                index = text
            else:
                if len(index) >= 1:
                    question_content_dict[index] += text

        language_spec = ""
        experience_spec = ""
        etc_spec = ""

        # If there is a college category data, extract experience, language, etc from pattern
        if len(info) >= 6:
            for data in info[5:]:
                pattern_lang = r"토익|OPIC|토익스피킹|오픽|OPIC|토스|토익 스피킹"
                pattern_exp = r"사회생활"
                if re.search(pattern_lang, data):
                    language_spec += data + " "
                else:
                    if re.search(pattern_exp, data):
                        experience_spec += data + " "
                    else:
                        etc_spec += data + " "
        # If there isn't any college data in the information
        else:
            for data in info[3:]:
                pattern_lang = r"토익|OPIC|토익스피킹|오픽|OPIC|토스|토익 스피킹"
                pattern_exp = r"사회생활"
                if re.search(pattern_lang, data):
                    language_spec += data + " "
                else:
                    if re.search(pattern_exp, data):
                        experience_spec += data + " "
                    else:
                        etc_spec += data + " "

        if question_content_dict.items():
            for question, content in question_content_dict.items():
                self.questions.append(question)
                self.cover_letter_contents.append(content)
                self.company.append(info[0])
                self.job.append(info[1])
                self.period.append(info[2])
                if len(info) >= 6:
                    self.college_category.append(info[3])
                    self.major.append(info[4])
                    self.grade.append(info[5])
                else:
                    self.college_category.append("")
                    self.major.append("")
                    self.grade.append("")
                self.language.append(language_spec.rstrip())
                self.experience.append(experience_spec.rstrip())
                self.etc.append(etc_spec.rstrip())

        self.log.info(f"{info[0]} cover letter data crawling is done")

    def convert_to_DataFrame(self):
        """
        Convert into DataFrame
        """
        self.pass_data = pd.DataFrame(
            {
                "문항(키워드)": self.questions,
                "자기소개서": self.cover_letter_contents,
                "회사": self.company,
                "직무": self.job,
                "지원 시기": self.period,
                "대학 분류": self.college_category,
                "전공": self.major,
                "학점": self.grade,
                "언어": self.language,
                "경험": self.experience,
                "기타": self.etc,
            }
        )

    def sort_columns_for_RAG(self):
        """
        Align data for RAG
        """
        self.pass_data.dropna(subset=["자기소개서"], inplace=True)
        self.pass_data.sort_values(
            by=[
                "직무",
                "회사",
                "전공",
                "대학 분류",
                "지원 시기",
                "경험",
                "기타",
                "학점",
                "언어",
            ],
            ascending=False,
        )

    def save_to_csv(self, filepath):
        """
        Save as a csv file

        Parameters:
            filepath : save destination
        """

        self.pass_data.to_csv(filepath, index=False)
        self.log.info("Data saved as CSV format")
