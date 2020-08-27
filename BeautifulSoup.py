#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the appropriate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
from bs4 import BeautifulSoup
import requests
import json

#html_page = "page_source.html"
html_page = "options.html"


def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        event_value = soup.find(id="__EVENTVALIDATION")
        view_value = soup.find(id="__VIEWSTATE")

        data["eventvalidation"] = event_value["value"]
        data["viewstate"] = view_value["value"]

    return data

"""
Your task in this exercise is to modify 'extract_carrier()` to get a list of
all airlines. Exclude all of the combination values like "All U.S. Carriers"
from the data that you return. You should return a list of codes for the
carriers.

All your changes should be in the 'extract_carrier()' function. The
'options.html' file in the tab above is a stripped down version of what is
actually on the website, but should provide an example of what you should get
from the full file.

Please note that the function 'make_request()' is provided for your reference
only. You will not be able to to actually use it from within the Udacity web UI.
"""
def extract_carriers(page):
    data = []
    exclude_values = ["All", "AllUS", "AllForeign"]

    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        carrier = soup.find(id="CarrierList")
        c_list = carrier.find_all("option")
        for option in c_list:
          option_value = option["value"]
          if(option_value not in exclude_values):
            data.append(option_value)

    return data

"""
Complete the 'extract_airports()' function so that it returns a list of airport
codes, excluding any combinations like "All".

Refer to the 'options.html' file in the tab above for a stripped down version
of what is actually on the website. The test() assertions are based on the
given file.
"""

def extract_airports(page):
    data = []
    exclude_values = ["All", "AllMajors", "AllOthers"]

    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        airport = soup.find(id = "AirportList")
        airport_list = airport.find_all("option")
        for a in airport_list:
          airport_value = a["value"]
          if (airport_value not in exclude_values):
            data.append(airport_value)
        
    for index, value in enumerate(data):
      print(index, value)
  
    return data

def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]
    airport = data["airport"]
    carrier = data["carrier"]

    r = s.post("https://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
               data = (("__EVENTTARGET", ""),
                       ("__EVENTARGUMENT", ""),
                       ("__VIEWSTATE", viewstate),
                       ("__VIEWSTATEGENERATOR",viewstategenerator),
                       ("__EVENTVALIDATION", eventvalidation),
                       ("CarrierList", carrier),
                       ("AirportList", airport),
                       ("Submit", "Submit")))

    return r.text


def test():
    '''
    data = extract_data("page_source.html")
    assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")
    '''
    '''
    data = extract_carriers(html_page)
    assert len(data) == 16
    assert "FL" in data
    assert "NK" in data
    '''
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

if __name__ == "__main__":
    test()