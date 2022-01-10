from src.elements import EducationButtonElement
from src.locators import Constants as const
import src.locators as locators
import time
import validators
import logging
from pathlib import Path
import csv
import sys

class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""
    loggerName = Path(__file__).stem
    logFormatter = logging.Formatter(fmt=' %(name)s :: %(levelname)-8s :: %(message)s')
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.WARNING)
    consoleHandler.setFormatter(logFormatter)

    logger.addHandler(consoleHandler)

    def __init__(self, driver):
        self.driver = driver
    
    def check_element_exist(self, element, text):
        return element.get_attribute('text').strip() == text


class MainPage(BasePage):
    """Home page action methods """
    education_button = EducationButtonElement()

    def go_to_education_page(self):
        self.education_button.click() if self.check_element_exist(
            element = self.education_button, 
            text = const.EDUCATION_BUTTON_TEXT
        ) else self.logger.warning(" lines: 37, warning message")

class EducationPage(BasePage):
    """Education page action methods """
    first_block_faculty_names = []
    second_block_faculty_names = []
    majors_per_faculty = []

    university = []


    def get_faculties(self):
        error = False
        try:
            faculty_block_elements = [self.driver.find_element(*faculty_block) for faculty_block in \
                                    locators.EducationPageLocators.FACULTY_BLOCKS ]
            self.first_block_faculty_names = faculty_block_elements[0].text.split('\n') 
                                
            self.second_block_faculty_names = faculty_block_elements[1].text.split('\n')
        except:
            self.logger.warning(" lines: 61, warning message")
            error = True

        return error

    def get_all_majors_name(self):
        first_major_block = []
        second_major_block = []
        for index, element in enumerate(locators.EducationPageLocators.FIRST_FACULTY_BLOCK_BUTTON):
            first_major_block.append(self.get_majors_names_per_element(element, \
                                locators.EducationPageLocators.FIRST_MAJOR_BLOCK[index], \
                                    index, 1))
                    
            time.sleep(0.5)
            second_major_block.append(self.get_majors_names_per_element(locators.EducationPageLocators.SECOND_FACULTY_BLOCK_BUTTON[index],\
                                        locators.EducationPageLocators.SECOND_MAJOR_BLOCK[index], \
                                            index, 2))

        self.majors_per_faculty = first_major_block + second_major_block
        # print(self.university)
    
    def get_majors_names_per_element(self, element_button, element_block, index, block_number):
        error = False
        try:
            faculty_button = self.driver.find_element(*element_button)
            self.driver.execute_script("arguments[0].click();", faculty_button)
            time.sleep(0.5)
            major_block = self.driver.find_element(*element_block)
            major_list = major_block.text.split('\n')
            self.get_majors_url_per_major_block(major_list, index, block_number)
        except:
            self.logger.warning(" lines: 87, warning message")
            print(sys.exc_info())
            error = True
        return error

    def get_majors_url_per_major_block(self, major_list, index, block_number):
        error = False
        major_dict = {}
        for i, major in enumerate(major_list):
            try:
                url = self.driver.find_element_by_xpath(f"//a[text()='{major}']").get_attribute('href')
                is_valid_link = self.is_valid_link(url)
            except:
                self.logger.warning(" lines: 99, warning message")
                url = const.BASE_ERROR_MESSAGE
                is_valid_link, error = False, True

            major_dict = {
                        'name': major,
                        'url': url,
                        'is_valid_link': is_valid_link,
                    }
            if block_number == 1:
                major_dict['faculty'] = self.first_block_faculty_names[index]
            else:
                major_dict['faculty'] = self.second_block_faculty_names[index]
            
            self.university.append(major_dict)
        return error

    def is_valid_link(self, url):
        return False if not validators.url(url) else True
    
    def major_is_abet(self, major):
        is_abet = False
        url = major['url']
        if major['is_valid_link']:
            self.driver.get(url)
            try:
                self.driver.find_element(*locators.MajorsPageLocators.ABET_LINK)
                is_abet = True
            except:
                # self.logger.warning(" lines: 128, warning message")
                is_abet = False
        return is_abet
    
    def get_abet_majors(self, majors):
        return [major['name'] for major in majors if self.major_is_abet(major)] 
    
    def create_csv(self, majors):
        fieldnames = ['name', 'faculty', 'url', 'is_valid_link']
        with open('./src/static/output.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(majors)
