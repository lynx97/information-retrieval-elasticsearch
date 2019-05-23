import scrapy
import datetime
from elasticsearch import Elasticsearch


class VnExpress(scrapy.Spider):
    name = 'auto_crawler'

    start_urls = [
        'https://vnexpress.net/the-thao',
        'https://vnexpress.net/giao-duc',
        'https://vnexpress.net/thoi-su',
        'https://vnexpress.net/the-gioi',
        'https://vnexpress.net/kinh-doanh',
        'https://vnexpress.net/giai-tri',
        'https://vnexpress.net/phap-luat',
        'https://vnexpress.net/suc-khoe',
        'https://vnexpress.net/doi-song',
        'https://vnexpress.net/du-lich',
        'https://vnexpress.net/khoa-hoc',
        'https://vnexpress.net/tam-su'

    ]

    def __init__(self):
        self.categories = {
            'the-thao': 'thể thao',
            'giao-duc': 'giáo dục',
            'thoi-su': 'thời sự',
            'the-gioi': 'thế giới',
            'kinh doanh': 'kinh doanh',
            'giai-tri': 'giải trí',
            'phap-luat': 'pháp luật',
            'suc-khoe': 'sức khỏe',
            'doi-song': 'đời sống',
            'du-lich': 'du lịch',
            'khoa-hoc': 'khoa học',
            'tam-su': 'tâm sự'
        }
        self.current_category = None
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
        self.now = datetime.datetime.now()
        self.two_hours_before = self.now - datetime.timedelta(hours=2)

    def parse(self, response):
        for v in self.categories.keys():
            if v in response.url:
                self.current_category = self.categories[v]
                break

        list_news = response.css('.sidebar_1 .list_news')
        news_urls = [v.css('.title_news a::attr(href)').get() for v in list_news]

        for url in news_urls:
            yield scrapy.Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        sentences = response.css('.content_detail p::text').getall()
        content = ' '.join(v for v in sentences)
        upload_time = response.css('.sidebar_1 .time::text').get()
        upload_time = upload_time[upload_time.index(',') + 2: upload_time.index('(') - 1]

        #  nếu là tin tức chỉ chứa video, bỏ qua
        if content != "":
            data = {
                'id': response.css('.myvne_save_for_later::attr(data-article-id)').get(),
                'upload_time': upload_time,
                'title': response.css('.title_news_detail::text').get().strip(),
                'description': response.css('.description::text').get().strip(),
                'content': content.strip(),
                'url': response.url,
                'category': self.current_category
            }

            if self.check_latest_time(data['upload_time']):
                # chèn data theo id của bài viết, nếu bài viết đã tồn tại trong elasticsearch nó sẽ tăng số version
                self.es.index(index='vn', doc_type='article', id=data['id'], body=data)

    def check_latest_time(self, string_date):
        day = datetime.datetime.strptime(string_date, '%d/%m/%Y, %H:%M')

        if self.two_hours_before <= day <= self.now:
            return True
        return False
