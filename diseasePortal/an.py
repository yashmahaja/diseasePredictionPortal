import re
import re
import PyPDF2
import numpy as np
import joblib
import os
import filetype

model = joblib.load('D:/Propy/Django/diseasePortal/diseasePredictionPortal/rf.pkl')

def process(f):
        pdfFileObj = open(f, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        if pdfReader.numPages == 2:
                pageObj = pdfReader.getPage(0)
                pageObj1 = pdfReader.getPage(1)
                first = pageObj.extractText().replace(' ',"")
                second = pageObj1.extractText().replace(' ',"")
                sent = first.replace('\n','')
                senny = second.replace('\n','')
                sen = sent + senny
        elif pdfReader.numPages == 1:
                pageObj = pdfReader.getPage(0)
                first = pageObj.extractText().replace(' ',"")
                sen = first.replace('\n','')


        words = ["name", "age", "specificgravity", "albumin","serumCreatinine","haemoglobin","packedcellvolume","redbloodcellcount","hypertension","diabetes"]
        words = ["Name", "Age", "Specificgravity", "Albumin","SerumCreatinine","Haemoglobin","PackedCellVolume","RedBloodCellCount","Hypertension","Diabetes"]
        sentence = re.sub(r"(?<!^)[\s,]*({})\s*:".format('|'.join(words)), ", \\1:", sen)
        splits = re.split(r':|,|\n',sentence)
        k = []
        o = []
        even = []
        odd = []
        for i in range(0,len(splits)):
                        if i % 2:
                                even.append(splits[i])
                        else:
                                odd.append(splits[i])
        for i in even:
                j = i.lstrip().rstrip()
                k.append(j)
        for i in odd:
                j = i.lstrip().rstrip()
                o.append(j)

        o[0] = k[0]
        o[1] = k[1]
        o[2] = float(k[2])
        o[3] = float(k[3])
        o[4] = float(k[4])
        o[5] = float(k[5])
        o[6] = float(k[6])
        o[7] = float(k[7])
        if k[8] == "No":
                k[8] = 0
        else:
                k[8] = 1
        if k[9] == "No":
                k[9] = 0
        else:
                k[9] = 1
        o[8] = int(k[8])
        o[9] = int(k[9])

        arr = np.array([[o[2],o[3],o[4],o[5],o[6],o[7],o[8],o[9]]])
        pred = model.predict_proba(arr)
        p = list(np.array(pred)[0])
        prob_percent_0 = round(p[0]*100,2)
        global prob_percent_1
        prob_percent_1 = round(p[1]*100,2)
        return [o[0],o[1], o[2],o[3],o[4],o[5],o[6],o[7],o[8],o[9], prob_percent_0,prob_percent_1]
            

a = process('D:/Propy/Django/diseasePortal/diseasePredictionPortal/diseasePortal/tp81.pdf')
print(prob_percent_1)