import pprint

from bs4 import BeautifulSoup
from get_html import get_html

'''
    The function parses page with the list of resumes at url.
    Then it creates the list of persons.
    After that the function asdds the next information from the list to the person list:
     - age
     - gender
     - url to personal resume

     Input: (str) url
     Output: (list) full list of persons
'''

def fetch_person_list(url):
    page = get_html(url)
    page_soup = BeautifulSoup(page, 'html.parser')

    person_list = []
    person = {}
    person_row_list = page_soup.tr(class_='output__item')

    
    for row in person_row_list:

        # Fetch age, gender and url from output listing page
        tag_with_age = row.find('span', class_='output__age')
        tag_with_gender = row.find('meta', itemprop='gender')
        tag_with_url = row.find('a', itemprop='jobTitle')

        # strip years number off ' years'
        age = tag_with_age.text.strip()[0:2]
        # check that the age is specified
        if age != '':
            age = int(age)
        else: age = 0
        gender = tag_with_gender.attrs['content']
        url = 'https://hh.ru{}'.format(tag_with_url.attrs['href'])
        title = tag_with_url.text

        person = {'gender': gender,
                  'url': url,
                  'title': title,
                  'age': age,
                  'has_degree': False,
                  'city': '',
                  'keywords': []}

        person_list.append(person)

    person_list = fetch_info_from_resume(person_list)

    return person_list

'''
    The function adds the next information from personal page to the person list:
     - has_degree
     - keywords
     - city

     Input: (list) list of persons without upper info
     Output: (list) full list of persons
'''

def fetch_info_from_resume(person_list):
    for person in person_list:
        personal_page = get_html(person['url'])
        personal_page_soup = BeautifulSoup(personal_page, 'html.parser')

        # Check that the personal page include a highschool/university degree mark
        personal_page_degree_mark = personal_page_soup.find_all(string='Высшее образование')
        # Add the degree mark to person parameter
        if personal_page_degree_mark:
            person['has_degree'] = True

        # Fetch the list tags with keywords
        personal_page_keywords_tags = personal_page_soup.find_all('span', class_='bloko-tag__section bloko-tag__section_text')
        personal_page_keywords_list = []
        # Add keywords to the list
        for tag in personal_page_keywords_tags:
            personal_page_keywords_list.append(tag.text)
        person['keywords'] = personal_page_keywords_list

        # Fetch the city name
        personal_page_city_tag = personal_page_soup.find('span', itemprop='addressLocality')
        if personal_page_city_tag:
            person['city'] = personal_page_city_tag.text

    return person_list

'''
    The function fetch resume list from hh.ru by keyword

     Input: (str) keyword
     Output: (list) full list of persons at hh.ru
'''

def fetch_resume_list_by_keyword(keyword):

    full_person_list = []

    # HH.ru limits page number value to 50 maximum
    for page_number in range(0, 1):
        url_args = {
            'exp_period': 'all_time',
            # HH.ru limits items max on page from 10 to 100
            'items_on_page': 10,
            'order_by': 'relevance',
            # Keyword 'python' to url argument
            'text': keyword,
            'pos': 'full_text',
            'source': 'resumes',
            'logic': 'normal',
            'clusters': 'true',
            'page': page_number
        }

        arg_string = ''

        for key, value in url_args.items():
            arg_string += '{}={}&'.format(key, value)

        page_url = 'https://hh.ru/search/resume?{}'.format(arg_string)

        page_person_list = fetch_person_list(page_url)

        # Add list of persons for every output results page
        full_person_list += page_person_list
        page_number += 1

    return full_person_list

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(fetch_resume_list_by_keyword('python'))
