from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

import pdfkit

import time


class PucLib:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)

    def generate_pdf(self, pdf_content):
        output_path = './out/books_resume.pdf'
        wkhtmltopdf_path = '/usr/local/bin/wkhtmltopdf'
        pdf_options = {
            'quiet': '',
            'dpi': 300,
            'disable-smart-shrinking': '',
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
        }

        pdfkit_configuration = pdfkit.configuration(
            wkhtmltopdf=wkhtmltopdf_path)

        pdfkit.from_string(pdf_content, output_path=output_path,
                           options=pdf_options, configuration=pdfkit_configuration)

    def replace_n_to_br(self, string):
        return string.replace("\n", "<br>")

    def collect_books_elements(self):
        time.sleep(4)
        raw_books_elements = self.driver.find_elements(
            By.CSS_SELECTOR, 'li.result-list-li')
        books_infos = ''
        for book in raw_books_elements:
            books_infos += f"<h3>{book.find_element(By.CSS_SELECTOR, 'a.title-link').get_attribute('text')}</h3><p>{self.replace_n_to_br(book.find_element(By.CSS_SELECTOR, 'div.display-info').get_attribute('innerText'))}</p><hr><br>"
        return books_infos

    def get_next_page_button_of_current_page(self):
        return self.driver.find_element(By.ID, 'ctl00_ctl00_MainContentArea_MainContentArea_bottomMultiPage_lnkNext')

    def main(self):
        driver = self.driver
        search_theme = 'Teste de software'
        student_name = 'Ian Bittencourt Andrade'
        title = 'Pesquisa de livros'

        driver.get('https://www.pucminas.br/destaques/Paginas/default.aspx')
        time.sleep(5)

        services_dropdown = driver.find_element(
            By.XPATH, '/html/body/form/div[5]/div/div[1]/main/header/nav[2]/div/div/div/div/ul/li[8]/a')
        services_dropdown.click()

        lib = driver.find_element(
            By.XPATH, '/html/body/form/div[5]/div/div[1]/main/header/nav[2]/div/div/div/div/ul/li[8]/ul/li[1]/a')
        lib.click()

        driver.switch_to.window(driver.window_handles[1])

        search_content_input = driver.find_element(
            By.XPATH, '/html/body/div/div[4]/div[2]/article/div/div/ul[2]/li[1]/form/div[2]/input')
        search_content_input.send_keys(search_theme)
        search_content_input.submit()

        driver.switch_to.window(driver.window_handles[2])
        time.sleep(6)

        books_infos = ''
        for page in range(5):
            time.sleep(4)
            books_infos += self.collect_books_elements()
            if (page < 5):
                self.get_next_page_button_of_current_page().click()

        html_structure = f"<!DOCTYPE html> <html lang='pt-br'> <head> <meta charset='UTF-8'> <meta http-equiv='X-UA-Compatible' content='IE=edge'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>{title}</title></head><body><h1>{title}</h1><p><b>Aluno:</b> {student_name}<br>Tema pesquisado: {search_theme}</p><hr>{books_infos}</body></html>"

        self.generate_pdf(html_structure)


Puc = PucLib()
Puc.main()
