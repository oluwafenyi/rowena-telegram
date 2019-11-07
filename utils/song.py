import logging

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from driver import ChromeHeadlessDriver


def present_options(results):
    logging.info('Presenting results to the user.')
    text = 'Here are your options, pick one by number:\n\n'
    for index, result in enumerate(results):
        if index == 5:
            break
        song = result.find_element_by_tag_name('h3').text.strip()
        artiste = result.find_element_by_tag_name('p').text.strip()
        size = result.find_element_by_tag_name('span').text.strip()
        text += f'{index+1}.\t{song}\n'
        text += f' \t{artiste}\n'
        text += f' \t{size}\n\n'
    return text


def get_results(search_terms):
    query = '+'.join(search_terms)
    logging.info(f'Getting results for query: "{query}"')
    driver = ChromeHeadlessDriver()
    driver.implicitly_wait(10)
    driver.get(f'https://musicpleer.com/#!{query}')
    try:
        ul = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR,
             '#searchResults [data-role="listview"].ui-listview')
        ))
        results = ul.find_elements_by_css_selector('.ui-li-has-thumb')[:5]
    except NoSuchElementException:
        driver.quit()
        logging.error('Page not found')
        raise AttributeError

    if not results:
        logging.info(f'Result not found for query: {query}')
        driver.quit()
        raise AttributeError

    options_text = present_options(results)
    return options_text, results, driver


def download_choice(choice, driver):
    link = choice.find_element_by_tag_name('a').get_attribute('href')
    logging.info(f'User has picked link: {link}')
    driver.get(link)
    song = driver.\
        find_element_by_css_selector('#searchResults-player #download-btn')\
        .get_attribute('href')
    logging.info(f'Sending song to user: {song}')
    return song
