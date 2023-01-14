#!/usr/bin/python

# Copyright (C) 2013  Prof. Jayanth R. Varma, jrvarma@iimahd.ernet.in,
# Indian Institute of Management, Ahmedabad 380 015, INDIA

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program (see file COPYING); if not, write to the 
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, 
# Boston, MA  02111-1307  USA

import json
import datetime

# Read in the starred items from the json file 
# Note: This assumes that the starred.json is in the current directory
# Result is a list of items each of which is a dictionary with following keys:
# 'origin', 'updated', 'author', 'title', 'alternate', 'timestampUsec', 'comments', 
# 'summary', 'crawlTimeMsec', 'annotations', 'published', 'id', 'categories', 'canonical'
# Note: Each item is a nested dictionary: some of the values are themselves dictionaries!
with open('starred.json') as fp:
    items = json.load(fp)['items']

# Extract only the relevant fields from each entry while also
# flattening the nested dictionaries 
new_items = []
for item in items:
    new_item = {}
    if 'origin' in item.keys():
        if 'htmlUrl' in item['origin'].keys():
            new_item['feedUrl'] = item['origin']['htmlUrl'] 
        if 'title' in item['origin'].keys():
            new_item['feedTitle'] = item['origin']['title']
    new_item['url'] = item['alternate'][0]['href']
    new_item['title'] = item['title']
    new_item['time'] = item['updated']
    if 'content' in item.keys():
        new_item['content'] = item['content']['content']
    if 'summary' in item.keys():
        new_item['summary'] = item['summary']['content']
    new_items.append(new_item)

# Sort by time descending
new_items.sort(key=lambda k: k['time'], reverse=True) 

# Function to create html file from the new_items 
# filename is the name of the file to be created 
#    Caution: existing file is overwritten without warning
# output_content specifies whether content/summary field should be output. 
#    If False only the metadata (title, time, links) are output.
# Unicode characters are encoded into html numeric entities
#    using encode('ascii', errors='xmlcharrefreplace')
def make_html(filename, output_content):
    with open(filename, 'w') as f:
        print >> f, '<html><head><title>My starred items</title></head>' 
        print >> f, '<body><h1>My starred items</h1>\n'
        for item in new_items:
            if 'feedUrl' in item.keys():
                print >> f, '<h1><a href="' + item['feedUrl'] + '">'
            if 'feedTitle' in item.keys():
                print >> f, item['feedTitle'].encode('ascii', errors='xmlcharrefreplace')
            elif 'feedUrl' in item.keys():
                print >> f, item['feedUrl'].encode('ascii', errors='xmlcharrefreplace') + '</a>'
            print >> f, '</h1>'
            print >> f, '<h2><a href="' + item['url'] + '">'
            print >> f, item['title'].encode('ascii', errors='xmlcharrefreplace') + '</a></h2>'
            print >> f, '<p>'
            print >> f, datetime.datetime.fromtimestamp(item['time']).strftime('%Y-%m-%d %H:%M:%S')
            print >> f, '</p>\n'
            if output_content:
                if 'content' in item.keys():
                    print >> f, item['content'].encode('ascii', errors='xmlcharrefreplace')
                if 'summary' in item.keys():
                    print >> f, item['summary'].encode('ascii', errors='xmlcharrefreplace')
        print >> f, '\n</body></html>'

# Make html file with full content only
make_html('starred-content.html', True)
# Make html file without content (only summary)
make_html('starred-links.html', False)
