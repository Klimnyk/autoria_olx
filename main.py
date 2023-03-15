import os
from datetime import date, datetime

import gspread
import gspread_dataframe
import pandas as pd
import requests

import json

SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
PATH = os.path.dirname(__file__)
CREDENTIALS_PATH = os.path.abspath(os.path.join(PATH, "json", "credentials"))
G_SHEET_ID = '1IrjiD-qLJ_4hks329RgXJ-qqQYWlZAnRYUMrOFHFa9g'


def load_json(filename):
    filepath = os.path.abspath(os.path.join(PATH, "json", filename))
    with open(filepath) as filepath:
        data = json.load(filepath)
    return data


def fetch_data_from_autoria():
    autoria_api_url = "https://auto.ria.com/api/search/auto?indexName=auto&category_id=1&state[0]={}"
    region_json = load_json('autoria_regions.json')
    autoria_data = []

    with requests.Session() as session:
        for item in region_json:
            url = autoria_api_url.format(item['id'])
            try:
                response = session.get(url)
                response.raise_for_status()
                response_json = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while requesting {url}: {e}")
                continue

            result = response_json.get('result')
            if result:
                search_result = result.get('search_result')
                if search_result:
                    count = search_result.get('count')
                    if count:
                        region = item.get('region')
                        autoria_data.append(
                            {
                                'date': date.today().strftime("%Y-%m-%d"),
                                'region': region,
                                'count': count,
                            }
                        )
    to_gspread('py-autoria', pd.DataFrame(autoria_data))


def to_gspread(worksheet_name, dataframe):
    gc = gspread.service_account(filename=os.path.join(CREDENTIALS_PATH, "google_credentials.json"))
    sh = gc.open_by_key(G_SHEET_ID)
    worksheet = sh.worksheet(worksheet_name)
    existing_df = pd.DataFrame(worksheet.get_all_records()).dropna()
    updated = pd.concat([existing_df, dataframe])
    worksheet.clear()
    gspread_dataframe.set_with_dataframe(worksheet, updated)


def fetch_data_from_olx():
    url_olx = 'https://www.olx.ua/api/v1/offers/metadata/search/?offset=0&limit=40&category_id=108&currency=UAH&filter_refiners=spell_checker&facets=[{"field":"region","fetchLabel":true,"fetchUrl":true,"limit":30}]'

    try:
        with requests.Session() as session:
            # todo fix it
            data = {
                'client_id': "100018",
                'client_secret': "mo96g2Wue78VBZrhghjVJwmJk7Adn0LTs3ZI6Vdk3lgXk5hi",
                'device_id': "e0be0658-1fde-4dbb-a3a4-d687bf05c7c9",
                'device_token': "eyJpZCI6ImUwYmUwNjU4LTFmZGUtNGRiYi1hM2E0LWQ2ODdiZjA1YzdjOSJ9.e14605f76d71cfeef568b8f8bbd4823bf85e7bf9",
                'grant_type': "device",
                'scope': "i2 read write v2"
            }
            r = session.post('https://www.olx.ua/api/open/oauth/token/', data=data)
            r.raise_for_status()
            access_token = r.json()['access_token']

            r = session.get(url_olx, headers={'authorization': f'Bearer {access_token}'})
            r.raise_for_status()
            olx_data = r.json()['data']['facets']['region']
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

    df = pd.json_normalize(olx_data)
    df['date'] = datetime.today().strftime('%Y-%m-%d')
    to_gspread('py-olx', df[['date', 'label', 'count']].rename(columns={'label': 'region'}))


if __name__ == '__main__':
    fetch_data_from_olx()
    fetch_data_from_autoria()
