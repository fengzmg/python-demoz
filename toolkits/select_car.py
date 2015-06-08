import requests
import re
import datetime
import threading
import multiprocessing
import time
import random

headers = {
    'Referer': 'http://en.wikipedia.org/wiki/Main_Page',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0',
    'X-Requested-With': 'Browser'
}

proxies = {
    'http': None
}

search_url = 'http://www.sgcarmart.com/used_cars/listing.php?RPG=%(page_size)s&MOD=Car+Make+%%2F+Model&ASL=1&PR1=0&PR2=&FR=%(from)s&TO=%(to)s&TRN=&ENG=%(engine_cap)s&VTS[]=2&VTS[]=13&VTS[]=12&VTS[]=11&VTS[]=10&VTS[]=9&VTS[]=8&VTS[]=7&VTS[]=6&VTS[]=3&FUE=&MIL_C=&OMV_C=&COE_C=&OWN_C=&OPC[]=0&DL=&LOC=&AVL=2' % \
             {
                'from': '2006',
                'to': '2007',
                'engine_cap': '4', # 2 for 2001 cc- 3000 cc, 5 for < 661cc, 4 for <1600cc
                'page_size': '100'
              }

config = {
    'async_enabled': False,
    'timeout': 30
}

class Car(object):
    def __init__(self):
        self.price = 0
        self.road_tax = 0
        self.transmission = ''
        self.engine_cap = ''
        self.power = ''
        self.reg_date = None
        self.omv = 0
        self.no_of_owners = 0
        self.detail_link = ''
        self.car_type = ''
        self.depreciation_by_year = 999999

    def calc_depreciation(self):
        delta = (self.reg_date + datetime.timedelta(days=365*10)) - datetime.datetime.now()
        self.depreciation_by_year = ((self.price - self.omv*0.5)/delta.days) * 365

    def __repr__(self):
        return "===============================================================\n" + \
                "Car:           %s\n" % self.car_type + \
                "Price:         %d\n" % self.price + \
                "OMV:           %d\n" % self.omv + \
                "REG Date:      %s\n" % self.reg_date + \
                "Eng Cap:       %s\n" % self.engine_cap + \
                "Transmission:  %s\n" % self.transmission + \
                "Road Tax:      %d\n" % self.road_tax + \
                "No of Owners:  %d\n" % self.no_of_owners + \
                "Depreciation:  %s\n" % self.depreciation_by_year + \
                "Detail:        %s\n" % self.detail_link + \
                "==============================================================="

class SgCarMartCarDetailParser:
    def __init__(self):
        pass
    def parseResponseToCar(self, link, html):
        car = Car()
        car.detail_link = link

        match = re.search(r'<a href="info\.php\?ID=\d+&DL=\d+">(.*)</a>', html)
        if match:
            car.car_type = match.group(1)

        match = re.search(r'<td class="label"><strong>Price</strong></td><td colspan="2"><a href="info_financial\.php\?ID=\d+" style="color:#000"><strong>\$(.*)</strong></a></td></tr>', html)
        if match:
            car.price = int(match.group(1).replace(',',''))

        match = re.search(r'<td class="label"><strong>OMV</strong></td>\n.*<td>\$(.*)</td>', html)
        if match:
            car.omv = int(match.group(1).replace(',',''))

        match = re.search(r'<td class="label"><strong>Reg Date</strong></td>\n.*<td>(\d{2}-.{3}-\d{4})</td>', html)
        if match:
            car.reg_date = datetime.datetime.strptime(match.group(1), '%d-%b-%Y')

        match = re.search(r'<td class="label"><strong>No. of Owners</strong></td>\n.*<td>(\d+)</td>', html)
        if match:
            car.no_of_owners = int(match.group(1).replace(',',''))

        match = re.search(r'<td class="label"><strong>Road Tax</strong></td>\n.*<td>\$(\d+).*</td>', html)
        if match:
            car.road_tax = int(match.group(1).replace(',',''))

        match = re.search(r'<td class="label"><strong>Engine Cap</strong></td>\n.*<td>(.* cc)</td>', html)
        if match:
            car.engine_cap = match.group(1)

        match = re.search(r'<td class="label"><strong>Transmission</strong></td>\n.*<td>(.*)</td>', html)
        if match:
            car.transmission = match.group(1)

        car.calc_depreciation()
        return car

