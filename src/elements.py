from selenium.webdriver.support.ui import WebDriverWait
import src.locators as locators


class BasePageElement(object):
    """Base page class that is initialized on every page object class."""

    def __set__(self, obj, value):
        """Sets the text to the value supplied"""

        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator)
        )
        driver.find_element(*self.locator).clear()
        driver.find_element(*self.locator).send_keys(value)

    def __get__(self, obj, owner):
        """Gets the text of the specified object"""

        driver = obj.driver
        WebDriverWait(driver, 100).until(
            lambda driver: driver.find_element(*self.locator)
        )
        element = driver.find_element(*self.locator)
        return element


class EducationButtonElement(BasePageElement):

    locator = locators.MainPageLocators.EDUCATION_BUTTON


class FirstFacultyBlockElement(BasePageElement):
    locator = locators.EducationPageLocators.FACULTY_BLOCKS[0]


class SecondFacultyBlockElement(BasePageElement):
    locator = locators.EducationPageLocators.FACULTY_BLOCKS[1]
