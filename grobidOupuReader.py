import os
import re
from typing import List, Dict
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class GrobidOutputReader:
    """
    A class to extract information from Grobid's XML output files.

    Attributes:
    -----------
    None

    Methods:
    --------
    xml_to_text(xml_file: str) -> str
        Given the path to an XML file, returns a plain text string containing the
        extracted information.

    xml_to_json(xml_file: str) -> Dict
        Given the path to an XML file, returns a dictionary containing the extracted
        information in JSON format.
    """

    def __init__(self):
        pass

    def xml_to_text(self, xml_file: str) -> str:
        """
        Extracts information from an XML file and returns it in a plain text format.

        Parameters:
        -----------
        xml_file: str
            Path to the XML file.

        Returns:
        --------
        str
            A plain text string containing the extracted information.
        """

        with open(xml_file) as f:
            text = f.read()

        soup = BeautifulSoup(text, 'lxml-xml')

        # initialize final_text
        final_text = ""

        # input the file name as the first line
        final_text += 'file_name: ' + xml_file
        final_text += '\n'

        # if there idno tag with type="DOI" add it to the final_text
        try:
            idno_list = soup.find_all('idno')
            for idno in idno_list:
                if idno['type'] == 'DOI':
                    final_text += 'DOI: ' + idno.text
                    final_text += '\n'
        except:
            pass

        # if there is a title, add it to the final_text
        if soup.title:
            final_text += 'Title: ' + soup.title.text
            final_text += '\n'

        # if there is an abstract, add it to the final_text
        try:
            if soup.abstract:
                final_text += 'Abstract: \n'
                abstract_s = soup.abstract.find_all('s')
                for s in abstract_s:
                    final_text += s.text + " "
                final_text += '\n'
        except:
            pass

        # find all divs
        all_div = soup.body.find_all('div')

        # loop through all divs
        for d in all_div:
            # if there is a headline, add it to the final_text
            if d.headline:
                final_text += d.headline.text
                final_text += '\n'

            # if there is a p tag, add it to the final_text
            if d.p:
                final_text += d.p.text
                final_text += '\n'

        return final_text

    def xml_to_json(self, xml_file: str) -> Dict:
        """
        Extracts information from an XML file and returns it in a dictionary in JSON format.

        Parameters:
        -----------
        xml_file: str
            Path to the XML file.

        Returns:
        --------
        Dict
            A dictionary containing the extracted information in JSON format.
        """

        with open(xml_file) as f:
            text = f.read()

        soup = BeautifulSoup(text, 'lxml-xml')
        json = {}
        json['file_name'] = xml_file
        try:
            idno_list = soup.find_all('idno')
            for idno in idno_list:
                if idno['type'] == 'DOI':
                    json
