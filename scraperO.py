import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
from selenium.webdriver.chrome.options import Options
import re
from convertdate import cd
from telegramsend import send



def getmatchdaylist(n):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)

    # link do ligi
    driver.get("http://www.90minut.pl/liga/1/liga13060.html")
    time.sleep(0.5)
    e = driver.find_elements(By.XPATH, value="/html/body/table[2]/tbody/tr[1]/td[3]/p[%d]/table" % n)
    m = ""
    for t in e:
        # print(t.text)
        m += t.text

    l = m.splitlines()
    pattern = r"-"
    matcheslist = ""
    for x in l:
        if re.search(pattern, x) and len(x) > 15:
            matcheslist += x + "\n"
    return matcheslist


def checkscore(text):
    pattern = r'\d+-\d+'
    if re.search(pattern, text):
        return True
    else:
        return False


def deletedaymonth(text):
    pattern = r'\d+\s\w+,\s'
    out = re.sub(pattern, '', text)
    return out


def todaymatches():
    # numer tygodnia przypisany do numeru kolejki w html
    # po zmianie ligii trzeba bedzie sprawdzic i pozmieniac

    weekandmatchday = {
        44: 30,
        45: 32,
        46: 34
    }

    today = datetime.datetime.now()
    week = today.isocalendar()[1]
    n = weekandmatchday[week]
    ml = getmatchdaylist(n)
    todaymatcheslist = ""
    t = datetime.datetime.now()

    #///////////////////////////////////////////////////////////
    #t = t + datetime.timedelta(days=1)
    # ///////////////////////////////////////////////////////////

    today = t.date()
    matches = ml.splitlines()
    pattern = r'(\d{1,2}\s\w+,\s\d{1,2}:\d{2})'

    for x in matches:
        #print(x)
        m = re.findall(pattern, x)
        for k in m:

            p = cd(k)
            pd = p.date()

            if today == pd:
                todaymatcheslist += x + "\n"

    todaymatcheslist = todaymatcheslist.rstrip()
    todaymatcheslist = deletedaymonth(todaymatcheslist)

    return todaymatcheslist


def mainfun():
    tm = todaymatches()
    if not tm:
        asyncio.run(send("Witam. Dzisiaj żadne mecze nie są rozgrywane w klasie okręgowej Rzeszów"))
        return

    # informacja o dzisiejszych meczach
    mdaymessage = "Dzisiejsze mecze w klasie okręgowej Rzeszów:: \n" + tm
    asyncio.run(send(mdaymessage))

    # wyszukaj najwczesniejsza godzine meczu i uspij program
    g = []
    pattern = r'\d{2}:\d{2}'
    tmlines = tm.splitlines()
    for a in tmlines:
        m = re.findall(pattern, a)
        g.extend(m)

    start = min(g)
    start = datetime.datetime.strptime(start, "%H:%M")
    start = start + datetime.timedelta(minutes=0)
    start = start.strftime("%H:%M")
    tnow = datetime.datetime.now()
    h, m = map(int, start.split(":"))
    startformat = tnow.replace(hour=h, minute=m, second=0, microsecond=0)
    diff = startformat - tnow
    s = diff.total_seconds()
    if s > 0:
        print("Usypiam program na", int(s), "sekund, do godziny:", start)
        time.sleep(s)

    # tablica indeksow meczow bez wyniku
    withoutresult = []
    for b in range(len(tmlines)):
        if not checkscore(tmlines[b]):
            withoutresult.append(b)

    # podczas gdy nie wszystkie wyniki zostaly podane wykonuj program
    while withoutresult:
        tm = todaymatches()
        tmlines = tm.splitlines()

        for x in withoutresult:
            if checkscore(tmlines[x]):
                print(tmlines[x])
                asyncio.run(send(tmlines[x]))
                withoutresult.remove(x)
        time.sleep(120)
        t = datetime.datetime.now()

        if t.hour >= 23 or t.hour < 0:
            return

    return

mainfun()