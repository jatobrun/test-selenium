from selenium.webdriver.common.by import By

class Constants():
    BASE_URL="https://www.espol.edu.ec"
    BASE_ERROR_MESSAGE = "Error"
    EDUCATION_BUTTON_TEXT = "Educación"
    IMPLICITY_WAIT_TIME = 10
    EDUCATION_BUTTON_HREF_TEXT = "/educacion"

class MainPageLocators(object):
    EDUCATION_BUTTON = (By.XPATH, f"//a[contains(@href, \
                        '{Constants.EDUCATION_BUTTON_HREF_TEXT}')]")

class EducationPageLocators(object):
    FACULTY_BLOCKS = [(By.XPATH, \
                        f"//div[@id='views-bootstrap-accordion-{str(e)}']") \
                        for e in range(1,3)]
    FIRST_FACULTY_BLOCK_BUTTON = [(By.XPATH, f"//a[contains(@href, '#collapse-1-{e}')]")\
                        for e in range(0, 4)]
    SECOND_FACULTY_BLOCK_BUTTON = [(By.XPATH, f"//a[contains(@href, '#collapse-2-{e}')]")\
                        for e in range(0, 4)]
    FIRST_MAJOR_BLOCK = [(By.XPATH, f"//div[@id='collapse-1-{e}']") \
                        for e in range(0, 4)]
    SECOND_MAJOR_BLOCK = [(By.XPATH, f"//div[@id='collapse-2-{e}']") \
                        for e in range(0, 4)]
    LINKS = (By.XPATH, "//div[@class='field-content']/ul/li/a")

class MajorsPageLocators(object):
    ABET_LINK = (By.XPATH, "//a[contains(@href, 'www.abet.org')]")


    