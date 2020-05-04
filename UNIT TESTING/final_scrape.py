import requests
from bs4 import BeautifulSoup
import urllib.request
import json
import pandas as pd


#   FOR UNIT TESTING
def check_connection_wiki():
    return page


#   FOR UNIT TESTING
def day_by_day_cases_test():
    table = soup.find(class_="barbox tright")
    t_body = table.find('tbody')
    tr_1 = t_body.find_all('tr', id="mw-customcollapsible-mar")
    return tr_1


def day_by_day():

    table = soup.find(class_="barbox tright")
    t_body = table.find('tbody')

    march_dates =[]
    march_total_cases = []
    march_new_cases = []

    march_deaths = []
    march_recoveries = []

    april_dates =[]
    april_total_cases = []
    april_new_cases = []

    april_deaths = []
    april_recoveries = []

    may_dates =[]
    may_total_cases = []
    may_new_cases = []

    may_deaths = []
    may_recoveries = []

    tr_1 = t_body.find_all('tr', id="mw-customcollapsible-mar")

    for i in tr_1[2:len(tr_1)]:
        td_1 = i.find('td')
        march_dates.append(td_1.text.replace('2020-03-', 'Mar '))

        span_1 = i.find_all('span')
        march_total_cases.append(int(span_1[0].text.replace(',', '')))
        march_new_cases.append(span_1[1].text.replace('(', '').replace(')', ''))

        title_1 = i.find_all('div')
        march_deaths.append(int((title_1[0])['title']))
        march_recoveries.append(int((title_1[1])['title']))



    tr_2 = t_body.find_all('tr', id="mw-customcollapsible-mar-l15")

    for j in tr_2:
        td_2 = j.find('td')
        march_dates.append(td_2.text.replace('2020-03-', 'Mar '))

        span_2 = j.find_all('span')
        march_total_cases.append(int(span_2[0].text.replace(',', '')))
        march_new_cases.append(span_2[1].text.replace('(', '').replace(')', ''))

        title_2 = j.find_all('div')
        march_deaths.append(int((title_2[0])['title']))
        march_recoveries.append(int((title_2[1])['title']))


    tr_3 = t_body.find_all(id="mw-customcollapsible-apr-l15")

    for k in tr_3:
        td_3 = k.find('td')
        april_dates.append(td_3.text.replace('2020-04-','Apr '))

        span_3 = k.find_all('span')
        april_total_cases.append(int(span_3[0].text.replace(',', '')))
        april_new_cases.append(span_3[1].text.replace('(', '').replace(')', ''))

        title_3 = k.find_all('div')
        april_deaths.append(int((title_3[0])['title']))
        april_recoveries.append(int((title_3[1])['title']))


    tr_4 = t_body.find_all(id="mw-customcollapsible-may-l15")

    for e in tr_4:
        td_4 = e.find('td')
        may_dates.append(td_4.text.replace('2020-05-','May '))

        span_4 = e.find_all('span')
        may_total_cases.append(int(span_4[0].text.replace(',', '')))
        may_new_cases.append(span_4[1].text.replace('(', '').replace(')', ''))

        title_4 = e.find_all('div')
        may_deaths.append(int((title_4[0])['title']))
        may_recoveries.append(int((title_4[1])['title']))



    global total_dates
    total_dates = march_dates+april_dates+may_dates
    global total_cases
    total_cases = (march_total_cases)+(april_total_cases)+(may_total_cases)
    global total_new_cases
    total_new_cases = (march_new_cases)+april_new_cases+may_new_cases
    global total_recoveries_day
    total_recoveries_day = march_recoveries + april_recoveries + may_recoveries
    global total_deaths_day
    total_deaths_day = march_deaths + april_deaths + may_deaths

    length = len(total_dates)
    if len(total_dates) == length and len(total_cases) == length and len(total_recoveries_day) == length and len(total_deaths_day) == length:
        return True
    else:
        return False


    #CASE TODAY
    # global case_today
    # case_today = total_cases[len(total_cases)-1]

    #ADDITIONAL CASE TODAY
    # global additional_today
    # additional_today = total_new_cases[len(total_new_cases)-1]

    #ADDTIONAL DEATHS TODAY
    # global additional_today_deaths
    # additional_today_deaths = total_deaths_day[len(total_deaths_day)-1] - total_deaths_day[len(total_deaths_day)-2]

    #ADDTIONAL RECOVERIES TODAY
    # global additional_today_recovered
    # additional_today_recovered = total_recoveries_day[len(total_recoveries_day)-1] - total_recoveries_day[len(total_recoveries_day)-2]



