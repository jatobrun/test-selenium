from selenium import webdriver
from src.locators import Constants as const
import src.page as page


class Espol(webdriver.Chrome):
    def __init__(
        self,
        driver_path="/Users/jamiltorres/Documents/ioet/chromedriver",
        teardown=False,
    ):
        self.driver_path = driver_path
        self.teardown = teardown
        super(Espol, self).__init__(self.driver_path)
        self.get(const.BASE_URL)
        self.implicitly_wait(const.IMPLICITY_WAIT_TIME)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def landing_page_action(self):
        main_page = page.MainPage(self)
        main_page.go_to_education_page()

    def exercise_1(self):
        education_page = page.EducationPage(self)
        education_page.get_faculties()
        education_page.get_all_majors_name()
        education_page.create_csv(education_page.university)
        print("Puedes encontrar el archivo en src/static/output.csv")
        return education_page.university

    def exercise_2(self, university):
        education_page = page.EducationPage(self)
        print("Cargando...")
        majors = education_page.get_abet_majors(university)
        print("Carreras con certificacion ABET:")
        _ = [print(f"{index}. {major}") for index, major in enumerate(majors)]
