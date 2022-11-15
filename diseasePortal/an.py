import re
import re
import PyPDF2
import numpy as np
import joblib

pdfFileObj = open('D:/Propy/Django/diseasePortal/diseasePortal/tp81.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

if pdfReader.numPages == 2:
        pageObj = pdfReader.getPage(0)
        pageObj1 = pdfReader.getPage(1)
        first = pageObj.extractText().replace(' ',"")
        second = pageObj1.extractText().replace(' ',"")
        sent = first.replace('\n','')
        senny = second.replace('\n','')
        sen = (sent + senny).lower()


elif pdfReader.numPages == 1:
        pageObj = pdfReader.getPage(0)
        first = pageObj.extractText()
        # sen = first.replace('\n','').lower()
        print(first)

# words = ["name", "age", "specificgravity", "albumin","serumcreatinine","haemoglobin","packedcellvolume","redbloodcellcount","hypertension","diabetes"]
# #  words = ["Name", "Age", "Specificgravity", "Albumin","SerumCreatinine","Haemoglobin","PackedCellVolume","RedBloodCellCount","Hypertension","Diabetes"]


# sentence = re.sub(r"(?<!^)[\s,]*({})\s*:".format('|'.join(words)), ", \\1:", sen)
# # print(sentence)
# splits = re.split(r':|,|\n',sentence)
# # print(splits)
# k = []
# o = []
# even = []
# odd = []
# for i in range(0,len(splits)):
#                 if i % 2:
#                         even.append(splits[i])
#                 else:
#                         odd.append(splits[i])
# for i in even:
#         j = i.lstrip().rstrip()
#         k.append(j)
# for i in odd:
#         j = i.lstrip().rstrip()
#         o.append(j)

# o[0] = k[0]
# o[1] = k[1]
# o[2] = float(k[2])
# o[3] = float(k[3])
# o[4] = float(k[4])
# o[5] = float(k[5])
# o[6] = float(k[6])
# o[7] = float(k[7])
# if k[8] == "No":
#         k[8] = 0
# else:
#         k[8] = 1
# if k[9] == "No":
#         k[9] = 0
# else:
#         k[9] = 1
# o[8] = int(k[8])
# o[9] = int(k[9])
