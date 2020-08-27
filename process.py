#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Let's assume that you combined the code from the previous 2 exercises with code
from the lesson on how to build requests, and downloaded all the data locally.
The files are in a directory "data", named after the carrier and airport:
"{}-{}.html".format(carrier, airport), for example "FL-ATL.html".

The table with flight info has a table class="dataTDRight". Your task is to
use 'process_file()' to extract the flight data from that table as a list of
dictionaries, each dictionary containing relevant data from the file and table
row. This is an example of the data structure you should return:

data = [{"courier": "FL",
         "airport": "ATL",
         "year": 2012,
         "month": 12,
         "flights": {"domestic": 100,
                     "international": 100}
        },
         {"courier": "..."}
]

Note - year, month, and the flight data should be integers.
You should skip the rows that contain the TOTAL data for a year.

There are couple of helper functions to deal with the data files.
Please do not change them for grading purposes.
All your changes should be in the 'process_file()' function.

The 'data/FL-ATL.html' file in the tab above is only a part of the full data,
covering data through 2003. The test() code will be run on the full table, but
the given file should provide an example of what you will get.
"""
from bs4 import BeautifulSoup
from zipfile import ZipFile
import os

def getinfo(tr, info):
    # get td_list 
    td_list = []
    for td in tr.find_all("td"):
        td_list.append(td.text)

    # and make info dictionary
    info["year"] = int(td_list[0])
    info["month"] = int(td_list[1])
                            
    dict_flights = {}
    dict_flights["domestic"] = int(td_list[2].replace(',', ''))
    dict_flights["international"] = int(td_list[3].replace(',', ''))
    info["flights"] = dict_flights

    return info

def addData(data, info):
    print("Adding info : ", info)
    data.append(info)
    return data

def process_file(f):
    """
    This function extracts data from the file given as the function argument in
    a list of dictionaries. This is example of the data structure you should
    return:

    data = [{"courier": "FL",
             "airport": "ATL",
             "year": 2012,
             "month": 12,
             "flights": {"domestic": 100,
                         "international": 100}
            },
            {"courier": "..."}
    ]


    Note - year, month, and the flight data should be integers.
    You should skip the rows that contain the TOTAL data for a year.
    """
    
    
    
    # Note: create a new dictionary for each entry in the output data list.
    # If you use the info dictionary defined here each element in the list 
    # will be a reference to the same info dictionary.
    with open(f, "r") as html:
        soup = BeautifulSoup(html)
        table = soup.find(id = "DataGrid1")

        data = []

        for tr in table.find_all("tr"):
            #print(tr)
            info = {}
            info["courier"], info["airport"] = f[:6].split("-")

            class_tr = ""
            if(tr.has_attr("class")):
                class_tr = tr["class"][0]
                print("class_tr : ", class_tr)

            style = ""
            if (tr.has_attr("style")):
                style = tr["style"]
                print("Style : ", style)

            check = False

            if ((class_tr == "dataTDRight") and (style == "")):
                check = True
                print("Inside first if : check : ", check)

            elif ((class_tr == "dataTDRight") and (style != "background-color:LightYellow;")):
                check = True
                print("Inside second if : check : ", check)

            else:
                print("check : ", check)
                #info = {}

            
            if (check == True):
                print("Data before append: ", data)
                
                info = getinfo(tr, info)
                print("info : ", info)
                
                data = addData(data, info)
                print("Data after append: ", data,"\n\n")
            else:
                print("No Data to add\n\n")
            

    #print(data)        
    return data


def test():
    data = process_file("FL-ATL.html")
    
        
    #assert len(data) == 399  # Total number of rows
    
    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2
    assert data[0]["courier"] == 'FL'
    print("data[0] : ", data[0])
    print("data[0][month] : ", data[0]["month"])
    assert data[0]["month"] == 10
    assert data[-1]["airport"] == "ATL"
    assert data[-1]["flights"] == {'international': 108289, 'domestic': 701425}
    
    print("... success!")
    
if __name__ == "__main__":
    test()