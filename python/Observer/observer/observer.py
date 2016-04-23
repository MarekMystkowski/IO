import random, string, json
import socket, os, time, threading
import requests, AdvancedHTMLParser

def parse(html):
    parser = AdvancedHTMLParser.IndexedAdvancedHTMLParser()
    parser.parseStr(html)
    return parser


class Page:
    title = ''
    url = ''
    paths = []
    interval = 60 # sekund
    login_url = ''
    login_data = {}
    session = None
    thread = None

    def __init__(self, url, paths, interval=None, login_url=None, login_data=None, login_submit=None):
        self.session = requests.session()
        self.url = url
        self.paths = paths
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
            self.session.post(self.login_url, data)

    def get_objects(self):
        r = self.session.get(self.url)
        parser = parse(r.text)
        self.title = parser.getElementsByTagName('title')[0].innerHTML
        doc = parser.getRoot()
        objs = []
        for obj_path in self.paths:
            e = doc
            prev_tag = e.tagName
            for index in obj_path:
                # pomijamy dodawany przez przeglądarki znacznik tbody
                ignore = False
                if prev_tag == 'table' and e.tagName != 'tbody' and e.tagName != 'thead':
                    ignore = True
                prev_tag = e.tagName
                if not ignore:
                    e = e.getChildren()[index]
            objs.append(e.innerHTML)
        return objs


def worker(page):
    page.login() # TODO: obsługa wylogowania
    objs = page.get_objects()
    working = True
    while working:
        time.sleep(page.interval)
        new_objs = page.get_objects()
        #for i in range(len(objs)):
        #    if objs[i] != new_objs[i]:
        #        print('Zmiana na stronie "' + page.title + '": ' + objs[i] + ' -> ' + new_objs[i])
        objs = new_objs
        print(objs) # wyświetla aktualne wartości obiektów


# id urządzenia
try:
    f = open('device_id', 'r')
    device_id = f.read()
except FileNotFoundError:
    device_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    with open('device_id', 'w') as f:
        f.write(device_id)
    # to działa chyba tylko na Windowsie, ale webbrowser.open ma jakiś problem i otwiera stronę w IE zamiast w Chromie
    os.startfile('http://127.0.0.1:8000/add_device?device_id=' + device_id + '&device_name=' + socket.gethostname())


# pobranie listy stron
r = requests.post('http://127.0.0.1:8000/api/page_list/', {'device_id': device_id})
pages = [Page(d['url'], d['paths'], int(d['interval']), d['login_url'], d['login_data']) for d in json.loads(r.text)]


# wątki do obserwowania stron
for page in pages:
    page.thread = threading.Thread(target=worker, args=(page,))
    page.thread.start()

