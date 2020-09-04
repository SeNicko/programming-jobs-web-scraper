'''
TODO:
  - Handle multiple pages (at the moment jobs comes only from first page)
  - Allow to change from only backend job offers to all types no fluff jobs has
  - Enable setting filters
  - Create simple frntend which will allow to browse through job offers. Redirect to no fluff jobs after click
'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from decouple import config

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(config('CHROMEDRIVER_PATH'), options=options)
driver.get('https://nofluffjobs.com/')

def fetchBackendJobs(): 
  job_adverts = []

  button = driver.find_element_by_xpath('/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-postings-search/div/nfj-main-loader/nfj-postings-list[1]/div[2]/a')
  button.click()

  job_offer_pages_count_element = WebDriverWait(driver, 10).until(lambda d: d.find_element_by_xpath('/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-postings-search/div/nfj-main-loader/div/nfj-search-results/div/ngb-pagination/ul/li[8]/a'))
  job_offer_pages_count = int(job_offer_pages_count_element.text)

  done = False
  current_job_offer = 1
  current_list = 1

  while not done:
    try:
      job_offer = WebDriverWait(driver, 0.5).until(lambda d: d.find_element_by_xpath('/html/body/nfj-root/nfj-layout/nfj-main-content/div/div/div[1]/nfj-postings-search/div/nfj-main-loader/div/nfj-search-results/nfj-postings-list[{current_list}]/a[{current_job_offer}]'.format(current_list = current_list, current_job_offer = current_job_offer)))
      job_adverts.append(job_offer)
      current_job_offer += 1
    except:
      if current_list >= 2:
        done = not done
      else:
        current_job_offer = 1
        current_list += 1

  print(job_adverts)
  driver.close()

fetchBackendJobs()