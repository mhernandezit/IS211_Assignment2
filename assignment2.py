#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from urllib2 import Request, urlopen, URLError
import argparse
import datetime
import csv
import logging
import sys

def downloadData (url):
    req = Request(url)
    response = urlopen(req)
    return csv.reader(response)

def processData (fileData):
    personData = {}
    for i, row in enumerate(fileData):
        try:
            day,month,year = row[2].split('/')
            dateData = datetime.datetime(int(year),int(month),int(day))
        except ValueError:
            logger.error("Error processing line #" + str(i) + " for ID # " + row[0])
            continue
        personData[row[0]] = (row[1],dateData)
    return personData

def displayPerson(personData):
    """​ Print the name and birthday of a given user identified by the input id 
    Person # <id> is <name> with a birthday of <date>"""
    lookupid = 1
    while lookupid > 0:
        iterid = raw_input("Please enter user ID to lookup: ")
        try:
            lookupid = int(iterid)
        except ValueError:
            logger.error("Input must be a number")
            continue
        if iterid in personData:
            print("Person # {} is {} with a birthday of {}").format(iterid, personData[iterid][0], personData[iterid][1]) 
        elif lookupid <= 0:
            print("Exiting")
            break
        else:
            print("No such person")

def logBuilder():
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.DEBUG)
    try:
        fh = logging.FileHandler('errors.log')
    except IOError:
        print("Unable to open log file")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

if __name__ == '__main__':
    logger = logBuilder()
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help = 'URL to lookup', required=True)
    args = parser.parse_args()
    try:
        csvdata = downloadData(args.url)
    except URLError:
        logger.error("Unable to retrieve CSV file")
        print('Unable to retrieve CSV file')
        sys.exit()
    except HTTPError:
        logger.error("404 error")
        print('404, destination unreachable')
        sys.exit()
    processDict = processData(csvdata)
    displayPerson(processDict)