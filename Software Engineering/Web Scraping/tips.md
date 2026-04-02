
## 🧩 Step 1: Get Comfortable with HTML & CSS Selectors

- **HTML basics**: Think of HTML as a tree. Tags like `<div>`, `<p>`, `<a>` are nodes. Attributes like `class="title"` or `id="main"` are labels.
    
- **CSS selectors**: These are shortcuts to find elements:
    
    - `div.title` → a `<div>` with class "title"
        
    - `#main` → element with id "main"
        
    - `a[href]` → all links with an `href` attribute
        
- **Practice tip**: Open any website in Chrome/Firefox → right‑click → _Inspect_. Hover over elements and try writing CSS selectors in the console (`document.querySelectorAll("selector")`).

## 🧩 Step 2: Learn XPath by Analogy

XPath looks scary, but it’s just another way to navigate the HTML tree:

- `//div` → all `<div>` tags
    
- `//div[@class="title"]` → `<div>` with class "title"
- 
- `//a/text()` → text inside all `<a>` tags
    
- `//h1[1]` → the first `<h1>` tag
    

👉 Think of XPath as “directions” in the tree. Start at the root (`//`) and walk down.

## 🧩 Step 3: Scrapy in Action

Here’s a simple spider that extracts titles and links:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://quotes.toscrape.com"]

    def parse(self, response):
        # Using CSS selectors
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall(),
            }

        # Follow pagination link
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

## 🧩 Step 4: Practice with Real Sites

- Start with **quotes.toscrape.com** (built for practice).
- Move to **books.toscrape.com** (great for product scraping).
- Then try a Kenyan site you know (like news or e‑commerce). Inspect elements, write selectors, test them in Scrapy.

## 🧩 Step 5: Build Muscle Memory

- Use **Scrapy shell**:
    
    ```bash
    scrapy shell "http://quotes.toscrape.com"
    ```
    
    Then test selectors interactively:
    
    ```python
    response.css("span.text::text").get()
    response.xpath("//small[@class='author']/text()").get()
    ```
    
- Compare CSS vs XPath until you feel which one is easier for you.
    

## 📌 Key Tips

- **Start small**: Extract one element at a time (title, link, price).
    
- **Use Scrapy shell**: It’s your playground for selectors.
    
- **Prefer CSS selectors**: They’re simpler; use XPath only when CSS can’t handle it.
    
- **Practice daily**: Even 15 minutes of writing selectors on random sites builds confidence.