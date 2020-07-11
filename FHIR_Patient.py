"""
FHIR_Client - MusMuss
this script uses libraries
https://github.com/pandas-dev/pandas
https://github.com/numpy/numpy
https://github.com/smart-on-fhir/client-py
https://github.com/pyinstaller/pyinstaller
"""
import os

from fhirclient import client
from pandas import DataFrame

html_style = """<html>
<head>
<style>
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #dddddd;
}
</style>
</head>
<body>

<h2>"""


i=0
paddress = ""
ptelecom = ""

settings ={
    'app_id': 'my_web_app',
    'api_base': 'https://api.logicahealth.org/MST/open/'
}
smart = client.FHIRClient(settings=settings)

import fhirclient.models.patient as p
import fhirclient.models.practitioner as pr
import fhirclient.models.encounter as e
import fhirclient.models.observation as o


def askhtml(kuerzel,head):
    while True:
        query = input('Create html ?\n')
        Fl = query[0].lower()
        if query == '' or not Fl in ['y', 'n']:
            print('Please answer with yes or no!')
        else:
            break
    if Fl == 'y':
        f = open(kuerzel + ".html", "w")
        f.write(html_style+head+"</h2>")
        f.write(html)
        f.close()
        os.system("start " + kuerzel + ".html")
    if Fl == 'n':
        print("")


#list all patients #MIME18PM_GMSZ
Input = input("insert Patient Name E.g. 'MIME18PM' \n")
pID = []
pName =[]
patients =[]

search = p.Patient.where(struct={'name': Input})
patients = search.perform_resources(smart.server)
for pat in patients:
    pID.append(pat.id)
    try:
        pName.append(pat.name[0].given[0] + " "+ pat.name[0].family)
    except:
        pName.append("NONE " + pat.name[0].family)


dfPatients = DataFrame({   "Patient ID": pID,
                           "Name": pName})

print(dfPatients)
print("\n")

html = dfPatients.to_html()
head = "Liste aller "+Input+" Patienten"
kuerzel = Input
askhtml(kuerzel,head)

Input = input("insert Patient ID !\n")
patID = str(Input)

#Patient
patient = p.Patient.read(patID, smart.server)
pbirthday = patient.birthDate.isostring
pnamee = smart.human_name(patient.name[0])
pname = patient.name[0].family + ","

while i < len(patient.name[0].given):
    pname += " "
    pname += (patient.name[0].given[i])
    i+=1

pgender = patient.gender

pcity = patient.address[0].city
ppostal = patient.address[0].postalCode
phome = patient.address[0].line[0]
pstate = patient.address[0].state
pcountry = patient.address[0].country

paddress = phome + ", " + ppostal + " " + pcity + ", " + pstate + ", " + pcountry

i=0
while i < len(patient.telecom):
    ptelecom += patient.telecom[i].system
    ptelecom += ": "
    ptelecom += patient.telecom[i].value
    ptelecom += "\n"
    i+=1

print("Patient "+patID+" gefunden.\n")
print("Name, Vorname: " + pname + " "  + "\n" + "Geburtsdatum: " + pbirthday + "\n" + "Geschlecht: " + pgender + "\n" + "Adresse: " + paddress + "\n" + ptelecom)

#show all observations
oID =[]
opID =[]
oCode =[]
oCodeValue =[]
oDate =[]
oValue =[]
oName =[]

search = o.Observation.where(struct={'performer': patID})
observations = search.perform_resources(smart.server)
for obser in observations:
    oID.append(obser.id)
    opID.append(obser.performer[0].reference)
    oDate.append(obser.effectiveDateTime.isostring)
    oCodeValue.append(obser.code.coding[0].display)
    oCode.append(obser.code.coding[0].code)
    try:
        oValue.append(str(obser.valueQuantity.value) + " " + obser.valueQuantity.unit)
    except:
        oValue.append(obser.valueString)
    oName.append(pname)

dfObserAll = DataFrame({ "Observation ID": oID,
                        "Performer ID": opID,
                        "Name": oName,
                        "Date": oDate,
                        "Code": oCode,
                        "Code Value": oCodeValue,
                        "Messungen": oValue})

print("Verlaufsübersicht persönlicher Messungen.")
print(dfObserAll)
html = dfObserAll.to_html()
head = "Liste aller Observationen von "+ patID
kuerzel = "Observation_"+patID
askhtml(kuerzel,head)

#show encounters
eID =[]
eStart =[]
eEnd =[]
eValue =[]
eDoc =[]
eDocID =[]
eSub =[]

