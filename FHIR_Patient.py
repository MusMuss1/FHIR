"""
FHIR_Client - MusMuss
this script uses libraries
https://github.com/pandas-dev/pandas
https://github.com/numpy/numpy
https://github.com/smart-on-fhir/client-py
https://github.com/pyinstaller/pyinstaller
"""
from fhirclient import client
from pandas import DataFrame

i=0
paddress = ""
ptelecom = ""

settings ={
    'app_id': 'my_web_app',
    'api_base': 'https://api.logicahealth.org/MST/open/'
}
smart = client.FHIRClient(settings=settings)

Input = input("Insert ID !\n")

import fhirclient.models.patient as p
import fhirclient.models.practitioner as pr
import fhirclient.models.encounter as e
import fhirclient.models.observation as o
import fhirclient.models.medicationrequest as m

practitioner = pr.Practitioner.read('16889', smart.server)
encounter = e.Encounter.read('17903', smart.server)

#Observation
observation = o.Observation.read(Input, smart.server)
operfomer = observation.performer[0].reference
code = observation.code.coding[0].code
codevalue = observation.code.coding[0].display

print(operfomer + " found \n")
operfomer = int("".join(filter(str.isdigit, operfomer)))

#Patient
patient = p.Patient.read(operfomer, smart.server)
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

print("Name, Vorname: " + pname + " "  + "\n" + "Geburtsdatum: " + pbirthday + "\n" + "Geschlecht: " + pgender + "\n" + "Adresse: " + paddress + "\n" + ptelecom)

print("Other Observations Found")

oID =[]
oDate =[]
oValue =[]
oName =[]

search = o.Observation.where(struct={'performer': str(operfomer),'code': str(code)})
observations = search.perform_resources(smart.server)
for obser in observations:
    oID.append(obser.id)
    oDate.append(obser.effectiveDateTime.isostring)
    oValue.append(str(obser.valueQuantity.value)+obser.valueQuantity.unit)
    oName.append(pname)


dfObser = DataFrame({   "Observation ID": oID,
                        "Name": oName,
                        "Date": oDate,
                        str(codevalue): oValue})

print(dfObser)
print("\n")

eID =[]
eStart =[]
eEnd =[]
eValue =[]
eDoc =[]
eSub =[]

search = e.Encounter.where(struct={'subject': str(operfomer)})
encounters = search.perform_resources(smart.server)
for enc in encounters:
    eID.append(enc.id)
    eStart.append(enc.period.start.isostring)
    eEnd.append(enc.period.end.isostring)
    eDoc.append(enc.participant[0].individual.display)
    eSub.append(pname)
    #pat = int("".join(filter(str.isdigit, enc.subject.reference)))
    #patient = p.Patient.read(pat, smart.server)
    #eSub.append(str(smart.human_name(patient.name[0])))


dfEnc = DataFrame({   "Encounter ID": eID,
                      "Start": eStart,
                      "End": eEnd,
                      "Doc": eDoc,
                      "Patient": eSub})

print(dfEnc)
print("\n")
html = dfObser.to_html() + dfEnc.to_html()
f = open("file2.html", "w")
f.write(html)
f.close()


input("press key to close")
#17862