
Scrapy is a fast high-level [web crawling](https://en.wikipedia.org/wiki/Web_crawler) and [web scraping](https://en.wikipedia.org/wiki/Web_scraping) framework, used to crawl websites and extract structured data from their pages. It can be used for a wide range of purposes, from data mining to monitoring and automated testing.

Using Scrapy you can easily build highly scalable scrapers that will retrieve a pages HTML, parse and process the data, and store it the file format and location of your choice.

#### create a virtual environment

```zsh
python3 -m venv [name]

source venv/bin/active
```

#### create a project

```zsh
scrapy startproject [name] #e.g. scrapy startproject bookscraper
```

#### start the project
we will use `https://books.toscrape.com/` as a practice example

```zsh

cd ../spiders

# scrapy genspider [nameyourspider] [website to scrape]

scrapy genspider bookspider books.toscrape.com
```



go to `scrapy.cfg` and add this `shell = ipython` to make it easier to read the output. Install `python3 install ipython` first
`scrapy shell` command to start it
**NOTE:** This is just for practice so you will have to write the code in the `bookspider.py` `parse()` function and you'll have to go to the browser and inspect it to find what you are looking for
The shell is used for preview purposes to make sure that the commands work

`scrapy shell`
```zsh
> scrapy shell "https://quotes.toscrape.com"

fetch('https://books.toscrape.com/')

response.css('article.product_pod') #to fetch the products(books) which is under css article tag 
books = response.css('article.product_pod') #to put the books returned into a variable
len(books) #to check how many product are there in the extracted books response

book = books[0]
book.css('h3 a::text').get() #to get the title of the first book in the list 
book.css('.product_price .price_color::text').get() #to get the price
book.css('h3 a').attrib['href'] #to get the url of the product details

response.css('li.next a ::attr(href)').get() #to get the next page url


```

#### For real code instead of practicing on the shell


`bookspider.py`
```python
import scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    # This method is called once we get a response from the website
    def parse(self, response):
        books = response.css('article.product_pod')
        
        for book in books:
            yield {  # yield (return)
                'name': book.css('h3 a::text').get(),
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }
            
        # Get the next page link
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            # The next page URLs might differ in structure
            if 'catalogue/' in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
                
            # Follow the next page and call parse() again
            yield response.follow(next_page_url, callback=self.parse)

```
`> scrapy crawl bookspider`  to run the file

#### Going into the details section of a book(product)
Now we will be diving into the details link of a single book and getting more data about it and then looping through all the other books until nothing is left

```python

import scrapy

class BookspiderSpider(scrapy.Spider):
    # Name used to run the spider: scrapy crawl bookspider
    name = 'bookspider'
    # Restrict crawling to this domain
    allowed_domains = ['books.toscrape.com']
    # Starting URL for the spider
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        # Select all book containers on the page
        books = response.css('article.product_pod')
        for book in books:
            # Extract the relative URL of the book detail page
            # ::attr(href) means "get the value of the href attribute"
            relative_url = book.css('h3 a::attr(href)').get()

            # Build the full book URL depending on whether 'catalogue/' is present
            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url

            # Follow the book detail page and call parse_book_page
            yield response.follow(book_url, callback=self.parse_book_page)

        # Handle pagination: find the "next" page link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            # Build the full next page URL depending on structure
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page

            # Follow the next page and call parse() again
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        # Select all rows in the product information table
        table_rows = response.css("table tr")

        # Yield a dictionary of extracted data
        yield {
            'url': response.url,  # Current page URL
            'title': response.css('.product_main h1::text').get(),  # Book title

            # Table rows contain product info in fixed positions
            'product_type': table_rows[1].css("td::text").get(),
            'price_excl_tax': table_rows[2].css("td::text").get(),
            'price_incl_tax': table_rows[3].css("td::text").get(),
            'tax': table_rows[4].css("td::text").get(),
            'availability': table_rows[5].css("td::text").get(),
            'num_reviews': table_rows[6].css("td::text").get(),

            # Star rating is stored in the class attribute of <p class="star-rating ...">
            'stars': response.css("p.star-rating").attrib['class'],

            # XPath explanation:
            # //ul[@class='breadcrumb'] → find the breadcrumb navigation list
            # /li[@class='active'] → locate the current page (active breadcrumb item)
            # /preceding-sibling::li[1]/a/text() → go one step back (the category link before "active")
            # and extract its text
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),

            # XPath explanation:
            # //div[@id='product_description'] → locate the product description header
            # /following-sibling::p/text() → get the paragraph immediately after it (the actual description)
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),

            # Price displayed on the page
            'price': response.css('p.price_color::text').get(),
        }


```
`scrapy crawl bookspider -O bookdata.csv`  to run and put the data into a csv file



# Cleaning Data with Items and Item pipeline

This is creating an organized form of the output data and error handling

`items.py`
```python

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

def serialize_price(value):
    return f'£ {str(value)}'

class BookItem(scrapy.Item):
   url = scrapy.Field()
   title = scrapy.Field()
   upc = scrapy.Field()
   product_type = scrapy.Field()
   price_excl_tax = scrapy.Field()
   price_incl_tax = scrapy.Field()
   tax = scrapy.Field()
   availability = scrapy.Field()
   num_reviews = scrapy.Field()
   stars = scrapy.Field()
   category = scrapy.Field()
   description = scrapy.Field()
   price = scrapy.Field()

```

[Item Pipelines](https://docs.scrapy.org/en/latest/topics/item-pipeline.html) are the data processors of Scrapy, which all our scraped Items will pass through and from where we can clean, process, validate, and store our data.

Using Scrapy Pipelines we can:

- Clean our data (ex. remove currency signs from prices)
- Format our data (ex. convert strings to ints)
- Enrich our data (ex. convert relative links to absolute links)
- Valdiate our data (ex. make sure the price scraped is a viable price)
- Store our data in databases, queues, files or object storage buckets.

In our Scrapy project, we will use Item Pipelines to clean and process our data before storing it in a database.

`pipelines.py`
```python

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## Strip all whitespaces from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        ## Availability --> extract number of books in stock
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        ## Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        ## Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5

        return item

```

---

The `BookscraperPipeline` should correspond to the name of the class in the `pipelines.py` file
NOTE: this line is automatically generated by scrapy and all you have to do is uncomment it.
`settings.py`
```python

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'bookscraper.pipelines.BookscraperPipeline': 300,
}

```

---

`bookspider.py`
```python

import scrapy
from bookscraper.items import BookItem  

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)


    def parse_book_page(self, response):

        table_rows = response.css("table tr")
        book_item = BookItem()

        book_item['url'] = response.url,
        book_item['title'] = response.css('.product_main h1::text').get(),
        book_item['upc'] = table_rows[0].css("td ::text").get()
        book_item['product_type' ] = table_rows[1].css("td ::text").get(),
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get(),
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get(),
        book_item['tax'] = table_rows[4].css("td ::text").get(),
        book_item['availability'] = table_rows[5].css("td ::text").get(),
        book_item['num_reviews']=  table_rows[6].css("td ::text").get(),
        book_item['stars'] = response.css("p.star-rating").attrib['class'],
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        book_item['price'] = response.css('p.price_color ::text').get(),
    
        yield book_item

```


# Saving Data to files and Databases

One you can use the command line method `scrapy crawl bookspider -O bookdata.csv`
Second you can use the settings method and add this like to save in a json or any format and just run it as usual `scrapy crawl bookspider`

`settings.py`
```python

FEEDS = {
    'booksdata.json': {'format': 'json'},
}

```

#### saving to database
We will be using the pipeline and mysql database
- Create a database using mysql
- Install mysql connector `pip3 install mysql mysql-connector-python`
- Now we can use the database using pipelines by adding the code below to the already existing code in pipelines

`pipelines.py`
```python

import mysql.connector

class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '', #add your password here if you have one set 
            database = 'books'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"][0])
        ))

        # ## Execute insert of data into database
        self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

```

`settings.py`
```python

ITEM_PIPELINES = {
   'bookscraper.pipelines.BookscraperPipeline': 300,
   'bookscraper.pipelines.SaveToMySQLPipeline': 400,
}

```
`> scrapy crawl bookspider`

