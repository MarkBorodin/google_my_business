import sys
import time

import psycopg2
from bs4 import BeautifulSoup
from selenium import webdriver


class Spider(object):

    def __init__(self, company):
        self.company = company

    def get_data(self):
        """start web browser with selenium and get data"""

        # make a request url to google
        url = 'https://www.google.com/search?q=' + ''.join(self.company)

        self.results = {} # noqa

        # send a request and get soup
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.headless = True
            browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
            browser.get(url)
            time.sleep(5)
            html = browser.page_source
            browser.close()
            soup = BeautifulSoup(html, 'lxml')

            # get the required data:

            try:
                self.results['my_business'] = soup.find('div', class_='ifM9O')
                if self.results['my_business']:
                    self.results['my_business_yes_no'] = 't'
                    print('mybusiness is present')
                else:
                    print("no my_business")
                    self.results['my_business_yes_no'] = 'f'
            except Exception as e:
                print("no my_business")
                self.results['my_business_yes_no'] = 'f'

            try:
                self.results['url'] = soup.find('a', class_='ab_button').get('href').strip()
                if self.results['url']:
                    self.results['url_yes_no'] = 't'
                    print('url is present')
            except Exception as e:
                print("no website")
                self.results['url'] = 'NULL'
                self.results['url_yes_no'] = 'f'

            try:
                self.results['phone'] = soup.find_all('span', class_='LrzXr zdqRlf kno-fv')[-1].text.strip()
                if self.results['phone']:
                    self.results['phone_yes_no'] = 't'
                    print('phone is present')
            except Exception as e:
                print("no phone")
                self.results['phone'] = 'NULL'
                self.results['phone_yes_no'] = 'f'

            try:
                self.results['rating'] = float(soup.find_all('span', class_='Aq14fc')[-1].text.strip().replace(',', '.'))
                if self.results['rating']:
                    self.results['rating_yes_no'] = 't'
                    print('rating is present')
            except Exception as e:
                print("no rating")
                self.results['rating'] = 'NULL'
                self.results['rating_yes_no'] = 'f'

            try:
                self.results['nr_of_ratings'] = soup.find_all('span', class_='hqzQac')[-1].text.strip().split(sep=' ')[0]
                if self.results['nr_of_ratings']:
                    self.results['nr_of_ratings_yes_no'] = 't'
                    print('nr_of_ratings is present')
            except Exception as e:
                print("no nr_of_ratings")
                self.results['nr_of_ratings'] = 'NULL'
                self.results['nr_of_ratings_yes_no'] = 'f'

            print(f"{self.company}:")
            print(f"my_business_yes_no: {self.results['my_business_yes_no']}")
            print(f"url_yes_no: {self.results['url_yes_no']}")
            print(f"url: {self.results['url']}")
            print(f"phone_yes_no: {self.results['phone_yes_no']}")
            print(f"phone: {self.results['phone']}")
            print(f"rating: {self.results['rating']}")
            print(f"rating_yes_no: {self.results['rating_yes_no']}")
            print(f"nr_of_ratings: {self.results['nr_of_ratings']}")
            print(f"nr_of_ratings_yes_no: {self.results['nr_of_ratings_yes_no']}")

        except Exception as e:
            print(e)

    def write_data_to_db(self):
        """write data to db"""

        self.open_db()

        # write data to db
        self.cur.execute(
            """INSERT INTO my_business_entry (url_yes_no, url, phone_yes_no, phone, rating, nr_of_ratings, myBusiness, company)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                str(self.results['url_yes_no']),
                str(self.results['url']),
                str(self.results['phone_yes_no']),
                str(self.results['phone']),
                str(self.results['rating']),
                str(self.results['nr_of_ratings']),
                str(self.results['my_business_yes_no']),
                str(self.company),
            )
        )

        self.connection.commit()
        self.close_db()

    def open_db(self):
        """open db"""
        hostname = '127.0.0.1'
        username = 'parsing_admin'
        password = 'parsing_adminparsing_admin'
        database = 'parsing'
        port = "5444"
        self.connection = psycopg2.connect(  # noqa
            host=hostname,
            user=username,
            password=password,
            dbname=database,
            port=port)
        self.cur = self.connection.cursor()  # noqa

    def close_db(self):
        """close db"""
        self.cur.close()
        self.connection.close()


if __name__ == '__main__':
    # get company in command line
    company = sys.argv[1]

    # create object
    spider = Spider(company)

    # get data
    spider.get_data()

    # write data to the db
    spider.write_data_to_db()
