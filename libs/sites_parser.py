import requests
from bs4 import BeautifulSoup as bs
from fuzzywuzzy import fuzz
import re

from libs.sites_domain_names import all_sites_list, all_sites_list_part_two

HEADERS = {'User-Agent': 'My User Agent 1.0', 'From': 'youremail@domain.example'}
PROTOCOL = "http://"

career_keywords = ["career", "careers", "vacancies", "vacancy", "job", "jobs", "positions", "opening", "opportunity",
                   "occupation", "employment"]

hire_list = ["developer", "qa", "engineer", "senior", "middle", "lead", "aqa", "software", "python",
             "programmer", "administrator", "specialist", "webmaster", "react.js", "node.js", "node js", "angular",
             "devops", "full stack", "fullstack", "frontend", "backend", "front end", "back end", "middle", "junior"]



exist_career_page = []
not_exist_career_page = []


def path_formation(value, url, protocol=PROTOCOL):
    if not value.startswith('http'):
        l = list(value)
        for c in value:
            if c in ['/', '.']:
                l.remove(l[0])
            else:
                break
        extension = ''.join(l)
        return f"{url}{extension}"
    else:
        return value


def get_html(url):
    try:
        if url.startswith('http'):
            html = requests.get(f"{url}", headers=HEADERS, verify=False)
        else:
            html = requests.get(f"{PROTOCOL}{url}", headers=HEADERS, verify=False)
    except:
        return False
    return {'html': html, 'url': html.url}


def get_all_links(html):
    all_links = []
    soup = bs(html, 'html.parser')
    a_tag_content = soup.find_all("a")
    for i in a_tag_content:
        all_links.append(i.get('href'))
    return all_links


def found_applicable_link(all_links):
    for i in all_links:
        for keywords in career_keywords:
            if fuzz.partial_ratio(i, keywords) == 100:
                return i.strip()
    return False


def parser(sites):
    for site in sites:
        response = get_html(site)
        if response and response['html'].status_code == 200:
            all_links = get_all_links(response['html'].text)
            career_page_link = found_applicable_link(all_links)
            if not career_page_link:
                print(f"Did not found career link for: '{site}'")
                not_exist_career_page.append(site)
                continue
            career_page_res = get_html(f"{path_formation(career_page_link, url=response['url'])}")
            if career_page_res and career_page_res['html'].status_code == 200:
                print(f"Found career page for: '{site}'")
                exist_career_page.append(site)
                # find_positions(career_page_res['html'])
            else:
                print(f"Did not found career page for: '{site}'")
                not_exist_career_page.append(site)
        else:
            print(f"No html received for: '{site}'")
            continue


# def find_positions(html):
#     page_content = bs(html.text, 'html.parser')
#
#     jobs = []
#     for vacancy in set(hire_list):
#         if vacancy in page_content.text:
#             entries = page_content.find_all(text=re.compile(vacancy, re.IGNORECASE))
#             for entry in entries:
#                 entry = entry.replace("\n", "").replace("\t", "").replace("Requirements:", ""). \
#                     replace("vacancies", "").replace(":", "").strip()
#                 if entry not in jobs and len(jobs) < 50:
#                     if "\n" not in entry and "<" not in entry and "?" not in entry \
#                             and ". " not in entry and len(entry.split(" ")) < 6 and len(entry) < 50:
#                         jobs.append(entry)
#     print(jobs)

    


parser(all_sites_list)
