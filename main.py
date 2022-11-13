from pyswip import Prolog
import pandas as pd
import numpy as np

prolog = Prolog()
prolog.consult("main.pl")


def getDoctorSuggestion():
    print("Get Doctor profile based on specialization")
    print("-------------------------------------------")
    doctor_df = pd.read_csv("doctor_link.csv")
    doctor_type_list={"General Physician":"general_physician","Homoeopath":"homoeopath","Ear-Nose-Throat Specialist":"ear_nose_throat_specialist","Ayurveda":"ayurveda","Dermatologist":"dermatologist","Gynecologist/Obstetrician":"gynecologist"}
    print("Available Doctor Types")
    doctor_type_list_names=list(doctor_type_list.keys())
    for i in range(len(doctor_type_list_names)):
        print(str(i+1)+" "+doctor_type_list_names[i])
    print("-------------------------------------------")
    doctor_type_ind  = int(input("Enter the doctor type number \n"))
    doctor_type = doctor_type_list[doctor_type_list_names[doctor_type_ind-1]]
    doctors_nicknames=list(prolog.query("getdoctor("+doctor_type+",X)."))
    for doctors_nickname in doctors_nicknames:
        for i in range(len(doctor_df)):
            if doctor_df.iloc[i,4]==doctors_nickname['X']:
                print("-------------------------------------------")
                print("Doctor Name : "+doctor_df.iloc[i,1])
                print("Profile Link : "+doctor_df.iloc[i,2])
                print("Doctor Type : "+doctor_df.iloc[i,3])
                print("-------------------------------------------")
                break

def diseaseDescription():
    print("Disease Description")
    
    disease_df = pd.read_csv("Disease_Description.csv")
    disease_list = list(disease_df['Nickname'])
    disease_name = input("Enter a Disease Name\n")
    def replaceSpace(string):
        temp=""
        for i in string:
            if(i==' '):
                temp+="_"
            else:
                temp+=i
        return temp.lower()
    disease_name =replaceSpace(disease_name)
    print("-------------------------------------------")
    for i in disease_list:
        newi = replaceSpace(i)
        if(newi==disease_name):
            disease_ind=list(prolog.query("getdiseasedescription("+disease_name+",X)."))[0]['X']
            print("Disease Name : "+disease_df.iloc[disease_ind,2])
            print("Disease Description : "+disease_df.iloc[disease_ind,3])
            print("-------------------------------------------")
            return
    print("Sorry, Disease cannot be found")
    print("-------------------------------------------")
    return

def diseaseFromSymptoms():
    print("Get Disease name from symptoms you have")
    print("-------------------------------------------")
    disease_df = pd.read_csv("dataset.csv")
    symptom_set = set()
    for i in range(len(disease_df)):
        for j in range(1,14):
            symptom = disease_df.iloc[i,j]
            if type(symptom) == str:
                symptom_set.add(symptom.lower())

    # print(disease_set)
    symptom_set=sorted(symptom_set)
    print("List of symptoms\n")
    for symptom in symptom_set:
        symptom = symptom.strip()
        print(symptom.capitalize())
    user_symptoms = input("Enter the symptoms(Max 4) separated by space(use _ incase of space for a symptom)").split(" ")
    user_symptoms.sort()
    print(user_symptoms)
    var=["W","X","Y","Z"]
    ind=0
    def getonepermutation(user_symptoms):
        temp=[]
        for i in range(4):
            user_symptoms.insert(i,"A")
            tempstr=",".join(user_symptoms)
            tempstr=tempstr+","+"X"
            temp.append(tempstr)
            user_symptoms.pop(i)
        return temp
    def gettwopermutation(user_symptoms):
        temp=[]
        indexs =[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]
        for index in indexs:
            user_symptoms.insert(index[0],"A")
            user_symptoms.insert(index[1],"B")
            tempstr=",".join(user_symptoms)
            tempstr=tempstr+","+"X"
            temp.append(tempstr)
            user_symptoms.pop(index[0])    
            user_symptoms.remove("B")          
        return temp
    def getthreepermutation(user_symptoms):
        temp=[]
        symptom=user_symptoms[0]
        user_symptoms=["A","B","C"]
        for i in range(4):
            user_symptoms.insert(i,symptom)
            tempstr=",".join(user_symptoms)
            tempstr=tempstr+","+"X"
            temp.append(tempstr)
            user_symptoms.pop(i)  
        return temp     
    if len(user_symptoms)==3:
        all_one_permutation=getonepermutation(user_symptoms)
        for permut in all_one_permutation:
            disease_result=list(prolog.query("getdiseasesymptoms("+permut+")."))
            if(len(disease_result)>=1):
                for i in range(len(disease_result)):
                    print("If you also have "+disease_result[i]['A']+". Then you have "+disease_result[i]['X'])
        
    elif len(user_symptoms)==2:
        all_two_permutation=gettwopermutation(user_symptoms)
        for permut in all_two_permutation:
            disease_result=list(prolog.query("getdiseasesymptoms("+permut+")."))
            if(len(disease_result)>=1):
                for i in range(len(disease_result)):
                    print("If you also have "+disease_result[i]['A']+" and "+disease_result[i]['B']+". Then you have "+disease_result[i]['X'])

    elif len(user_symptoms)==1:
        all_three_permutation=getthreepermutation(user_symptoms)
        for permut in all_three_permutation:
            disease_result=list(prolog.query("getdiseasesymptoms("+permut+")."))
            if(len(disease_result)>=1):
                for i in range(len(disease_result)):
                    print("If you also have "+disease_result[i]['A']+", "+disease_result[i]['B']+" and "+disease_result[i]['C']+". Then you have "+disease_result[i]['X'])
    print("-------------------------------------------")
def getsymptoms():
    print("Get symptoms of a Disease")
    print("-------------------------------------------")
    disease_df = pd.read_csv("dataset.csv")
    disease = input("Enter a disease\n")
    print("-------------------------------------------")
    for i in range(len(disease_df)):
        if disease==disease_df.iloc[i,0].lower():
            for j in range(14):
                if type(disease_df.iloc[i,j])==str:
                    print(disease_df.iloc[i,j].strip().capitalize())
            return
def start():
    tasks = ["1. Get Description of various diseases.","2. Get disease name based on the symptoms.",
    "3. Get list of symptoms for a disease","4. Get Doctor profiles based on criteria","5. EXIT"]
    
    res=1
    while True:
        print("-------------------------------------------")
        for i in tasks:
            print(i)
        print("-------------------------------------------")
        res=int(input("Select a choice\n"))
        if(res==1):
            diseaseDescription()
        elif res==2:
            diseaseFromSymptoms()
        elif res==3:
            getsymptoms()
            print("-------------------------------------------")
        elif res==4:
            getDoctorSuggestion()
        elif res==5:
            break
        else:
            print("Enter a valid input.")

start()