search = e.Encounter.where(struct={'subject': patID})
encounters = search.perform_resources(smart.server)
for enc in encounters:
    eID.append(enc.id)
    eStart.append(enc.period.start.isostring)
    eEnd.append(enc.period.end.isostring)
    eDoc.append(enc.participant[0].individual.display)
    eDocID.append(enc.participant[0].individual.reference)
    eSub.append(pname)
    #pat = int("".join(filter(str.isdigit, enc.subject.reference)))
    #patient = p.Patient.read(pat, smart.server)
    #eSub.append(str(smart.human_name(patient.name[0])))


dfEnc = DataFrame({   "Encounter ID": eID,
                      "Start": eStart,
                      "End": eEnd,
                      "Doc": eDoc,
                      "Doc ID":eDocID,
                      "Patient": eSub})

print(dfEnc)
print("\n")
html = dfEnc.to_html()
head = "Liste aller Encounter von "+ patID
kuerzel = "Encounter_"+patID
askhtml(kuerzel,head)

#show encouterobservation
oID = []
opID = []
oCode = []
oCodeValue = []
oDate = []
oValue = []
oName = []

Input =input("Enter Practitioner ID !\n")

search = o.Observation.where(struct={'performer': Input,'subject': patID, 'status': 'final'})
observations = search.perform_resources(smart.server)
for obser in observations:
    oID.append(obser.id)
    opID.append(obser.performer[0].reference)
    oDate.append(obser.effectiveDateTime.isostring)
    oCodeValue.append(obser.code.coding[0].display)
    oCode.append(obser.code.coding[0].code)
    try: #Wert+Einheit
        oValue.append(str(obser.valueQuantity.value) + " " + obser.valueQuantity.unit)
    except:#Versuche Blutdruck
        try:
            oValue.append("(" + obser.component[0].code.coding[0].display + "/" + obser.component[1].code.coding[
                0].display + ") " + str(obser.component[0].valueQuantity.value) + "/" + str(
                obser.component[1].valueQuantity.value) + " " + obser.component[0].valueQuantity.unit)
        except:#Versuche Schlafverhalten
            oValue.append(obser.valueString)
    oName.append(pname)

dfObser = DataFrame({"Observation ID": oID,
                     "Performer ID": opID,
                     "Patient": oName,
                     "Date": oDate,
                     "Code": oCode,
                     "Code Value": oCodeValue,
                     "Messungen": oValue})

print(dfObser)
print("\n")
html = dfObser.to_html()
head = "Liste aller Encounter Observationen von "+ patID
kuerzel = "Encounter_"+patID
askhtml(kuerzel,head)



# show other observations
def observa(Input):
    oID = []
    opID = []
    oCode = []
    oCodeValue = []
    oDate = []
    oValue = []
    oName = []

    search = o.Observation.where(struct={'performer': patID, 'code': str(Input)})
    observations = search.perform_resources(smart.server)
    for obser in observations:
        oID.append(obser.id)
        opID.append(obser.performer[0].reference)
        oDate.append(obser.effectiveDateTime.isostring)
        oCodeValue.append(obser.code.coding[0].display)
        oCode.append(obser.code.coding[0].code)
        try:
            oValue.append(str(obser.valueQuantity.value) + " " + obser.valueQuantity.unit)
        except:
            oValue.append(obser.valueString)
        oName.append(pname)

    dfObser = DataFrame({   "Observation ID": oID,
                            "Performer ID": opID,
                            "Name": oName,
                            "Date": oDate,
                            "Code": oCode,
                            "Code Value": oCodeValue,
                            "Messungen": oValue})

    kuerzel = "Observation_" + Input + "_" + patID
    html = dfObser.to_html()
    print(dfObser)
    return html

while True:
    quest = input('Look for speci Observations ?\n')
    Fl = quest[0].lower()
    if quest == '' or not Fl in ['y', 'n']:
        print('Please answer with yes or no!')
    else:
        break
if Fl == 'y':
    Input = input("Enter Observation Code\n")
    kuerzel = "Observation_" + Input + "_" + patID
    html = observa(Input)
    head = "Liste aller Observationen vom Typ " + Input
    askhtml(kuerzel,head)
    input("press key to close...")
if Fl == 'n':
    input("press key to close...")


#17862

"""    # Observation
    observation = o.Observation.read(Input, smart.server)
    operfomer = observation.performer[0].reference
    code = observation.code.coding[0].code
    codevalue = observation.code.coding[0].display

    print(operfomer + " found \n")
    operfomer = int("".join(filter(str.isdigit, operfomer)))

    print("Other Observations Found")"""