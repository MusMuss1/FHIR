from fhirclient import client
settings ={
    'app_id': 'my_web_app',
    'api_base': 'https://api.logicahealth.org/MST/open/'
}
smart = client.FHIRClient(settings=settings)

import fhirclient.models.patient as p

patient = p.Patient.read('17852', smart.server)


pbirthday = patient.birthDate.isostring
pnamee = smart.human_name(patient.name[0])
pname = patient.name[0].family
pvname = patient.name[0].given[0]
pvname1 = patient.name[0].given[1]
pgender = patient.gender

pcity = patient.address[0].city
ppostal = patient.address[0].postalCode
phome = patient.address[0].line[0]
pstate = patient.address[0].state
pcountry = patient.address[0].country

paddress = phome + ", " + ppostal + " " + pcity + ", " + pstate + ", " + pcountry

psys = patient.telecom[0].system
pvalue = patient.telecom[0].value
puse = patient.telecom[0].use

pphone = psys + ": " + puse + ", " + pvalue

psys2 = patient.telecom[1].system
pvalue2 = patient.telecom[1].value

pmaail = psys2 + ": " + pvalue2

print("Name, Vorname: " + pname + ", " + pvname + " " +pvname1 + "\n" + "Geburtsdatum: " + pbirthday + "\n" + "Geschlecht: " + pgender + "\n" + "Adresse: " + paddress + "\n" + pphone + "\n" + pmaail)

