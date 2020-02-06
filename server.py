from http.server import HTTPServer, BaseHTTPRequestHandler
from PyPDF4 import PdfFileReader
import textdistance as td
import re

def fuzzy_match(list1, list2):
    min_dist = 10
    min_word1 = ''
    min_word2 = ''
    
    for word1 in list1:
        for word2 in list2:
            cur_dist = td.levenshtein.distance(word1.replace('(%)', '').lower().replace('tax', '').replace('rate', ''), 
                                               word2.replace('(%)', '').lower().replace('tax', '').replace('rate', ''))
            if cur_dist < min_dist:
                min_dist = cur_dist
                min_word1 = word1
                min_word2 = word2
                
    return [min_word1, min_word2]

def get_subsentences(string):
    sentence = string.split(' ')
    return [' '.join(sentence[i:j]) for i in range(len(sentence)) 
            for j in range(i + 1, len(sentence) + 1)]

def get_answer(question):
    substrings = get_subsentences(question)
    country = fuzzy_match(substrings, rates_dict.keys())[1]
    rate = fuzzy_match(substrings, rates_dict[country].keys())[1]
    
    return ('The ' + rate + ' in ' + country + ' is ' + rates_dict[country][rate] + '. '
        'Please check <a href="https://www.ey.com/Publication/vwLUAssets/ey-worldwide-corporate-tax-guide-2019/$FILE/ey-worldwide-corporate-tax-guide-2019.pdf#page=' + 
        str(page_no[country]) + '">page ' + str(page_no[country] - 9) + '</a> of the Tax Guide for more information.')

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        body = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(get_answer(body.decode('utf-8')).encode('utf-8'))

reader = PdfFileReader(open('tax-guide.pdf', 'rb'))
content = ""
indexes = []
for i in range(0,1898):
    cur_page = reader.getPage(i).extractText()
    content += cur_page + '\n'
    
    if len(re.split(r'\nA\. (\w| )+\n', cur_page)) > 1:
        indexes.append(i+1)
        
content = content.split('ey.com/GlobalTaxGuides\n \ney.com/TaxGuidesApp\n')

country_dict = {}
page_no = {}
for i in range(1, len(content)):
    country_dict[content[i-1].split('\n')[-2]] = content[i]
    page_no[content[i-1].split('\n')[-2]] = indexes[i-1]

rates_dict = {}
for key in country_dict.keys():
                    
    country_rates = (re.split(r'\n[A-F]\. (\w| )+\n',
                              (re.sub(r'\([a-z]\)', '', country_dict[key])))[2]
                       .split('\n \n'))
    
    for i in reversed(range(len(country_rates))):

        if country_rates[i][:1] == ' ':
            j = 1
            while not re.match(r'[A-Z]', country_rates[i-j][:1]):
                j += 1
            country_rates[i] = country_rates[i-j] + ' on ' + country_rates[i][2:]
    
    rates_dict[key] = {}
    for i in range(len(country_rates)):
        if country_rates[i].replace('\n', '').isnumeric():
            rates_dict[key][country_rates[i-1].replace('\n', '').strip()] = country_rates[i].replace('\n', '').strip()


print("Ready!")
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()