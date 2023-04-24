from bs4 import BeautifulSoup as bs
from textblob import Word
import re

class GrobidOutputReader:

    """
        The output of Grobid is an xml file. This class reads the xml file and converts it to a plain text file.
        
        Initializes a GrobidOutputReader object with specified parser.
        :param parser: The name of the parser to use. Default is 'lxml-xml'.
        :type parser: str
        for more unformaton about parsers, see https://beautiful-soup-4.readthedocs.io/en/latest/index.html?highlight=parser#installing-a-parser
        :param spell_corrector: If True, the text will be spell corrected. The default is True.
        :type spell_corrector: bool
    
    """

    def __init__(self, parser = "lxml-xml", spell_corrector = True):
        self.parser = parser
        self.spell_corrector = spell_corrector

    # calculate the jacaard similarity between two words
    @staticmethod
    def jacaard_similarity(x, y):
        x = set(x)
        y = set(y)
        return len(x.intersection(y)) / len(x.union(y))


    def correct_spelling(self, sentence, similarity = jacaard_similarity):

        # regex to find all the words in the sentence with upper case letters from second letter to the end
        words = re.findall(r"\b\w*[a-z]\w*[A-Z][a-z]*\w*\b", sentence)
        
        if len(words) > 0:
            for word in words:
                # replace upper case letters with 'f' letter
                word_f = re.sub(r'[A-Z]', 'f', word)
                word_blob = Word(word_f)
                if len(word_blob.spellcheck()) > 1:
                    # compute the jacaard similarity between the word_f and the all words in the spellcheck list
                    jacaard_similarities = [similarity(word_f, word[0]) for word in word_blob.spellcheck()]
                    # find the index of the word with the highest jacaard similarity
                    index = jacaard_similarities.index(max(jacaard_similarities))
                    # replace the word with the correct spelling
                    sentence = sentence.replace(word, word_blob.spellcheck()[index][0])
                else:
                    # replace the word with the correct spelling
                    sentence = sentence.replace(word, word_blob.spellcheck()[0][0])
        return sentence


    def XMLtoText(self, xml_file, divide_by_headline = True):
        """
            Reads the xml file and converts it to a plain text file.
            Parameters
            ----------
            xml_file : str
                The path to the xml file.
                Note: Its better to use the absolute path with r before the path.
            divide_by_headline : bool, optional
                If True, the text will be divided by headlines. The default is True.
            Returns
            -------
            str
                The plain text file.
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

        if divide_by_headline:
            # loop through all divs
            for d in all_div:
                # if there is a headline, add it to the final_text
                if d.head:
                    final_text += d.head.text + ': \n'

                    d_s = d.find_all('s')

                    for s in d_s:
                        final_text += s.text+" "

                    final_text += '\n'
                # if there is no headline, add "No Headline:" to the final_text
                else:
                    final_text += 'No Headline:'+ '\n'

                    d_s = d.find_all('s')
                    for s in d_s:
                        final_text += s.text+" "

                    final_text += '\n'
        else:
            for d in all_div:
                d_s = d.find_all('s')
                for s in d_s:
                    final_text += s.text+" "

        return final_text
    

    def XMLtoDict(self, path, sentence_len_threshold = 5):

        """
            Reads the xml file and converts it to a dictionary.
            Parameters
            ----------
            path : str
                The path to the xml file.
                Note: Its better to use the absolute path with r before the path.
            Returns
            -------
            dict
                The dictionary with the following keys:
                title: str
                    The title of the paper.
                doi: str
                    The doi of the paper.
                md5: str
                    The md5 of the paper.
                authors: list
                    The list of authors of the paper with forename and surname.
                keywords: list
                    The list of keywords of the paper.
                date: str
                    The date of the paper.
                sentences: list 
                    The list of sentences of the paper.
            
        """

        with open(path) as f:
            text = f.read()

        soup = bs(text, self.parser)

        # paper title
        title = soup.title

        try:
            title = title.text
            if len(title)<1:
                title = "No Title"
        except:
            title = "No Title"
            
        # paper doi
        idno_doi = soup.find('idno', type='DOI')
        if idno_doi:
            idno_doi = idno_doi.text
        else:
            idno_doi = "No DOI"

        # paper md5
        idno_md5 = soup.find('idno', type='MD5')
        if idno_md5:
            idno_md5 = idno_md5.text
        else:
            idno_md5 = "No MD5"

        # paper date
        date_tag = soup.find('date')
        if date_tag:
            date = date_tag.get('when')
        else:
            date = "No Date"

        # paper authors
        sourceDesc = soup.sourceDesc
        try:

            persName = sourceDesc.find_all('persName')
            authors_list = [{'forename': author.forename.text, 'surname': author.surname.text} for author in persName]
            if len(authors_list)<1:
                authors_list = ["No Authors"]
          
        except:
            authors_list = ["No Authors"]
        
        
        # paper keywords
        keywords = soup.find_all('term')
        if keywords:
            keywords_list = [keyword.text for keyword in keywords]
        else:
            keywords_list = ["No Keywords"]

        # paper sentences
        sentences = soup.find_all('s')
        if sentences:
            if self.spell_corrector:
                # sentences_list = [self.correct_spelling(sentence.text) for sentence in sentences]
                # check if the sentence is long enough
                sentences_list = [self.correct_spelling(sentence.text) for sentence in sentences if len(sentence.text.split()) > sentence_len_threshold]
            else:
                # sentences_list = [sentence.text for sentence in sentences]
                # check if the sentence is long enough
                sentences_list = [sentence.text for sentence in sentences if len(sentence.text.split()) > sentence_len_threshold]
        else:
            sentences_list = ["No Sentences"]

        return {
                'title': title,
                'doi': idno_doi,
                'md5': idno_md5,
                'date': date,
                'authors': authors_list,
                'keywords': keywords_list,
                'sentences': sentences_list
                }