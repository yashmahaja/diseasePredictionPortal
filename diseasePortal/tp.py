import re
import PyPDF2
import numpy as np
import joblib
import spacy

pdfFileObj = open('D:/Propy/Django/diseasePortal/diseasePortal/medicalreport.pdf', 'rb')
# pdfFileObj = open('D:/Propy/Django/diseasePortal/diseasePortal/static/uploads/tp69.pdf', 'rb')
# pdfFileObj = open('D:/Propy/Django/diseasePortal/diseasePortal/tp80.pdf', 'rb') 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)
content = pageObj.extractText()
namePattern = "([A-Z][a-z]+(?: [A-Z][a-z]\.)? [A-Z][a-z]+)"
pattern = "AGE|age|Age.*:\s*(.\d+)" 
# pattern = "Age|age|AGE.*([^\:]\d+)"
finalPattern = "(age|Age|AGE)+.*\s*(.\d+)"
edgecase = "(age|Age|AGE)+.{*:\s{0,}}*(.\d+)"
# print(content)
b = re.findall(edgecase,content)
a = re.findall(namePattern,content)

nlp = spacy.load("en_core_web_sm")
doc = nlp(content)

print(doc)