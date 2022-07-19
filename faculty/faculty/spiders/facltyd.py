from abc import ABC

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class FacltydSpider(CrawlSpider):
    name = 'facltyd'
    allowed_domains = ['bennett.edu.in']
    start_urls = ['https://www.bennett.edu.in']

    rules = (
        Rule(LinkExtractor(allow='/faculties'), callback='parse_item'),
        Rule(LinkExtractor(allow='/academics'), ),
        Rule(LinkExtractor(allow='/admission'), ),
        Rule(LinkExtractor(allow='#'), ),
    )

    def parse_item(self, response):

        Name = response.css("h1::text").get()
        Designation = response.css("._desgi::text").get()
        School = response.css("li:nth-child(1) .depart-name::text").get()
        Department = response.css("li:nth-child(2) .depart-name::text").get()
        Position = response.css("li:nth-child(3) .depart-name::text").get()
        Email = response.css(".depart-name a::text").get()
        About = response.css(".profile-discription::text").get()
        if About is not None:
            About.strip()
        Education = response.css(".firsr-bx.style-bx span , .firsr-bx h5::text").extract()
        Education = [e.replace('<span>','') for e in Education]
        Education = [e.replace('<h5>','') for e in Education]
        Education = [e.replace('</span>','') for e in Education]
        Education = [e.replace('</h5>','') for e in Education]
        Experience = response.css(".slide-right h5+ span::text").extract()
        Research = response.css(".style-bx2 span::text").extract()
        Projects = response.css(".scrolling-details div::text").extract()
        Projects = [x.strip() for x in Projects]
        Projects = list(filter(len, Projects))
        Distinction = response.css(".slide-left .nano-content span::text").extract()
        Image = response.css(".bn-profile-img img::attr(src)").get()
        profile = response.url

        yield {
            'Name': Name,
            "Image": Image,
            'Designation': Designation,
            'School': School,
            'Department': Department,
            'Position': Position,
            'Email': Email,
            'About': About,
            'Education': Education,
            'Experience': Experience,
            "Research": Research,
            "Projects": Projects,
            "Distinction": Distinction,
            'profile': profile

        }

