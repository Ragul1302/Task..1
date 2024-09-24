import
urllib.request
from html.parser import HTMLParser


# Define a custom HTML parser class
class ProductHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_product = False
        self.current_tag = None
        self.product_names = []
        self.prices = []
        self.ratings = []
        self.current_name = ''
        self.current_price = ''
        self.current_rating = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            # Check for the start of a product block
            attrs_dict = dict(attrs)
            if attrs_dict.get('class') == 'product':
                self.in_product = True
        elif self.in_product:
            if tag == 'h2' and ('class', 'product-name') in attrs:
                self.current_tag = 'name'
            elif tag == 'p' and ('class', 'price') in attrs:
                self.current_tag = 'price'
            elif tag == 'span' and ('class', 'rating') in attrs:
                self.current_tag = 'rating'

    def handle_endtag(self, tag):
        if tag == 'div' and self.in_product:
            # End of a product block
            self.in_product = False
            self.product_names.append(self.current_name)
            self.prices.append(self.current_price)
            self.ratings.append(self.current_rating)
            self.current_name = ''
            self.current_price = ''
            self.current_rating = ''
        elif tag == 'h2' or tag == 'p' or tag == 'span':
            self.current_tag = None

    def handle_data(self, data):
        if self.current_tag == 'name':
            self.current_name += data.strip()
        elif self.current_tag == 'price':
            self.current_price += data.strip()
        elif self.current_tag == 'rating':
            self.current_rating += data.strip()


def scrape_products(url):
    # Fetch the HTML content of the page
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')

    # Parse the HTML content
    parser = ProductHTMLParser()
    parser.feed(html)

    # Print the extracted data
    print("Product Name, Price, Rating")
    for name, price, rating in zip(parser.product_names, parser.prices, parser.ratings):
        print(f"{name}, {price}, {rating}")


# URL of the webpage to scrape
url = 'http://example.com/products'  # Replace with the actual URL

# Call the function to scrape and print the products
scrape_products(url)