def by_age_test():
    table = soup.find(class_ = 'multicol', role = 'presentation')
    t_body = table.find('tbody')
    t_body_2 = t_body.find('tbody')
    tr = t_body_2.find_all('tr')

    return tr


def by_age():
    
    global age_group
    age_group = ['Above 90']
    global age_number_of_case
    age_number_of_case = []
    global age_percentage_of_case
    age_percentage_of_case =[]
    global age_number_of_deaths
    age_number_of_deaths = []
    global age_percentage_of_deaths
    age_percentage_of_deaths = []
    global age_percentage_of_lethality
    age_percentage_of_lethality = []


    table = soup.find(class_ = 'multicol', role = 'presentation')
    t_body = table.find('tbody')
    t_body_2 = t_body.find('tbody')
    tr = t_body_2.find_all('tr')


    for i in tr[6:len(tr)-1]:
        th = i.find('th')
        age_group.append(th.text.strip())

    age_group[len(age_group)-1] = 'Unknown'
        
    for i in tr[5:len(tr)-1]:
        td = i.find_all('td')
        
        age_number_of_case.append(int(td[0].text.strip()))
        age_percentage_of_case.append(float(td[1].text.strip().replace('(', '').replace(')', '')))
        age_number_of_deaths.append(int(td[2].text.strip()))
        age_percentage_of_deaths.append(float(td[3].text.strip().replace('(', '').replace(')', '')))
        if td[4].text.strip() == '–':
            age_percentage_of_lethality.append(td[4].text.strip())
        else:
            age_percentage_of_lethality.append(float(td[4].text.strip().replace('(', '').replace(')', '')))


def by_region_test():
    table = soup.find(style="text-align:center; font-size:90%")
    t_head = table.find('tbody')
    tr = t_head.find_all('tr')
    return tr


def by_region():
    global region
    region = []
    global region_cases
    region_cases = []
    global region_deaths
    region_deaths = []
    global region_active
    region_active = []
    global region_recovered
    region_recovered = []

    table = soup.find(style="text-align:center; font-size:90%")
    t_head = table.find('tbody')
    tr = t_head.find_all('tr')

    for i in tr[2:len(tr)-3]:
        th = i.find('th')
        td = i.find_all('td')
        region.append(th.text.strip())
        region_cases.append(int(td[0].text.strip()))
        region_deaths.append(int(td[1].text.strip()))
        region_active.append(int(td[3].text.strip()))
        region_recovered.append(int(td[5].text.strip()))

        headers = ['Regions', 'Total number of Cases', 'Total number of deaths', 'Total number of recoveries']
        indices = [i for i in range(1, len(region)+1)]
        global df
        df = pd.DataFrame(list(zip(region, region_cases, region_deaths, region_recovered)), columns=headers, index=indices)


def by_sex_test():
    table = soup.find(class_ = 'multicol', role = 'presentation')
    t_body = table.find('tbody')
    t_body_2 = t_body.find('tbody')
    tr = t_body_2.find_all('tr')
    return tr


def by_sex():
    global sex
    sex = ['Male', 'Female']
    global sex_number_of_case
    sex_number_of_case = []
    global sex_percentage_of_case
    sex_percentage_of_case =[]
    global sex_number_of_deaths
    sex_number_of_deaths = []
    sex_percentage_of_deaths = []
    sex_percentage_of_lethality = []


    table = soup.find(class_ = 'multicol', role = 'presentation')
    t_body = table.find('tbody')
    t_body_2 = t_body.find('tbody')
    tr = t_body_2.find_all('tr')


    for i in tr[3:len(tr)-12]:
        td = i.find_all('td')
        sex_number_of_case.append(int(td[0].text.strip()))
        sex_percentage_of_case.append(float(td[1].text.strip().replace('(', '').replace(')', '')))
        sex_number_of_deaths.append(int(td[2].text.strip()))
        sex_percentage_of_deaths.append(float(td[3].text.strip().replace('(', '').replace(')', '')))
        sex_percentage_of_lethality.append(float(td[4].text.strip().replace('(', '').replace(')', '')))


def for_total_deaths_total_recovered_test():
    url = 'https://www.worldometers.info/coronavirus/country/philippines/'
    page = requests.get(url)
    return page


