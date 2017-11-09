from Library.Scroll import Scroll
import re
from collections import defaultdict
import bs4

class IndeedCrawler(Scroll):

    def __init__(self):

        self.base_url = "https://www.indeed.ae"
        url_parts = [self.base_url+"/jobs?q=","&l="]
        urls = defaultdict(list)

        for location in self.search_location:
            for search in self.search_parameters:
                url = url_parts[0] + '+'.join(search) + url_parts[1] + location
                urls[" ".join(search)].append(url)

        super(IndeedCrawler, self).__init__(urls, "indeed" )

    def check_pagination(self, url, source_code):
        soup = bs4.BeautifulSoup(source_code, 'html.parser')
        pages = set()


        pages_count = soup.select("#searchCount")

        count = re.findall(r'\d+$', pages_count[0].text)

        total_pages = count[0]
        if total_pages:

            pages = [i for i in range(10, int(total_pages) + 1, 5)]

        pages = sorted(pages)
        parameter_page = [['', '&start=' + str(page), page] for page in pages]

        return parameter_page


    def extract_jobs_from_source(self, source_code):
        jobs = []
        webpage = "Indeed.ae"
        soup = bs4.BeautifulSoup(source_code, 'html.parser')
        entries = soup.select("#resultsCol .row.result")
        for entry in entries:
            title = entry.select("h2.jobtitle a")
            job_title = title[0].text if len(title)>0 else ""
            location = entry.select("span.location")
            job_location = location[0].text if len(location)>0 else ""
            company = entry.select("span.company")
            job_company = company[0].text if len(company)>0 else ""
            online = ''
            ln = entry.select("h2.jobtitle a")
            link = self.base_url + ln[0].get("href") if len(ln)>0 else ""
            jobs.append([webpage, job_title, job_location, job_company, str(online), link])
        return jobs

    def start_crawling(self):
        print("Start %s..." % __name__)
        return super(IndeedCrawler, self).start_crawling()