from PyPDF4 import PdfFileReader
import re

reader = PdfFileReader(open("tax-guide.pdf", "rb"))

content = ""
for i in range(0,1898):
    content += reader.getPage(i).extractText() + "\n"
content = content.split("ey.com/GlobalTaxGuides\n \ney.com/TaxGuidesApp\n")

country_dict = {}
for i in range(1, len(content)):
    country_dict[content[i-1].split('\n')[-2]] = content[i]
    
#country_dict.keys()
#country_dict['Australia']

rates = re.split(r'\w\n\(a\)\n \n', 
                 re.split(r'\n[A-F]\.(\w| )+\n', 
                          country_dict['Australia'])[2])[0].split('\n \n')

rates_dict = {}
for i in range(len(rates)):
    if rates[i].isnumeric():
        rates_dict[rates[i-1]] = rates[i]
        
#rates
#rates_dict.keys()
#rates_dict['Corporate Income Tax Rate (%)']