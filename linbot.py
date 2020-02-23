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

        for x in self.browser.driver.find_elements_by_css_selector('.search-result__info a'):
            # print('1', x.get_attribute("href"))
            href = x.get_attribute("href")
            if "https://www.linkedin.com/in/" in href:
                profile_id = href.split("https://www.linkedin.com/in/")[1][:-1]
                utils.append_ids(profile_id)

        if self.store_connect is False:
            self.connect()

        max_pagination = self.browser.driver.find_elements_by_css_selector(
            '.artdeco-pagination__indicator button')[-1].get_attribute(
                'aria-label')
        max_pagination = max_pagination.split(' ')[-1]
        print(max_pagination)

        if int(max_pagination) >= 2:
            if int(max_pagination) > 2:
                max_pagination = "2"
            for y in range(2, int(max_pagination)):
                self.search_page_n += 1
                self.browser.goto(url="{}&page={}".format(
                    url_search.format(self.search), self.search_page_n))
                self.browser.scroll_bottom()
                time.sleep(1)
                if self.store_connect is False:
                    self.connect()
                for x in self.browser.driver.find_elements_by_css_selector('.search-result__info a'):
                    # print('1', x.get_attribute("href"))
                    href = x.get_attribute("href")
                    if "https://www.linkedin.com/in/" in href:
                        profile_id = href.split(
                            "https://www.linkedin.com/in/")[1][:-1]
                        utils.append_ids(profile_id)

        # for x in self.browser.driver.find_elements_by_class_name("search-result__info"):
        #     for y in x.find_elements_by_tag_name("a"):
        #         print(y.get_attribute("href"))

# while True:

        #     if len(self.button_connects) >= self.limit_connect:
        #         break
        #     self.search_page_n += self.limit_connect
        #     self.browser.goto(url="{}&page={}".format(
        #         url_search.format(self.search), str(self.search_page_n)))
        print('\t-> Done\n')

    def connect(self):
        print('[] Connect with 2 people')
        self.button_connects = self.browser.find_els_xpath(
            xpath=config.selectors['connect'])[:1]
        for button_connect in self.button_connects[:self.limit_connect]:
            print(button_connect.get_attribute('aria-label'))
            button_connect.click()
            self.browser.wait(el=config.selectors['connect_confirm'])
            button_send = self.browser.find_el_xpath(
                config.selectors['connect_confirm'])
            button_send.click()
            self.store_connect = True
            time.sleep(2)

        for request in self.browser.driver.requests:
            print("PATH", request.path)
            print('HEADERS', request.headers)
            if request.path == "https://www.linkedin.com/voyager/api/growth/normInvitations":
                utils.store_request(
                    headers=request.headers, body=request.body)

        print('\t-> Done\n')

    def close(self):
        print('[] Closing the browser')
        self.browser.driver.close()
    
    def send_reqs(self):
        lines = utils.get_ids()
        for id in lines:
            print('[] Send request to {}'.format(id))
            req = utils.set_request(profile_id=id)
            r = requests.post("https://www.linkedin.com/voyager/api/growth/normInvitations", 
                headers=req['headers'], data=req['body'])
            print('\t-> Done')            
            print("[] Next round : {}".format(
                utils.get_next_round(round_duration=60)))
            time.sleep(60)


    def run(self):
        # while True:
        self.browser = headless.Browser()
        utils.clear()
        self.login()
        self.search_page()
        # self.connect()
        self.close()
        self.send_reqs()
        # time.sleep(300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--role', help='Keywords to use while searching people')
    parser.add_argument('--user', help='Email or phone')
    args = parser.parse_args()
    password = getpass.getpass('Linkedin password:')

    LinBot(email=args.user, password=password, search=args.role).run()
