#!/bin/python3

# Copyright (c) 2022 Humanitarian OpenStreetMap Team
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     Odkconvert is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with Odkconvert.  If not, see <https:#www.gnu.org/licenses/>.
#

import logging
import epdb
import argparse
import sys, os
from datetime import tzinfo, datetime
import json
from OdkCentral import OdkCentral, OdkProject, OdkForm


class OdkClient(object):
    def __init__(self, url=None, user=None, passwd=None):
        """A Class for client side access to ODK Central"""
        self.url = url
        self.user = user
        self.passwd = passwd
        self.cache = dict()

    def readCache(self, cache=".odkcentral"):
        file = open(cache, "rb")
        data = file.readline()
        print(json.load(data))
        file.close()
        
    def writeCache(self, cache=".odkcentral", data=None):
        if args.cache:
            try:
                file = open(cache, "xb")
            except FileExistsError:
                file = open(cache, "wb")
            file.write("projects\n")
            file.write(json.dump(data))
            file.close()
        logging.info("Wrote config file %s" % filespec)
        
parser = argparse.ArgumentParser(description='command line client for ODK Central')
parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
parser.add_argument("-s", "--server", choices=['projects', 'users'],
                    help="project operations")
parser.add_argument("-p", "--project", choices=['forms', 'submissions', 'app-users'],
                    help="project operations")
parser.add_argument("-d", "--download", choices=['xml', 'xlsx', 'attach', 'submit', 'zip'],
                    help="Download files")
parser.add_argument("-up", "--upload", choices=['xml', 'xlsx', 'attach', 'submit', 'zip'],
                    help="Download files")
parser.add_argument('-u', '--user', help = 'ODK Central username (usually email)')
parser.add_argument('-pw', '--password', help = 'ODK Central password')
parser.add_argument('-i', '--id', type=int, help = 'Project ID nunmber')
parser.add_argument('-c', '--cache', action="store_true", help = 'cache data from ODK Central')

args = parser.parse_args()

# if verbose, dump to the terminal.
if args.verbose is not None:
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)    

# The ODK Central server
if args.server:
    central = OdkCentral()
    # central.authenticate()
    if args.server == "projects":
        projects = central.listProjects().json()
        print("There are %d projects on this ODK Central server" % len(projects))
        for project in projects:
            print("\t%s: %s" % (project['id'], project['name']))
    elif args.server == "users":
        users = central.listUsers()
        logging.info("There are %d users on this ODK Central server" % len(users.json()))
        for project in projects.json():
            print(project['id'], project['name'])

elif args.project:
    project = OdkProject()
    # form.authenticate()
    if args.project == "forms":
        forms = project.listForms(4).json()
        for form in forms:
            print("\t%r: %r" % (form['xmlFormId'], form['name']))
    if args.project == "submissions":
        submit = project.listSubmissions(4, "cemeteries").json()
        for entry in submit:
            print("\t%r" % entry)
    if args.project == "app-users":
        users = project.listAppUsers(4).json()
        for user in users:
            print("\t%r: %s" % (user['id'], user['displayName']))

# This downloads files from the ODK server
elif args.download:
    form = OdkForm()
    if args.download == "xml":
        pass
    elif args.download == "xls":
        pass
    elif args.download == "attach":
        pass
    elif args.download == "submit":
        pass
    elif args.download == "zip":
        pass

# This uploads files to the ODK server
elif args.upload:
    form = OdkForm()
    if args.upload == "xml":
        pass
    elif args.upload == "xls":
        pass
    elif args.upload == "attach":
        pass
    elif args.upload == "submit":
        pass
    elif args.upload == "zip":
        pass
