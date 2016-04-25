import random, string, json
import socket, os, time, threading
import requests, AdvancedHTMLParser

def parse(html):
    parser = AdvancedHTMLParser.IndexedAdvancedHTMLParser()
    parser.parseStr(html)
    return parser


class Page:
    id = 0
    url = ''
    paths = []
    interval = 60 # sekund
    login_url = ''
    login_data = {}
    session = None
    thread = None

    def __init__(self, id, url, paths, interval=None, login_url=None, login_data=None, login_submit=None):
        self.session = requests.session()
        self.id = id
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

    # loguje się na stronę
    def login(self):
        if self.login_url:
            r = self.session.get(self.login_url)
            parser = parse(r.text)
            data = self.login_data.copy()
            for input in parser.getElementsByTagName('input'):
                if input.getAttribute('type') == 'hidden':
                    data[input.getAttribute('name')] = input.getAttribute('value')
            self.session.post(self.login_url, data)

    # zwraca listę obserwowanych obiektów
    def get_objects(self):
        r = self.session.get(self.url)
        parser = parse(r.text)
        #self.title = parser.getElementsByTagName('title')[0].innerHTML
        doc = parser.getRoot()
        objs = []
        for obj_path in self.paths:
            e = doc
            # pomijamy dodawany przez parser drugi znacznik html
            if e.tagName == 'html' and e.getChildren()[0].tagName == 'html':
                e = e.getChildren()[0]
            prev_tag = e.tagName
            for index in obj_path:
                # pomijamy dodawany przez przeglądarki znacznik tbody
                ignore = False
                if prev_tag == 'table' and e.tagName != 'tbody' and e.tagName != 'thead':
                    ignore = True
                prev_tag = e.tagName
                if not ignore:
                    children = e.getChildren()
                    if len(children) <= index:
                        return None # błąd!
                    e = children[index]
            objs.append(e.innerHTML)
        return objs

    # wysyła informację o zmianie na serwer
    def notify(self, old_value, new_value):
        print("Zmiana na stronie " + self.url + ": " + old_value + " -> " + new_value)
        r = requests.post('http://127.0.0.1:8000/api/new_change/', {'device_id': device_id, 'page_id': self.id, 'old_value': old_value, 'new_value': new_value})
        if r.status_code != 200:
            print("Error %d: " % r.status_code + r.text)
            exit()


def worker(page):
    page.login()
    objs = page.get_objects()
    working = True
    while working:
        time.sleep(page.interval)
        new_objs = page.get_objects()
        # w przypadku wykrycia zmiany (albo błędu) logujemy się ponownie
        if objs != new_objs:
            page.login()
            new_objs = page.get_objects()
        # TODO: obsługa błędów
        for i in range(len(objs)):
             if objs[i] != new_objs[i]:
                 page.notify(objs[i], new_objs[i])
        objs = new_objs
        #print(objs) # wyświetla aktualne wartości obiektów


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
    print("Connect this device to your account in your browser and run the program again.")
    exit()


# pobranie listy stron
r = requests.post('http://127.0.0.1:8000/api/page_list/', {'device_id': device_id})
if r.status_code != 200:
    print("Error %d: " % r.status_code + r.text)
    exit()
pages = [Page(int(d['id']), d['url'], d['paths'], int(d['interval']), d['login_url'], d['login_data']) for d in json.loads(r.text)]


# wątki do obserwowania stron
for page in pages:
    page.thread = threading.Thread(target=worker, args=(page,))
    page.thread.start()

