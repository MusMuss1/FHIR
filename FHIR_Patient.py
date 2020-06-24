from fhirclient import client

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

practitioner = pr.Practitioner.read('16889', smart.server)
encounter = e.Encounter.read('17903', smart.server)

#Observation
observation = o.Observation.read(Input, smart.server)
operfomer = observation.performer[0].reference

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

print(pnamee)