import threading
import time
import requests
import AdvancedHTMLParser

def parse(html):
    parser = AdvancedHTMLParser.IndexedAdvancedHTMLParser()
    parser.parseStr(html)
    return parser


class Page:
    title = ''
    page_url = ''
    object_paths = []
    interval = 60 # sekund
    login_url = ''
    login_data = {}
    login_submit = []
    session = None
    thread = None

    def __init__(self, page_url, objects, interval=None, login_url=None, login_data=None, login_submit=None):
        self.session = requests.session()
        self.page_url = page_url
        self.objects = objects
        if interval is not None:
            self.interval = interval
        if login_url is not None:
            self.login_url = login_url
        if login_data is not None:
            self.login_data = login_data
        if login_submit is not None:
            self.login_submit = login_submit

    def login(self):
        if self.login_url:
            r = self.session.get(self.login_url)
            parser = parse(r.text)
            data = self.login_data.copy()
            for input in parser.getElementsByTagName('input'):
                if input.getAttribute('type') == 'hidden':
                    data[input.getAttribute('name')] = input.getAttribute('value')
            self.session.post(self.login_url, data=data)

    def get_objects(self):
        r = self.session.get(self.page_url)
        parser = parse(r.text)
        self.title = parser.getElementsByTagName('title')[0].innerHTML
        doc = parser.getRoot()
        objs = []
        for obj_path in self.objects:
            e = doc
            for index in obj_path:
                e = e.getChildren()[index]
            objs.append(e.innerHTML)
        return objs


pages = [
    Page('https://usosweb.mimuw.edu.pl/kontroler.php?_action=dla_stud/studia/sprawdziany/pokaz&wez_id=86594',
         [[1, 1, 2, 0, 1, 0, 0, 0, 7, 1, 4, 0, 2, 0]], # ocena z kartkówki z sieci
         30,
         'https://logowanie.uw.edu.pl/cas/login?service=https%3A%2F%2Fusosweb.mimuw.edu.pl%2Fkontroler.php%3F_action%3Dlogowaniecas%2Findex&locale=pl',
         {'username': '123456789', 'password': 'qwerty'}),
    Page('http://frazpc.pl',
         [[1, 7, 1, 0, 0, 0, 2, 1, 0, 0, 0], [1, 7, 1, 0, 0, 0, 2, 1, 1, 0, 0]], # nagłówki dwóch pierwszych artykułów
         20)]


def worker(page):
    page.login() # TODO: obsługa wylogowania
    objs = page.get_objects()
    working = True
    while working:
        time.sleep(page.interval)
        new_objs = page.get_objects()
        for i in range(len(objs)):
            if objs[i] != new_objs[i]:
                print('Zmiana na stronie "' + page.title + '": ' + objs[i] + ' -> ' + new_objs[i])
        objs = new_objs
        #print(objs) # wyświetla aktualne wartości obiektów


for page in pages:
    page.thread = threading.Thread(target=worker, args=(page,))
    page.thread.start()