class SgCarMartCarListParser:
    def __init__(self):
        pass
    
    def parseReponseToCarList(self, html):
        links = re.findall(r'href="(info\.php\?ID=\d+&DL=\d+)"',html)
        return ['http://www.sgcarmart.com/used_cars/' + link for link in list(set(links))]

    def retrieve_next_link_page(self, html):
        next_link = None
        match = re.search(r'<span class=.pagebar.>\)</span>.*<a href="(/used_cars/listing\.php\?.*)" class=.*>Next <span>', html)
        if match:
            next_link =  'http://www.sgcarmart.com' + match.group(1)
        return next_link


class CarListExtractionThread(threading.Thread):
    def __init__(self, link_to_extract, parser, details_links=[], link_pages=[]):
        threading.Thread.__init__(self)
        self.link_to_extract = link_to_extract
        self.parser = parser
        self.details_links = details_links
        self.name = 'Thread-' + link_to_extract
        self.link_pages = link_pages
        self.link_pages.append(link_to_extract) if not link_to_extract in self.link_pages else None

    def run(self):
        print 'retrieving car list from %s\n' % self.link_to_extract
        res = requests.get(self.link_to_extract, proxies=proxies, headers=headers, timeout=config.get('timeout'))
        links = self.parser.parseReponseToCarList(res.text)
        self.details_links.extend(links)

        threads = []

        next_link_page = self.parser.retrieve_next_link_page(res.text)

        if next_link_page is not None:
            print 'retrieved next page: ' + next_link_page     
            if not next_link_page in self.link_pages:
                print 'spawning new thread for next page:' + next_link_page
                new_thread = CarListExtractionThread(next_link_page, self.parser, self.details_links, self.link_pages)
                new_thread.start()
                threads.append(new_thread)
            
        for thread in threads:
            thread.join()


class CarDetailsExtractionThread(threading.Thread):
    def __init__(self, link_to_extract, parser, cars=[]):
        threading.Thread.__init__(self)
        self.link_to_extract = link_to_extract
        self.parser = parser
        self.cars = cars
        self.name = 'Thread-' + link_to_extract

    def run(self):
        print 'retrieving car info from %s\n' % self.link_to_extract
        try:
            detail_res = requests.get(self.link_to_extract, proxies=proxies, headers=headers, timeout=config.get('timeout'))
            car = self.parser.parseResponseToCar(self.link_to_extract, detail_res.text)
            self.cars.append(car) if car.price > 3000 else None
        except Exception as e:
            print e

    def __call__(self, *args, **kwargs):
        self.run()

def list_cars():
    details_links = []
    CarListExtractionThread(search_url, SgCarMartCarListParser(), details_links).run()
    print 'detected %d cars...' % len(details_links)
    cars = []
    threads = []
    

    for detail_link in  list(set(details_links)):
        t = CarDetailsExtractionThread(detail_link, SgCarMartCarDetailParser(), cars)
        time.sleep(random.randint(0,30)/100.0)
        t.start()
        threads.append(t)
    #thread_pool = multiprocessing.Pool(processes=50)
    #[thread_pool.apply(t) for t in threads]
    #thread_pool.close()
    #thread_pool.join() # must call close() before calling join
    for thread in threads:
        thread.join()

    cars.sort(key=lambda car: car.depreciation_by_year)

    print 'retrieved %d cars' % len(cars)   
    print 'top 100 value for money:'

    for car in cars[:100]:
        print car

if __name__ == '__main__':
    list_cars()

