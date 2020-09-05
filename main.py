import csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from decouple import config

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(config("CHROMEDRIVER_PATH"), options=options)


class JobOffer:
    def __init__(self, title, company, salary_data):
        self.title = title
        self.company = company

        self.salary_converter(salary_data)

    def salary_to_int(self, salary_as_a_string):
        if "k" in salary_as_a_string:
            return int(salary_as_a_string[:-1]) * 1000
        elif "M" in salary_as_a_string:
            return int(salary_as_a_string[:-1]) * 1000000
        else:
            return int(salary_as_a_string)

    def salary_converter(self, salary_data):
        currency = salary_data.split()[-1]
        splitted = salary_data[: -len(currency)].replace(" ", "").split("-")

        self.min_salary = self.salary_to_int(splitted[0])
        self.max_salary = self.salary_to_int(splitted[1])
        self.currency = currency

    def get_csv(self):
        return [
            self.title,
            self.company,
            self.min_salary,
            self.max_salary,
            self.currency,
        ]


def fetch_backend_jobs():
    job_offers = []

    for page in range(1, 23):
        driver.get("https://nofluffjobs.com/jobs/backend?page={page}".format(page=page))

        done = False
        current_job_offer = 1
        current_list = 1

        while not done:
            try:
                job_offer = WebDriverWait(driver, 0.5).until(
                    lambda d: d.find_element_by_xpath(
                        "/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-postings-search/div/nfj-main-loader/div/nfj-search-results/nfj-postings-list[{current_list}]/a[{current_job_offer}]".format(
                            current_list=current_list,
                            current_job_offer=current_job_offer,
                        )
                    )
                )
                job_offers.append(
                    JobOffer(
                        title=job_offer.find_element_by_xpath(
                            ".//nfj-posting-item-title/div[1]/h4"
                        ).text,
                        company=job_offer.find_element_by_xpath(
                            ".//nfj-posting-item-title/div[1]/span"
                        ).text[2:],
                        salary_data=job_offer.find_element_by_xpath(
                            ".//div[2]/nfj-posting-item-tags/span"
                        ).text,
                    )
                )
                current_job_offer += 1
            except:
                if current_list >= 2:
                    done = not done
                else:
                    current_job_offer = 1
                    current_list += 1

    driver.close()
    return job_offers


jobs = fetch_backend_jobs()

with open("results/backend-{date}".format(date=datetime.now()), "w+") as file:
    writer = csv.writer(file)

    for job in jobs:
        writer.writerow(job.get_csv())