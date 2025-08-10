import scrapy
from bs4 import BeautifulSoup

class AcademicSpider(scrapy.Spider):
    name = "academic_spider"
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org/list/cs.AI/recent"]

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract paper links
        for paper in soup.select("dt a[href^='/abs/']"):
            link = response.urljoin(paper.get("href"))
            yield scrapy.Request(link, callback=self.parse_paper)

    def parse_paper(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        
        title = soup.find("h1", class_="title").get_text(strip=True).replace("Title:", "") if soup.find("h1", class_="title") else None
        abstract = soup.find("blockquote", class_="abstract").get_text(strip=True).replace("Abstract:", "") if soup.find("blockquote", class_="abstract") else None

        yield {
            "url": response.url,
            "title": title,
            "abstract": abstract
        }
