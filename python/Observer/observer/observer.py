import random, string, json
import socket, os, time, threading
import requests, AdvancedHTMLParser
import sys
import subprocess
import time


def open_file(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def parse(html):
    parser = AdvancedHTMLParser.IndexedAdvancedHTMLParser()
    parser.parseStr(html)
    return parser


server_address = 'http://127.0.0.1:8000'


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
            r = self.session.get(self.login_url['get'])
            parser = parse(r.text)
            data = self.login_data.copy()
            for input in parser.getElementsByTagName('input'):
                if input.getAttribute('type') == 'hidden':
                    data[input.getAttribute('name')] = input.getAttribute('value')
            r = self.session.post(self.login_url['post'], data)

    # zwraca listę obserwowanych obiektów
    def get_objects(self):
        r = self.session.get(self.url)
        parser = parse(r.text)
        #self.title = parser.getElementsByTagName('title')[0].innerHTML
        doc = parser.getRoot()
        objs = []
        for obj_path in self.paths:
            e = doc
            # jeśli na początku ścieżki jest id, zaczynamy od elementu z tym id
            if isinstance(obj_path[0], str):
                e = doc.getElementById(obj_path[0])
            # pomijamy dodawany przez parser drugi znacznik html
            if e.tagName == 'html' and e.getChildren()[0].tagName == 'html':
                e = e.getChildren()[0]
            prev_tag = e.tagName
            for index in obj_path:
                if isinstance(index, int):
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
        r = requests.post(server_address + '/api/new_change/', {'device_id': device_id, 'page_id': self.id, 'old_value': old_value, 'new_value': new_value})
        if r.status_code != 200:
            print("Error %d: " % r.status_code + r.text)
            exit()


kill_em_all = False
event = threading.Event()


def worker(page):
    page.login()
    objs = page.get_objects()
    working = True
    while working and not kill_em_all:
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
        # print(objs)
        # page.notify("TEST", new_objs[0])
        event.wait(page.interval)


pages = []


def start_threads():
    # pobranie listy stron
    r = requests.post(server_address + '/api/page_list/', {'device_id': device_id})
    if r.status_code != 200:
        print("Error %d: " % r.status_code + r.text)
        exit()
    global pages
    pages = [Page(int(d['id']), d['url'], d['paths'], int(d['interval']), d['login_url'], d['login_data']) for d in json.loads(r.text)]

    # wątki do obserwowania stron
    for page in pages:
        page.thread = threading.Thread(target=worker, args=(page,))
        page.thread.start()


def stop_threads():
    global kill_em_all
    kill_em_all = True
    global event
    event.set()
    for page in pages:
        page.thread.join()
    kill_em_all = False
    event.clear()


def restart_threads():
    stop_threads()
    start_threads()

# id urządzenia
try:
    f = open('device_id', 'r')
    device_id = f.read()
except FileNotFoundError:
    device_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    with open('device_id', 'w') as f:
        f.write(device_id)
    open_file(server_address + '/add_device?device_id=' + device_id + '&device_name=' + socket.gethostname())
    print("Connect this device to your account in your browser and run the program again.")
    exit()

# atrapa

r = requests.post(server_address + '/api/what/', {'device_id': device_id, 'msg': 'hi'})
if r.status_code != 200:
    print("Error %d: " % r.status_code + r.text)
    exit()

try:
    while True:
        r = requests.post(server_address + '/api/what/', {'device_id': device_id, 'msg': 'what'})
        if r.status_code != 200:
            print("Error %d: " % r.status_code + r.text)
            exit()
        msg = r.json()['that']

        # TODO: nie zatrzymywać wątków przed ich rozpoczęciem
        # (możemy wysłać 'hi' a potem od razu otrzymać 'stop' jeżeli np. w tym samym czasie do serwera zgłosi się inna odświeżaczka z wyższym priorytetem)

        action = ''
        if msg == 'nope':
            action = 'bad boy'
        elif msg == 'wait':
            action = 'wait'
        elif msg == 'start':
            action = 'start'
            start_threads()
        elif msg == 'stop':
            action = 'stop'
            stop_threads()
            r = requests.post(server_address + '/api/what/', {'device_id': device_id, 'msg': 'stopped'})
            if r.status_code != 200:
                print("Error %d: " % r.status_code + r.text)
                exit()
        elif msg == 'update':
            action = 'update'
            restart_threads()

        print('action: ' + action)
        time.sleep(4)

except KeyboardInterrupt:
    stop_threads()
    r = requests.post(server_address + '/api/what/', {'device_id': device_id, 'msg': 'bye'})
    if r.status_code != 200:
        print("Error %d: " % r.status_code + r.text)
    exit()
