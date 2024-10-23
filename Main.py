from requests.structures import CaseInsensitiveDict
from datetime import date, datetime
import pandas as pd
import jdatetime
import requests
import time

print("Welcome to Basalam Product Scraper!")
word = input("Enter KeyWord For Search : ")
num_of_products = int(input("Enter Number Of Products : "))

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Accept"] = "application/json"

ids = []

for i in range(1, num_of_products, 24):
    print(i, 'to', min(num_of_products, (i + 24)))
    resp = requests.get(
        f"https://search.basalam.com/ai-engine/api/v2.0/product/search?productAds=false&adsImpressionDisable=true&q={word}&bazarGardy=false&from={i}&size={num_of_products - i + 1}&filters.hasDiscount=false&filters.isReady=false&filters.isExists=true&filters.hasDelivery=false&filters.queryNamedTags=false",
        headers=headers)
    resp.raise_for_status()
    basalam_data = resp.json()["products"]
    print(f"Number of products received: {len(basalam_data)}")
    for product in basalam_data:
        ids.append(product['id'])

print(f"Total number of IDs collected: {len(ids)}")

final_data = []

for product_id in ids:
    try:
        product_resp = requests.get(
            f"https://core.basalam.com/v3/products/{product_id}",
            headers=headers
        )
        product_resp.raise_for_status()
        product_data = product_resp.json()  

        attributes_dict = {}
        attr_index = 1
        for group in product_data.get('attribute_groups', []):
            group_title = group['title']
            for attr in group.get('attributes', []):
                attributes_dict[f'title_{attr_index}'] = attr['title']
                attributes_dict[f'value_{attr_index}'] = attr['value']
                attributes_dict[f'unit_{attr_index}'] = attr.get('unit', '')
                attr_index += 1

        category_parent_titles = []
        category = product_data.get('category')
        while category and category.get('parent'):
            category_parent_titles.append(category['parent']['title'])
            category = category['parent']

        product_details = {
            'id': product_data['id'],
            'title': product_data['title'],
            'price': product_data.get('price', None),
            'photo_lg': product_data['photo']['lg'] if product_data.get('photo') else '',
            'photo_md': product_data['photo']['md'] if product_data.get('photo') else '',
            'photos_lg': [photo['lg'] for photo in product_data.get('photos', [])],
            'category_title': product_data['category']['title'] if product_data.get('category') else None,
            'category_parent_titles': ' > '.join(category_parent_titles) if category_parent_titles else None,
            'tags': [cat['title'] for cat in (product_data.get('category_list') or []) if cat],
            'description': product_data.get('description', None),
            'navigation_title': product_data['navigation']['title'] if product_data.get('navigation') else None,
            'navigation_category_parent_title': product_data['navigation']['parent']['title'] if product_data.get('navigation') and product_data['navigation'].get('parent') else None,
            'seller': product_data['vendor']['title'] if product_data.get('vendor') else None,
            'weight': product_data.get('net_weight', None),
            'rating': product_data.get('rating', None),
            'review_count': product_data.get('review_count', None),
            'time': str(jdatetime.date.fromgregorian(date=date.today())),
        }

        product_details.update(attributes_dict)
        final_data.append(product_details)

        time.sleep(0.5)

    except requests.RequestException as e:
        print(f"Failed to get data for product ID {product_id}: {e}")

data = pd.DataFrame(final_data)

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = "basalam_products_" + current_time + ".xlsx"

data.to_excel(file_name, index=False, engine='openpyxl')

print(f"Data successfully saved to {file_name}")
