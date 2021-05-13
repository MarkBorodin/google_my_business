import sys
import time

import psycopg2
from bs4 import BeautifulSoup
from selenium import webdriver


class Spider(object):

    def get_data(self, company):
        """start web browser with selenium and get data"""

        # make a request url to google
        url = 'https://www.google.com/search?q=' + ''.join(company)

        results = dict()
        results['company'] = company

        # send a request and get soup
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.headless = True
            browser = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
            browser.get(url)
            time.sleep(7)
            html = browser.page_source
            browser.close()
            soup = BeautifulSoup(html, 'lxml')

            # get the required data:

            try:
                results['my_business'] = soup.find('div', class_='liYKde g VjDLd')
                if results['my_business']:
                    results['my_business_yes_no'] = 't'
                    print('mybusiness is present')

                    try:
                        results['url'] = soup.find('a', class_='ab_button').get('href').strip()
                        if results['url'] != '#':
                            results['url_yes_no'] = 't'
                            print('url is present')
                        else:
                            results['url'] = None
                            results['url_yes_no'] = 'f'
                    except Exception as e:
                        print("no website")
                        results['url'] = None
                        results['url_yes_no'] = 'f'

                    try:
                        results['phone'] = soup.find_all('span', class_='LrzXr zdqRlf kno-fv')[-1].text.strip()
                        if results['phone']:
                            results['phone_yes_no'] = 't'
                            print('phone is present')
                    except Exception as e:
                        print("no phone")
                        results['phone'] = None
                        results['phone_yes_no'] = 'f'

                    try:
                        results['rating'] = float(
                            soup.find_all('span', class_='Aq14fc')[-1].text.strip().replace(',', '.'))
                        if results['rating']:
                            results['rating_yes_no'] = 't'
                            print('rating is present')
                    except Exception as e:
                        try:
                            results['rating'] = float(
                                soup.find('span', class_='inaKse G5rmf').text.strip().split(sep='/')[0])
                            if results['rating']:
                                results['rating_yes_no'] = 't'
                                print('rating is present')
                        except Exception as e:
                            print("no rating")
                            results['rating'] = None
                            results['rating_yes_no'] = 'f'

                    try:
                        results['nr_of_ratings'] = \
                            soup.find_all('span', class_='hqzQac')[-1].text.strip().split(sep=' ')[0]
                        if results['nr_of_ratings']:
                            results['nr_of_ratings_yes_no'] = 't'
                            print('nr_of_ratings is present')
                    except Exception as e:
                        try:
                            results['nr_of_ratings'] = \
                                soup.find('span', class_='inaKse KM6XSd').text.strip()
                            results['nr_of_ratings'] = ''.join(i for i in results['nr_of_ratings'] if i.isdigit())
                            if results['nr_of_ratings']:
                                results['nr_of_ratings_yes_no'] = 't'
                                print('nr_of_ratings is present')
                        except Exception as e:
                            print("no nr_of_ratings")
                            results['nr_of_ratings'] = None
                            results['nr_of_ratings_yes_no'] = 'f'

                    self.write_data_to_db(results)

                    print(f"{company}:")
                    print(f"my_business_yes_no: {results['my_business_yes_no']}")
                    print(f"url_yes_no: {results['url_yes_no']}")
                    print(f"url: {results['url']}")
                    print(f"phone_yes_no: {results['phone_yes_no']}")
                    print(f"phone: {results['phone']}")
                    print(f"rating: {results['rating']}")
                    print(f"rating_yes_no: {results['rating_yes_no']}")
                    print(f"nr_of_ratings: {results['nr_of_ratings']}")
                    print(f"nr_of_ratings_yes_no: {results['nr_of_ratings_yes_no']}")

                else:
                    print(f"{company}: no my_business")

            except Exception as e:
                print(f"{company}: no my_business")

        except Exception as e:
            print(e)

    def write_data_to_db(self, results):
        """write data to data base"""
        self.open_db()

        # write data to db
        self.cur.execute(
            """INSERT INTO my_business_entry (
            url_yes_no, url, phone_yes_no, phone, rating, nr_of_ratings, myBusiness, company)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (
                results['url_yes_no'],
                results['url'],
                results['phone_yes_no'],
                results['phone'],
                results['rating'],
                results['nr_of_ratings'],
                results['my_business_yes_no'],
                results['company'],
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
    spider = Spider()

    # get data
    spider.get_data(company)
