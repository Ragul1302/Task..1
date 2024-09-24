import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'http://example.com/products'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    product_names = []
    prices = []
    ratings = []


    products = soup.find_all('div', class_='product')

    for product in products:
        name = product.find('h2', class_='product-name').get_text(strip=True)
        product_names.append(name)

        price = product.find('p', class_='price').get_text(strip=True)
        prices.append(price)

        rating = product.find('span', class_='rating').get_text(strip=True)
        ratings.append(rating)

    df = pd.DataFrame({
        'Product Name': product_names,
        'Price': prices,
        'Rating': ratings
    })

    df.to_csv('products.csv', index=False)

    print('Data has been successfully scraped and saved to products.csv')
else:
    print(f'Failed to retrieve page with status code: {response.status_code}')