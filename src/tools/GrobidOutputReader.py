from bs4 import BeautifulSoup as bs

class GrobidOutputReader:

    """
        The output of Grobid is an xml file. This class reads the xml file and converts it to a plain text file.
        
        Initializes a GrobidOutputReader object with specified parser.
        :param parser: The name of the parser to use. Default is 'lxml-xml'.
        :type parser: str
        for more unformaton about parsers, see https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=parser#installing-a-parser
    
    """

    def __init__(self, parser = "lxml-xml"):
        self.parser = parser


    def XMLtoText(self, xml_file, divide_by_headline = True):
        """
            Reads the xml file and converts it to a plain text file.

            :param xml_file: The path to the xml file.
            :type xml_file: str
            :param divide_by_headline: If True, the text will be divided by headlines. Default is True.
            :type divide_by_headline: bool
            :return: The plain text file.
            :rtype: str
        """

        # read the xml file
        with open(xml_file) as f:
            text = f.read()

        soup = bs(text, self.parser)

        # initialize final_text
        final_text = ""
        # input the file name as the first line
        final_text += 'file_name: ' + xml_file
        final_text += '\n'

        # if there is a title, add it to the final_text
        if soup.title:
            final_text += 'Title: '+soup.title.text
            final_text += '\n'

        # there is a doi, add it to the final_text
        try:
            if soup.idno:
                final_text += 'DOI: '+soup.idno.text
                final_text += '\n'
        except:
            pass

        # if there is an abstract, add it to the final_text
        try :
            if soup.abstract:
                if divide_by_headline:
                    final_text += 'Abstract: \n'
                    
                abstract_s = soup.abstract.find_all('s')
                for s in abstract_s:
                    final_text += s.text+" "
                if divide_by_headline:
                    final_text += '\n'
                else:
                    final_text += ' '
        except:
            pass

        # find all divs
        all_div = soup.body.find_all('div')

        # loop through all divs
        for d in all_div:
            # if there is a headline, add it to the final_text
            if d.head:
                final_text += d.head.text
                if divide_by_headline:
                    final_text += '\n'
                else:
                    final_text += ' '
                d_s = d.find_all('s')

                for s in d_s:
                    final_text += s.text+" "

                if divide_by_headline:
                    final_text += '\n'
                else:
                    final_text += ' '
           
            # if there is no headline, add "No Headline" to the final_text
            else:
                final_text += 'No Headline'

                if divide_by_headline:
                    final_text += '\n'
                else:
                    final_text += ' '

                d_s = d.find_all('s')
                for s in d_s:
                    final_text += s.text+" "

                if divide_by_headline:
                    final_text += '\n'
                else:
                    final_text += ' '
                    
        return final_text