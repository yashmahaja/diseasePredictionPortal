from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.contrib import auth
import pyrebase
import numpy as np
import joblib
import firebase_admin
from firebase_admin import credentials, firestore
from django.shortcuts import render,HttpResponse
from .models import FileUpload
from .functions import handle_uploaded_file
from .functions import process
from .forms import StudentForm 
import re


config = {
  'apiKey': "AIzaSyBKD1ME4nuheRuVpQfzwb9Vrp8nqgJ0yRg",
  'authDomain': "diseaseportal.firebaseapp.com",
  'projectId': "diseaseportal",
  'storageBucket': "diseaseportal.appspot.com",
  'messagingSenderId': "50470373235",
  'appId': "1:50470373235:web:d1b3fa03ea977a9b546706",
  'databaseURL' : "",

}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
cred = credentials.Certificate('diseasefire.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def signIn(request):
    return render(request,"signIn.html")

def logout(request):
    auth.logout(request)
    return render(request, "signIn.html")
    
def postsign(request):
    email = request.POST.get('email')
    password = request.POST.get('pass')

    try:
          user = authe.sign_in_with_email_and_password(email,password) 
    except:
        message = "Invalid Credentials"
        return render(request, "signIn.html", {"messg" : message})
    # print(user['idToken'])
    session = user['idToken']
    request.session['uid'] = str(session)
    return render(request, "welcome.html",{"e":email})

def uploadresult(request):  
    model = joblib.load('rf.pkl')
    logireg = joblib.load("logreg.pkl")
    knn = joblib.load("knn.pkl")
    dt = joblib.load("decisiontree.pkl")
    svm = joblib.load("svm.pkl")
    navbay = joblib.load("naivebayes.pkl")
    
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():  
            handle_uploaded_file(request.FILES['file']) 
            give = process(request.FILES['file'])
            if give == "Error":
                return render(request,"error.html")
            else:
                i = []
                for j in give:
                    i.append(j)
                name = i[0]
                name = re.sub(r"(\w)([A-Z])", r"\1 \2", name)
                age = i[1]
                sg = float(i[2])
                al = float(i[3])
                sc = float(i[4])
                haem = float(i[5])
                pcv = float(i[6])
                rbcc = float(i[7])
                htn = int(i[8])
                dia = int(i[9])
                prob_percent_0 = float(i[10])
                global prob_percent_1 
                prob_percent_1 = float(i[11])
                labels = ["NOT CKD","CKD"]
                data = [prob_percent_0,prob_percent_1]
                arr = np.array([[sg,al,sc,haem,pcv,rbcc,htn,dia]])
                logistic = logireg.predict(arr)[0]
                b = navbay.predict(arr)[0]
                c = knn.predict(arr)[0]
                d = dt.predict(arr)[0]
                e = svm.predict(arr)[0]
                f = model.predict(arr)[0]
                op = b,c,d,e,logistic,f
                predss = list(op)
                cnt = predss.count(1)
                if cnt == 6:
                    value = "Strongly Positive"
                elif cnt == 5:
                    value = "Somewhat Positive"
                elif cnt == 4:
                    value = "Slightly Positive"
                elif cnt == 3:
                    value = "Can't Say"
                elif cnt == 2:
                    value = "Slightly Negative"
                elif cnt == 1:
                    value = "Somewhat Negative"
                elif cnt == 0:
                    value = "Strongly Negative"
                if htn == 0:
                    res = "No"
                else:
                    res = "Yes"
                if dia == 0:
                    res1 = "No"
                else:
                    res1 = "Yes"
                context = {
                    'name': name,
                    'sg': sg,
                    'al': al,
                    'sc': sc,
                    'haem': haem,
                    'pcv': pcv,
                    'rbcc': rbcc,
                    'htn': res,
                    'dia': res1, 
                    'pred': prob_percent_0,
                    'pred1': prob_percent_1,
                    'age': age,
                    'labels': labels,
                    'data' : data,
                    'value' : value,
                    'predss': predss,
                }
                datas = {
            'specificGravity': sg,
            'albumin': al,
            'serumCreatinine': sc,
            'haemoglobin': haem,
            'packedCellVolume': pcv,
            'redBloodCellCount': rbcc,
            'hypertension': res,
            'diabetes': res1,
             'pred': prob_percent_0,
            'pred1': prob_percent_1,
            }
                db.collection('data').document().set(datas)
                idtoken = request.session['uid']
                a = authe.get_account_info(idtoken)
                a = a['users']
                a = a[0]
                a = a['localId']
                print(str(a))
                return render(request,"result.html",context)
    else:  
        student = StudentForm()  
        return render(request,"welcome.html",{'form':student})  


def result(request):

    model = joblib.load('rf.pkl')
    logireg = joblib.load("logreg.pkl")
    knn = joblib.load("knn.pkl")
    dt = joblib.load("decisiontree.pkl")
    svm = joblib.load("svm.pkl")
    navbay = joblib.load("naivebayes.pkl")
    sg = float((request.GET['sg']))
    name = (request.GET['name'])
    age = int((request.GET['age']))
    al = float((request.GET['albumin']))
    # bg = float((request.GET['bg']))
    sc = float((request.GET['sc']))
    haem = float((request.GET['haemo']))
    pcv = float((request.GET['pcv']))
    rbcc = float((request.GET['rbcc']))
    htn = int((request.GET['hypertension']))
    dia = int((request.GET['diabetes']))
    arr = np.array([[sg,al,sc,haem,pcv,rbcc,htn,dia]])
    pred = model.predict_proba(arr)
    logistic = logireg.predict(arr)[0]
    b = navbay.predict(arr)[0]
    c = knn.predict(arr)[0]
    d = dt.predict(arr)[0]
    e = svm.predict(arr)[0]
    f = model.predict(arr)[0]
    op = b,c,d,e,logistic,f
    predss = list(op)
    cnt = predss.count(1)
    if cnt == 6:
        value = "Strongly Positive"
    elif cnt == 5:
        value = "Somewhat Positive"
    elif cnt == 4:
        value = "Slightly Positive"
    elif cnt == 3:
        value = "Can't Say"
    elif cnt == 2:
        value = "Slightly Negative"
    elif cnt == 1:
        value = "Somewhat Negative"
    elif cnt == 0:
        value = "Strongly Negative"
    p = list(np.array(pred)[0])
    prob_percent_0 = round(p[0]*100,2)
    global prob_percent_1
    prob_percent_1 = round(p[1]*100,2)
    labels = ["NOT CKD","CKD"]
    data = [prob_percent_1,prob_percent_0]
    # if pred == 0:
    #      value = "You have CKD"
    # else:
    #      value = "You don't have CKD"
    if htn == 0:
        res = "No"
    else:
        res = "Yes"
    if dia == 0:
        res1 = "No"
    else:
        res1 = "Yes"
    context = {
        'sg': sg,
        'al': al,
        # 'bg': bg,
        'sc': sc,
        'haem': haem,
        'pcv': pcv,
        'rbcc': rbcc,
        'htn': res,
        'dia': res1, 
        'pred': prob_percent_0,
        'pred1': prob_percent_1,
        'labels': labels,
        'data': data,
        'name': name,
        'age': age,
        'predss': predss,
        'value' : value

    }
    datas = {
        'specificGravity': sg,
        'albumin': al,
        'serumCreatinine': sc,
        'haemoglobin': haem,
        'packedCellVolume': pcv,
        'redBloodCellCount': rbcc,
        'hypertension': res,
        'diabetes': res1,
         'pred': prob_percent_0,
        'pred1': prob_percent_1
    }
    db.collection('data').document().set(datas)
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print(str(a))
    template = 'result.html'
    return render(request,template,context)

def fdata(request):
    patients = db.collection('data').where("pred1", "==", prob_percent_1).limit(5).get()
    context = {
        'patients': [patient.to_dict() for patient in patients],
    }
    return render(request,"data.html",context)