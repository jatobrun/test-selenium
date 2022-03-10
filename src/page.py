from src.elements import EducationButtonElement
from src.locators import Constants as const
import src.locators as locators
import time
import validators
import csv


class BasePage(object):
    """Base class to initialize the base page that will be called from all
    pages"""

    def __init__(self, driver):
        self.driver = driver

    def check_element_exist(self, element, text):
        return element.get_attribute("text").strip() == text


class MainPage(BasePage):
    """Home page action methods"""

    education_button = EducationButtonElement()

    def go_to_education_page(self):
        if self.check_element_exist(
            element=self.education_button, text=const.EDUCATION_BUTTON_TEXT
        ):
            self.education_button.click()


class EducationPage(BasePage):
    """Education page action methods"""

    first_block_faculty_names: List[str] = []
    second_block_faculty_names = []
    majors_per_faculty = []

    university = []

    def get_faculties(self):
        """Get all faculties in all faculty blocks"""
        faculty_block_elements = [
            self.driver.find_element(*faculty_block)
            for faculty_block in locators.EducationPageLocators.FACULTY_BLOCKS
        ]
        self.first_block_faculty_names = faculty_block_elements[0].text.splitlines()
        self.second_block_faculty_names = faculty_block_elements[1].text.splitlines()

    def get_all_majors_name(self):
        """Get all majors name in all faculties"""
        first_major_block = []
        second_major_block = []
        for index, element in enumerate(
            locators.EducationPageLocators.FIRST_FACULTY_BLOCK_BUTTON
        ):
            first_major_block.append(
                self.get_majors_names_per_element(
                    element,
                    locators.EducationPageLocators.FIRST_MAJOR_BLOCK[index],
                    index,
                    1,
                )
            )

            time.sleep(0.5)
            second_major_block.append(
                self.get_majors_names_per_element(
                    locators.EducationPageLocators.SECOND_FACULTY_BLOCK_BUTTON[index],
                    locators.EducationPageLocators.SECOND_MAJOR_BLOCK[index],
                    index,
                    2,
                )
            )

        self.majors_per_faculty = first_major_block + second_major_block

    def get_majors_names_per_element(
        self, element_button, element_block, index, block_number
    ):
        """Get all the majors name per block of faculty

        Args:
            element_button (locator): Collapsable majors
            element_block (locator): The faculty element that I want their majors
            index (int): Identifies the major index in the faculty block
            block_number (int): The identifier to know what faculty block iterates
        """
        faculty_button = self.driver.find_element(*element_button)
        self.driver.execute_script("arguments[0].click();", faculty_button)
        time.sleep(0.5)
        major_block = self.driver.find_element(*element_block)
        major_list = major_block.text.split("\n")
        self.get_majors_url_per_major_block(major_list, index, block_number)

    def get_majors_url_per_major_block(self, major_list, index, block_number):
        major_dict = {}
        for major in major_list:
            major_selector = f"//a[text()='{major}']"
            url = self.driver.find_element_by_xpath(
                selector
            ).get_attribute("href")

            is_valid_link = self.is_valid_link(url)
            major_dict = {
                "name": major,
                "url": url,
                "is_valid_link": is_valid_link,
            }
            if block_number == 1:
                major_dict["faculty"] = self.first_block_faculty_names[index]
            else:
                major_dict["faculty"] = self.second_block_faculty_names[index]

            self.university.append(major_dict)

    def is_valid_link(self, url):
        """Validate if a link is a valid url

        Args:
            url (string): The link that we want to validate

        Returns:
            Boolean: True if the string is a valid url, otherwise is false
        """
        return True if validators.url(url) else False

    def major_is_abet(self, major) -> bool:
        """This functions helps to know if a major have the abet certifications

        Args:
            major (dict): A dictionary that contains all the major information

        Returns:
            Boolean: True is the major have the abet certification, otherwise is false
        """
        url = major["url"]
        if major["is_valid_link"]:
            self.driver.get(url)
            return self.driver.find_element(
                *locators.MajorsPageLocators.ABET_LINK
            ).is_enabled()
        return False

    def get_abet_majors(self, majors):
        """Search all the abet majors in a group o majors

        Args:
            majors (list): a List of majors

        Returns:
            List: a list of all majors that have abet
        """
        return [major["name"] for major in majors if self.major_is_abet(major)]

    def create_csv(self, majors):
        """Help us to create a csv files with all the necesary information about the task

        Args:
            majors (list): A list of all majors in a university
        """
        fieldnames = ["name", "faculty", "url", "is_valid_link"]
        with open(const.CSV_PATH, "w", encoding="UTF8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(majors)
