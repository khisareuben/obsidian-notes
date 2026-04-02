
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

#### Going into the details section of a book(product)
Now we will be diving into the details link of a single book and getting more data about it

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


## 🧭 Core Concepts of XPath

- **Absolute vs Relative Paths**
    
    - `/html/body/div` → starts from the root (absolute).
    - `//div` → searches anywhere in the document (relative, more flexible).
        
- **Basic Syntax**
    
    - `//tagname` → selects all elements with that tag.
    - `//tagname[@attribute='value']` → selects elements with a specific attribute.
    - `//tagname/text()` → extracts the text inside the element.
    - `//tagname/@href` → extracts the value of the `href` attribute.
## 🔗 Navigating Relationships

XPath shines when you need to move between related elements:

- **Parent → Child**
    - `//div[@class='product']/p` → finds `<p>` inside a `<div class="product">`.

- **Sibling Navigation**
    
    - `preceding-sibling::li[1]` → selects the `<li>` immediately before the current one.
    - `following-sibling::p` → selects the `<p>` immediately after the current node.
        
- **Ancestor/Descendant**
    
    - `ancestor::ul` → moves up to the parent `<ul>`.
    - `descendant::span` → finds all `<span>` inside the current node.

## 📊 Example from Your Spider

- **Category Extraction*
    
    ```xpath
    //ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()
    ```
    
    - Find the breadcrumb list (`ul[@class='breadcrumb']`).
    - Locate the active item (`li[@class='active']`).
    - Move one step back (`preceding-sibling::li[1]`).
    - Get the text inside its `<a>` tag.
        
- **Description Extraction**
    
    ```xpath
    //div[@id='product_description']/following-sibling::p/text()
    ```
    
    - Find the div with id `product_description`.
    - Move to the next `<p>` after it (`following-sibling::p`).
    - Extract its text.
        
## ✅ Why Use XPath Instead of CSS

- **CSS selectors** are simpler for direct matches (`.class`, `#id`, `tag[attr=value]`).    
- **XPath** is more powerful when you need:
    
    - To move between siblings or parents.
    - To extract based on position (`[1]`, `[last()]`).
    - To combine conditions (`//div[@class='x' and @id='y']`).
## 📝 Minimal Notes

- XPath = “path language” for navigating HTML/XML.
- Use `//` for relative search, `@` for attributes, `/` for hierarchy.
- `preceding-sibling` and `following-sibling` let you move sideways in the DOM.
- In your spider, XPath is used to grab **category** and **description** because they’re not easily accessible with CSS alone.