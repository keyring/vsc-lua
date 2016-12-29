#!/usr/bin/python3
# -*- coding:utf-8 -*-

import urllib.request
import bs4
import json
import io


out_json_file = io.open('snippets.json', 'w')
in_json_file = io.open('../snippets/snippets.json', 'r')

url1 = 'http://www.lua.org/manual/5.1/manual.html'
url2 = 'http://www.lua.org/manual/5.2/manual.html'
url3 = 'http://www.lua.org/manual/5.3/manual.html'

soup51 = bs4.BeautifulSoup(urllib.request.urlopen(url1).read(), "html.parser")
soup52 = bs4.BeautifulSoup(urllib.request.urlopen(url2).read(), "html.parser")
soup53 = bs4.BeautifulSoup(urllib.request.urlopen(url3).read(), "html.parser")

snippets51 = {}
snippets52 = {}
snippets53 = {}

soups = [
    { 'soup':soup51, 'snippet':snippets51, 'ver':'5.1' },
    { 'soup':soup52, 'snippet':snippets52, 'ver':'5.2' },
    { 'soup':soup53, 'snippet':snippets53, 'ver':'5.3' }
]

def snippets(soup, snippet, ver):
    stand = soup.find_all("h3")
    for s in stand:
        string = s.string
        if string != None:
            string = string.replace('\u00b7', ".")            
            splitstrs = string.split(' ', 1)
            name = splitstrs[0]
            if name.find('luaL_')>-1 or name.find('lua_') >-1:
                continue
            snippet[name] = {}
            snippet[name]['ver'] = ver
            snippet[name]['prefix'] = name
            snippet[name]['body'] = name + '(${0:...})'
            snippet[name]['description'] = string
            snippet[name]['scope'] = 'source.lua'

for v in soups:
    snippets(v['soup'], v['snippet'], v['ver'])

snippets5 = {}

for s in snippets51:
    if s not in snippets5:
        snippets5[s] = snippets51[s]
        snippets5[s]['ver'] = snippets51[s]['ver']

for s in snippets52:
    if s not in snippets5:
        snippets5[s] = snippets52[s]
        snippets5[s]['ver'] = snippets52[s]['ver']
    else:
        snippets5[s]['ver'] += ',' + snippets52[s]['ver']

for s in snippets53:
    if s not in snippets5:
        snippets5[s] = snippets53[s]
        snippets5[s]['ver'] = snippets53[s]['ver']
    else:
        snippets5[s]['ver'] += ',' + snippets53[s]['ver']


json_in_str = json.loads(in_json_file.read())

for s in snippets5:
    if s not in json_in_str:
        json_in_str[s] = snippets5[s]
        json_in_str[s]['description'] = snippets5[s]['ver']+'\n\n'+json_in_str[s]['description']
        del json_in_str[s]['ver']

json_str = json.dumps(json_in_str, indent=4, sort_keys=True)

out_json_file.write(json_str)
