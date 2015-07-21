#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import urllib
import requests
import xml.dom.minidom

def executeQuery(sparql, outputFileName, delimiter, verbose):

    user_agent = {'User-Agent': 'Mozilla/5.0','Accept':'text/html,application/xml'}

    prefix='PREFIX : <http://www.semanticweb.org/ontologies/2015/1/EPNet-ONTOP_Ontology#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> PREFIX dcterms: <http://purl.org/dc/terms/>'
    query=urllib.quote(prefix+sparql)
    #r will store the XML answer of the query
    r=requests.get("http://136.243.8.213:8080/openrdf-sesame/repositories/epnet_pleiades_edh?query="+query,headers=user_agent)

    if verbose:
        print(r.content)

    allAmphoras=""
    try:
        allAmphoras=xml.dom.minidom.parseString(r.content)
    except:
        print('Error - answer is not a valid response: '+allAmphoras)
        return

    outputFile = open(outputFileName, 'w')
    # TODO write header

    i = 0
    for result in allAmphoras.getElementsByTagName('result'):
        newEntry = str(i)
        for literal in result.getElementsByTagName('literal'):
            newEntry += delimiter
            literalStr = literal.childNodes[0].data.encode('utf-8')
            newEntry += literalStr
        outputFile.write(newEntry+'\n')
        i += 1

def readQuery(queryFileName):
    with open (queryFileName, "r") as queryFile:
        query = queryFile.read().replace('\n', '')
        return query
    return ''


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-o", "--output", help="CSV file to store output", default="out.csv")
    parser.add_argument("-d", "--delimiter", help="delimiter between fields", default=";")
    parser.add_argument("-qf", "--queryFile", help="file with query")
    parser.add_argument("-q", "--query", help="direct query")
    parser.add_argument("-v", "--verbose", help="verbose actions", default=False)
    
    args = parser.parse_args()

    if not args.query and not args.queryFile:
        print('Error - no query asked')
        return -1

    query = ''
    if args.query:
        query = args.query
    elif args.queryFile:
        query = readQuery(args.queryFile)
    else:
        print('Error - conflicting options query and queryFile. Use only one of them')
        return -1

    executeQuery(query, args.output, args.delimiter, args.verbose)

if __name__ == "__main__":
    main()