def date_test():
    url = 'https://www.worldometers.info/coronavirus/country/philippines/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    main_date = soup.find(style="font-size:13px; color:#999; text-align:center")
    return main_date



def for_total_deaths_total_recovered():
    url = 'https://www.worldometers.info/coronavirus/country/philippines/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # global total_deaths
    # total_deaths = []
    # global total_recovered
    # total_recovered = []
    #
    # whole = soup.find(class_ = "col-md-8")
    # whole_1 = whole.find(class_ = 'content-inner')
    #
    # div = whole_1.find_all(id="maincounter-wrap")
    # for i in div[1:3]:
    #     span = i.find('span')
    #     total_deaths.append(int(span.text.strip()))
    #     total_recovered.append(int(span.text.strip()))
    # total_deaths.pop(1)
    # total_recovered.pop(0)

    #FOR DATE TODAY
    global dates
    dates  = []
    main_date = soup.find(style="font-size:13px; color:#999; text-align:center")
    dates.append(main_date.text.strip())


    
def cases_outside_ph():
    global outside_region
    outside_region = []
    global outside_confirmed_cases
    outside_confirmed_cases = []
    global outside_under_treatment
    outside_under_treatment = []
    global outside_recovered
    outside_recovered = []
    global outside_deaths
    outside_deaths =[]


    table = soup.find(style="text-align:right; font-size:90%; width:40%; clear:right; margin:0 0 0.5em 1em;")
    tbody = table.find('tbody')
    tr = tbody.find_all('tr')

    for i in tr[1:len(tr)-3]:
        th = i.find('th')
        outside_region.append((th.text.strip())[:-3])

        td = i.find_all('td')
        outside_confirmed_cases.append(int(td[0].text.strip()))
        outside_under_treatment.append(int(td[1].text.strip()))
        outside_recovered.append(int(td[2].text.strip()))
        outside_deaths.append(int(td[3].text.strip()))


def pui_pum_tested_connection_test():
    url = 'https://endcov.ph/dashboard/'
    page = requests.get(url)
    return page

def pui_pum_tested_test():
    url = 'https://endcov.ph/dashboard/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    main = soup.find_all(class_='h4 mb-0 font-weight-bold text-gray-800')
    return main


def pui_pum_tested():
    url = 'https://endcov.ph/dashboard/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    global pui
    pui =[]
    global pum
    pum = []
    global tested
    tested = []
    main = soup.find_all(class_ = 'h4 mb-0 font-weight-bold text-gray-800')
    pui.append(int(main[3].text.strip()))
    pum.append(int(main[4].text.strip()))
    tested.append(int(main[5].text.strip()))  


def api_connection():
    url = "https://coronavirus-ph-api.herokuapp.com/total"
    page = requests.get(url)
    return page




def api_length_of_stats():
    url = "https://coronavirus-ph-api.herokuapp.com/total"
    page = requests.get(url)
    data = json.loads(page.text)
    length_of_data = len(data['data'])
    return length_of_data


def api():
    url = "https://coronavirus-ph-api.herokuapp.com/total"
    page = requests.get(url)

    data = json.loads(page.text)
    global api_total_cases, api_total_deaths, api_total_recoveries, api_additional_cases_today, api_additional_deaths_today, api_additional_recoveries_today, api_admitted, api_fatality_rate, api_recovery_rate
    api_total_cases = data['data']['cases']
    api_total_deaths = data['data']['deaths']
    api_total_recoveries = data['data']['recoveries']
    api_additional_cases_today = data['data']['cases_today']
    api_additional_deaths_today = data['data']['deaths_today']
    api_additional_recoveries_today = data['data']['recoveries_today']
    api_admitted = data['data']['admitted']
    api_fatality_rate = data['data']['fatality_rate']
    api_recovery_rate = data['data']['recovery_rate']

# def list_of_facilities():
#     main = soup.find(id = 'bodyContent')
#     table = main.find(class_ = 'mw-content-ltr', dir = 'ltr')
#     table_2 = table.find(class_ = 'mw-parser-output')
#     for i in table_2:
#         ul = i.find('ul')
#         print(ul)

# def latest_news():
#     url = 'https://www.doh.gov.ph/2019-nCoV'
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, 'html.parser')
#
#     table = soup.find('views-table cols-3')
#     print(table)



url = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_Philippines'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')
