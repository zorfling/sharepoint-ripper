#!/usr/bin/python

# Mechanize
import mechanize
import html2text
import codecs
import re
import yaml
import os
from ntlm import HTTPNtlmAuthHandler
from bs4 import BeautifulSoup

def parse_page(config, url, output):
    global handled

    user = config['username']
    password = config['password']
    scrape_recursively = config['scrape_recursively']
    content_div_id = config['content_div_id']
    sharepoint_url = config['sharepoint_url']
    wiki_base_url = config['wiki_base_url']
    wiki_index = config['wiki_index']
    confluence_space_key = config['confluence_space_key']

    passman = mechanize.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, user, password)
# create the NTLM authentication handler
    auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

# create and install the opener
    browser = mechanize.Browser()
    browser.add_handler(auth_NTLM)

# Ignore robots.txt
    browser.set_handle_robots(False)
# retrieve the result
    response = browser.open(url)
    handled.append(url)

    soup = BeautifulSoup(response.read(), "html5lib")
    innerDiv = soup.find_all("div", id=content_div_id)

    if len(innerDiv) > 0:
# iterate over all relative links and update links
        links = innerDiv[0].find_all("a", href=re.compile("^\/"))
        for link in links:
# scrape link
            if scrape_recursively and wiki_base_url in link['href']:
                newoutput = link['href'].replace(wiki_base_url, "").replace("%20", "+").replace(".aspx", "")
                fullLink = sharepoint_url + link['href']
                if fullLink not in handled:
                    print fullLink
                    parse_page(config, fullLink, newoutput + ".md")

# fix links to point to Confluence-esque links
# remove Sharepoint url
                    link['href'] = link['href'].replace(wiki_base_url, ("/display/" + confluence_space_key + "/"));
# pluses rather than %20s
                    link['href'] = link['href'].replace("%20", "+");
# remove aspx
                    link['href'] = link['href'].replace(".aspx", "");

# add Sharepoint url to any remaining sharepoint links
            else:
                link['href'] = sharepoint_url + link['href'];

# convert to markdown and write
        content = str(innerDiv[0]).decode('utf-8').replace(u"\u200b", "")
        h = html2text.HTML2Text()
        h.body_width = 0
        markdown = h.handle(content)

        file = codecs.open("output/" + output, 'w', 'utf-8');
        file.write(markdown);
        file.close()

    else:
        if response.read() != '':
            print 'Failed'
        else:
            print 'Empty'
    return


config = yaml.load(file("config.yml"))
url = config['sharepoint_url'] + config['wiki_base_url'] + config['wiki_index']

# parse the index page
d = os.path.dirname('output/')
if not os.path.exists(d):
    os.makedirs(d)

handled = []
parse_page(config, url, 'index.md')
