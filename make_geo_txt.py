#! /usr/bin/python3
"""
yah
"""

import sys, os
import csv
import re
import argparse
import string
    
def make_geo_txt(infile, colrange, lonc, latc, proj):
    """
    make a list of photo locations so that ODM
    can process them efficiently.
    """
    latcol = col2num(latc)
    loncol = col2num(lonc)
    sites = list(csv.reader(open(infile)))[1:]
    cols = parse_range(colrange)
    outfile = os.path.join(os.path.dirname(infile), 'geo.txt')
    with (open(outfile, 'w')) as csvfile:
        w = csv.writer(csvfile, delimiter = ' ')
        w.writerow([proj])
        for site in sites:
            for col in cols:
                w.writerow([site[col-1],
                            site[int(loncol) - 1],
                            site[int(latcol) - 1]])

def col2num(col):
    """Excel column letters to 1-based column number"""
    if col.isdigit():
        return col
    else:
        colnum = 0
        for c in col:
            if c in string.ascii_letters:
                colnum = colnum * 26 + (ord(c.upper()) -
                                        ord('A')) + 1
        return colnum

def parse_range(instring):
    """
    Takes a string like '3-5, 13, 36-38'
    or 'c-e, m, aj-al' (spreadsheet column names)
    and returns a list of index integers like 
    [3,4,5,13,36,37,38]
    """
    rng = re.sub(r'\s+', '', instring.strip())
    parts = [s.split('-') for s in rng.split(',')]
    numparts = [[col2num(x) for x in i] for i in parts]
    l = ([range(int(i[0]), int(i[1]) + 1)
         if len(i) == 2
         else i[0] for i in numparts])
    
    return [int(item) for sublist in l for item in sublist]
        

if __name__ == "__main__":
    """

    """
    p = argparse.ArgumentParser(description =
                                ('Georeference attachments '
                                 'from ODK submissions using '
                                 'lat and lon columns.'))
    p.add_argument('inputfile', help = 'Input CSV file')
    p.add_argument('-r', '--range', required=True,
                   help = ('columns with attachments to be '
                           'georeferenced. Use format '
                           '"3-5,7,9-11" or "c-e,g,i-k" '
                           '(spreadsheet format). Use 1-based '
                           'column numbers'))
    p.add_argument('-lat', '--latitude',
                   help = ('Latitude column. Can be 1-based '
                           'column number or spreadsheet '
                           'column letters'))
    p.add_argument('-lon', '--longitude',
                   help = ('longitude column '
                           'can be 1-based column number or '
                           'spreadsheet column letters'))
    p.add_argument('-proj', '--projection',
                   help = 'Coordinate Reference System',
                   default = 'EPSG:4326')
    args = p.parse_args()

    make_geo_txt(args.inputfile, args.range,
                 args.longitude, args.latitude,
                 args.projection)
