import headless
import utils
import time
import argparse
import getpass
import config


class LinBot:
    def __init__(self, email: str, password: str, search: str):
        self.email = email
        self.password = password
        self.limit_connect = 2
        self.search_page_n = 0
        self.button_connects = []
        self.search = search
        self.browser = None

    def login(self):
        print('[] Login as {}'.format(self.email))
        self.browser.goto(url=config.urls['base'] + "/")
        self.browser.wait(el=config.selectors['login_user'])
        input_email = self.browser.find_el_xpath(
            xpath=config.selectors['login_user'])
        input_password = self.browser.find_el_xpath(
            xpath=config.selectors['login_password'])
        input_email.send_keys(self.email)
        input_password.send_keys(self.password)
        self.browser.find_el_xpath(
            xpath=config.selectors['login_submit']).click()
        print('\t-> Done\n')

    def search_page(self):
        print('[] Looking for {}'.format(self.search))
        url_search = config.urls['base'] + config.urls['search']
        self.browser.goto(
            url=url_search.format(self.search))
        self.browser.scroll_bottom()
        while True:
            self.button_connects = self.browser.find_els_xpath(
                xpath=config.selectors['connect'])
            if len(self.button_connects) >= self.limit_connect:
                break
            self.search_page_n += self.limit_connect
            self.browser.goto(url="{}&page={}".format(
                url_search.format(self.search), str(self.search_page_n)))
        print('\t-> Done\n')

    def connect(self):
        print('[] Connect with 2 people')
        for button_connect in self.button_connects[:self.limit_connect]:
            print(button_connect)
            button_connect.click()
            self.browser.wait(el=config.selectors['connect_confirm'])
            button_send = self.browser.find_el_xpath(
                config.selectors['connect_confirm'])
            button_send.click()
            time.sleep(2)
        print('\t-> Done\n')

    def close(self):
        print('[] Closing the browser')
        self.browser.driver.close()
        print("[] Next round : {}".format(
            utils.get_next_round(round_duration=300)))

    def run(self):
        while True:
            self.browser = headless.Browser()
            utils.clear()
            self.login()
            self.search_page()
            self.connect()
            self.close()
            time.sleep(300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--role', help='Keywords to use while searching people')
    parser.add_argument('--user', help='Email or phone')
    args = parser.parse_args()
    password = getpass.getpass('Linkedin password:')

    LinBot(email=args.user, password=password, search=args.role).run()
