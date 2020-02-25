import headless
import utils
import time
import argparse
import getpass
import config
import sys
import requests


class LinBot:
    def __init__(self, email: str, password: str, search: str):
        self.email = email
        self.password = password
        self.limit_connect = 2
        self.search_page_n = 0
        self.button_connects = []
        self.search = search
        self.browser = None
        self.store_connect = False

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
        try:
            self.browser.wait(el=config.selectors['page_loaded'])
        except:
            print('\tLogin Failed')
            self.browser.close()
            sys.exit()

        print('\t-> Done\n')

    def search_page(self):
        print('[] Looking for {}'.format(self.search))
        url_search = config.urls['base'] + config.urls['search']
        self.browser.goto(
            url=url_search.format(self.search))
        self.browser.scroll_bottom()
        time.sleep(1)

        self.get_available_connect()

        if self.store_connect is False:
            self.connect()

        max_pagination = self.browser.driver.find_elements_by_css_selector(
            config.selectors['pagination_button'])[-1].get_attribute(
                config.selectors['aria_label'])
        max_pagination = max_pagination.split(' ')[-1]

        if int(max_pagination) >= 2:
            if int(max_pagination) > 10:
                max_pagination = "11"
            for y in range(2, int(max_pagination)):
                self.search_page_n += 1
                self.browser.goto(url="{}&page={}".format(
                    url_search.format(self.search), self.search_page_n))
                self.browser.scroll_bottom()
                time.sleep(1)
                if self.store_connect is False:
                    self.connect()
                self.get_available_connect()
        print('\t-> Done\n')

    def get_available_connect(self):
        print('\t-> Get available connects - Page {}'.format(self.search_page_n))
        for y in self.browser.driver.find_elements_by_css_selector('.search-result'):
            try:
                if y.find_element_by_css_selector(config.selectors['search_actions']).text == "Connect":
                    x = y.find_element_by_css_selector(
                        config.selectors['search_link'])
                    href = x.get_attribute("href")
                    if "/in/" in href:
                        profile_id = href.split(
                            config.urls['base'] + config.urls['in'])[1][:-1]
                        utils.append_ids(profile_id)
            except:
                pass

    def connect(self):
        print('\t-> Get a sample request')
        self.button_connects = self.browser.find_els_xpath(
            xpath=config.selectors['connect'])[:1]
        for button_connect in self.button_connects[:self.limit_connect]:
            print(button_connect.get_attribute(config.selectors['aria_label']))
            button_connect.click()
            self.browser.wait(el=config.selectors['connect_confirm'])
            button_send = self.browser.find_el_xpath(
                config.selectors['connect_confirm'])
            button_send.click()
            self.store_connect = True
            time.sleep(2)

    def close(self):
        print('[] Closing the browser')
        self.browser.driver.close()

    def send_reqs(self):
        lines = utils.get_ids()
        for profile_id in lines:
            print('[] Send request to {}'.format(profile_id))
            req = utils.set_request(profile_id=profile_id)
            r = requests.post(config.urls['base'] + config.urls['connect'],
                              headers=req['headers'], data=req['body'])
            print('\t-> Done')
            utils.update_ids(profile_id=profile_id)
            print("\t-> Next round : {}\n".format(
                utils.get_next_round(round_duration=180)))
            time.sleep(180)

    def run(self):
        # while True:
        self.browser = headless.Browser()
        utils.clear()
        self.login()
        self.search_page()
        self.close()
        self.send_reqs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--role', help='Keywords to use while searching people')
    parser.add_argument('--user', help='Email or phone')
    args = parser.parse_args()
    password = getpass.getpass('Linkedin password:')

    LinBot(email=args.user, password=password, search=args.role).run()
