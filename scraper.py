import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def search_station():
    search = input("Station Name: ")
    query = station_list

    while len(query) != 1 :
        buff = []
        for i in query:
            if search.upper() in i.upper(): 
                buff.append(i)
        if len(buff) == 0:
            search = input("No results found. Try again.\n")
            continue
        query = []
        query = buff.copy()
        if len(query) > 1:
            print(query)
            search = input("Choose one of the options.\n")
            
    return query[0]

station_list = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://cafcp.org/stationmap")

    page.locator("#popup-message-close").click()

    page.locator("#trigger-list").click()

    station_nodes = page.query_selector_all('.views-field-title')
    for s in station_nodes:
        element = s.query_selector('span > a')
        station_list.append(element.inner_text())

    station = search_station()
    print(station)

    page.locator('a:has-text("'+ station +'")').click(timeout=5000)


    try:
        while True:
            status = page.locator('tr:has-text("H70 Status")').inner_text(timeout=1000).split('\t')
            if len(status[1]) >= 1:
                break

        status = page.locator('tr:has-text("H70 Status")').inner_text(timeout=1000).split('\t')
        inv = page.locator('tr:has-text("H70 Inventory")').inner_text(timeout=1000).split('\t')
        print("H70 Status: " + status[1].strip())
        print("H70 Inventory: " + inv[1].strip())
    except:
        station_type = page.locator('tr:has-text("Station Type")').inner_text().split('\t')
        expected_open = page.locator('tr:has-text("Expected to Open")').inner_text().split('\t')
        print("Status: " + station_type[1])
        print("Expected to Open: " + expected_open[1])

    

    browser.close()