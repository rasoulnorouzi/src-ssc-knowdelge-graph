import numpy as np
import pandas as pd
import re
from bs4 import BeautifulSoup as bs
import os

class GrobidOutputReader:
    def __init__(self):
        pass

    def xmlTOtext(self, xml_file):
        with open(xml_file) as f:
            text = f.read()

        soup = bs(text, 'lxml-xml')

        final_text = ""
        final_text += 'file_name: ' + xml_file + '\n'

        try:
            idno_list = soup.find_all('idno')
            for idno in idno_list:
                if idno['type'] == 'DOI':
                    final_text += 'DOI: ' + idno.text + '\n'
        except:
            pass

        if soup.title:
            final_text += 'Title: ' + soup.title.text + '\n'

        try:
            if soup.abstract:
                final_text += 'Abstract: \n'
                abstract_s = soup.abstract.find_all('s')
                for s in abstract_s:
                    final_text += s.text + " "
                final_text += '\n'
        except:
            pass

        all_div = soup.body.find_all('div')

        for d in all_div:
            if d.headline:
                final_text += d.headline.text + '\n'

            if d.p:
                final_text += d.p.text + '\n'

        return final_text

    def xmlToJSON(self, xml_file):
        with open(xml_file) as f:
            text = f.read()

        soup = bs(text, 'lxml-xml')
        json = {}
        json['file_name'] = xml_file

        try:
            idno_list = soup.find_all('idno')
            for idno in idno_list:
                if idno['type'] == 'DOI':
                    json['DOI'] = idno.text
        except:
            pass

        if soup.title:
            json['Title'] = soup.title.text

        try:
            if soup.abstract:
                abstract_s = soup.abstract.find_all('s')
                abstract = ""
                for s in abstract_s:
                    abstract += s.text + " "
                json['Abstract'] = abstract
        except:
            pass

        all_div = soup.body.find_all('div')
        sections = []

        for d in all_div:
            if d.headline:
                section = {}
                section['headline'] = d.headline.text
                section['text'] = d.p.text
                sections.append(section)

        json['sections'] = sections
        return json
