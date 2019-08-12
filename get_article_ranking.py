import datetime
import json
import urllib.request

obtained_articles = []
PER_PAGE = 100
like_number_criteria = 10
MAX_PAGINATE = 100
updated_at_criteria = datetime.date.today() + datetime.timedelta(days=-30)
BASE_URI = 'https://qiita.com/api/v2/items'


def convert_str_to_dt(str_datetime):
    dt = datetime.datetime.strptime(str_datetime[:10], '%Y-%m-%d')
    date = datetime.date(dt.year, dt.month, dt.day)
    return date


def set_items(http_body):
    for item in http_body:
        updated_date = convert_str_to_dt(item.get('updated_at'))
        print(item.get('likes_count'))
        if item.get('likes_count') >= like_number_criteria and updated_at_criteria <= updated_date:
            obtained_articles.append(item)


def issue_request(req):
    with urllib.request.urlopen(req) as res:
        body = json.load(res)
        set_items(body)


def set_articles(paginate_number):
    get_items_uri = BASE_URI + f'?page={paginate_number}&per_page={PER_PAGE}'
    req = urllib.request.Request(get_items_uri)
    issue_request(req)


try:
    for i in range(1, MAX_PAGINATE):
        set_articles(i)
except urllib.error.HTTPError as err:
    print(err.code)
except urllib.error.URLError as err:
    print(err.reason)

print(obtained_articles)


