#!/usr/bin/env python
# coding: utf-8

import io
import sys


from PIL import Image
from pyzbar import pyzbar


import os
import sys
import json
import base64
#import requests
from OpenSSL import crypto
from binascii import hexlify
from bs4 import BeautifulSoup
from cose.keys import CoseKey
import sys
import glob
import json
import zlib
import flynn
import base45
#import PyPDF2
from PIL import Image
from pyzbar import pyzbar
from datetime import datetime
from urllib.request import urlopen


from datetime import datetime, timedelta

# Import des autres fichiers pythons
from nam import *
from GroupIdentifier.byRecovery import *
from GroupIdentifier.byTesting import *
from GroupIdentifier.byVaccination import *


# Récupération du modèle théorique d'un pass sanitaire

sch = urlopen('https://raw.githubusercontent.com/ehn-dcc-development/ehn-dcc-schema/release/1.3.0/DCC.combined-schema.json')
glb_schema = json.load(sch)


# Création d'une classe liée au passe covid (en anglais : GreenPass)

class CovidPass:
    
    filePath = None
    fileType = None
    PassFile = None
    
    QRCodedata        = None
    QRCodedataDecoded = None
    
    QRCodeIssuer = None
    QRCodeDateExpiry = None
    QRCodeDateGenerated = None
    QRCodeValidityDate = None
    
    PassExpiryDate = None
    GroupIdentifier = None
    
    PersoneNameInformation = nam()
    byVaccination = vaccination()
    byTesting = testing()
    byRecovery = recovery()
    
    isValid = None
    
    Ver = None
    Dob = None
    
    
    SchemaVersion = None
    data = None

    def __init__(self,filepath=None,fileType=None,QRCodedata=None):
        self.filePath = filepath
        self.fileType = fileType
        self.QRCodedata = QRCodedata
    
    #ReadQRCode : fonction qui lit le QR sur une image png.
    def readQRcode(self):
        if self.fileType == "png":
            img = Image.open(self.filePath)
            decoded = pyzbar.decode(img)
            #decoded = pyzbar.decode(img)[0].data
            if len(decoded) < 1:
                print("[-] Value not found", file=sys.stderr)
                #sys.exit(1)
            output = decoded[0]
            if output.type != "QRCODE":
                print("[-] Not a qrcode", file=sys.stderr)
                #sys.exit(1)
            self.QRCodedata  = output.data

        return self.QRCodedata 
    
    
    def readQrCode_from_image(self,img):
        """
        Lire le QR sur une image déjà lu et chargé en mémoire
        """
        decoded = pyzbar.decode(img)
        if len(decoded) < 1:
            print("[-] Value not found", file=sys.stderr)
            return None
        output = decoded[0]
        if output.type != "QRCODE":
            print("[-] Not a qrcode", file=sys.stderr)
            return None
        self.QRCodedata  = output.data
        return self.QRCodedata 

    

    def decodeQRcodeData(self,b_print=False):
        QRcodedataDecodedCompress = base45.b45decode(self.QRCodedata[4:])
        self.QRcodedataDecoded = zlib.decompress(QRcodedataDecodedCompress) # decompress:
        (_, (headers1, headers2, cbor_data, signature)) = flynn.decoder.loads(self.QRcodedataDecoded)  # decode cose document:
       
        data = flynn.decoder.loads(cbor_data) # decode
        date = lambda ts: datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        self.QRCodeIssuer = data[1]
        self.QRCodeDateExpiry = date(data[4])
        self.QRCodeDateGenerated = date(data[6])
        self.data = data[-260][1]
        
        if (b_print): #si on souhaite afficher
            print("QR Code Issuer :", self.QRCodeIssuer)
            print("QR Code Expiry :", self.QRCodeDateExpiry)
            print("QR Code Generated :", self.QRCodeDateGenerated)
            self.QRcodePrint(data[-260][1], glb_schema['properties'])
            self.PassPrintData()
            
        self.QRcodeGetData()
     
    #affiche les données de manière officiele
    def QRcodePrint(self,data, schema, level=0):
        
        for key, value in data.items():
            description = schema[key].get('title') or schema[key].get('description') or key
            description, _, _ = description.partition(' - ')
            #print(value)
            if type(value) is dict:
                print('  '*level, description)
                _, _, sch_ref = schema[key]['$ref'].rpartition('/')
                self.QRcodePrint(value, glb_schema['$defs'][sch_ref]['properties'], level+1)
            elif type(value) is list:
                print('  '*level, description)
                _, _, sch_ref = schema[key]['items']['$ref'].rpartition('/')
                for v in value:
                    self.QRcodePrint(v, glb_schema['$defs'][sch_ref]['properties'], level+1)
            else: # value is scalar
                print('  '*level, description, ':', value) 
        
    #affiche les données telles qu'elles sont écrites 
    def PassPrintData(self): 
        for key, value in self.data.items():
            if type(value) is dict:
                for keydic, valuedic in value.items():
                    print(key,'/',keydic,':',valuedic)
                    
            elif type(value) is list:
                for i in range(0,len(value)):
                    for keydic, valuedic in value[0].items():
                        print(key,'/',keydic,':',valuedic)
                        
            else: #valeur normale
                print(key,':',value)
    #récupère les données du QR code et les stocks dans une variable
    def QRcodeGetData(self):
        for key, value in self.data.items():
            
            if key == 'nam':
                self.QRCodeGetDataKeyNam(value)
               
            if key == 'dob':
                self.Dob = value
                
            #if key == 'r':
            
            #if key == 't':
            if key == 'v' or key == 'r' or key =='t':
                self.GroupIdentifier = key
                self.QRCodeGetDataKeyGroupIdentifier(value)
                
    #return la chaine de caractères du pass décodé 
    def getData(self):
        return self.data
    
    def setData(self,d):
        self.data = d
            
    def afficherPassQRCodeInfos(self):
        print('-----------------------------------------')
        print('QRCode Issuer:',self.QRCodeIssuer)
        print('Date de délivration du QRCode:',self.QRCodeDateGenerated)
        print('Date expiration du QRCode:',self.QRCodeDateExpiry)
        
    def afficherPassNamInfos(self):
        print('--------------NOMS/PRENOMS---------------')
        print('Nom:',self.PersoneNameInformation._fn,'-','Nom standardisé:',self.PersoneNameInformation._fnt)
        print('Prénom:',self.PersoneNameInformation._gn,'-','Prénom standardisé:',self.PersoneNameInformation._gnt)
    
    def afficherGroupIdentifier(self):
        if self.GroupIdentifier == 'v':    
            self.afficherGroupIdentifierVaccination()
        if self.GroupIdentifier == 'r':    
            self.afficherGroupIdentifierRecovery()
        if self.GroupIdentifier == 't':    
            self.afficherGroupIdentifierTesting()
    
    #Affichage des informations liées au pass vaccinal
    def afficherGroupIdentifierVaccination(self):
        print('-------INFORMATIONS VACCINALES-----------')
        print('Virus:',self.byVaccination._tg,'-',self.byVaccination.getName_tg())
        print('Type Vaccin:',self.byVaccination._vp,'-',self.byVaccination.getName_vp())
        print('Production Medecinale:',self.byVaccination._mp,'-',self.byVaccination.getName_mp())
        print('Autorisation Marketing: ',self.byVaccination._ma,'-',self.byVaccination.getName_ma())
        print('Doses:',self.byVaccination._dn,'/',self.byVaccination._sd)
        print('Date de vaccination:',self.QRCodeDateGenerated)
        print('Pays: ',self.byVaccination._co)
        print('Certificate Issuer: ',self.byVaccination._is)
        print('Unique Certificate Identifier: ',self.byVaccination._ci)
    
    def afficherGroupIdentifierTesting(self):
        print('---------INFORMATIONS TEST----------------')
        print('Virus:',self.byTesting._tg,'-',self.byTesting.getName_tg())
        print('Type de test:',self.byTesting._tt,'-',self.byTesting.getName_tt())
        print('Resultat:',self.byTesting._tr,'-',self.byTesting.getName_tr())

    
    
    def afficherGroupIdentifierRecovery(self):
        print('------INFORMATIONS RETABLISSEMENT---------')
        
    def AfficherPass(self):
        
        self.afficherPassQRCodeInfos()
        self.afficherPassNamInfos()
        #self.afficherGroupIdentifierVaccination()
        self.afficherGroupIdentifier()
        
    def QRCodeGetDataKeyNam(self,value):
        for keydic, valuedic in value.items():
            if keydic == 'fn' : self.PersoneNameInformation._fn  = valuedic
            if keydic == 'fnt': self.PersoneNameInformation._fnt = valuedic
            if keydic == 'gn' : self.PersoneNameInformation._gn  = valuedic
            if keydic == 'gnt': self.PersoneNameInformation._gnt = valuedic    
            
    
    def QRCodeGetDataKeyGroupIdentifier(self,value):
        
        if self.GroupIdentifier == 'v':
            for keydic, valuedic in value[0].items():
                if keydic == 'tg' : self.byVaccination._tg = valuedic
                if keydic == 'vp' : self.byVaccination._vp = valuedic
                if keydic == 'mp' : self.byVaccination._mp = valuedic
                if keydic == 'ma' : self.byVaccination._ma = valuedic
                if keydic == 'dn' : self.byVaccination._dn = valuedic
                if keydic == 'sd' : self.byVaccination._sd = valuedic       
                if keydic == 'co' : self.byVaccination._co = valuedic
                if keydic == 'is' : self.byVaccination._is = valuedic
                if keydic == 'ci' : self.byVaccination._ci = valuedic
    
                        
        if self.GroupIdentifier == 'r':
            for keydic, valuedic in value[0].items():
                if keydic == 'tg' : self.byRecovery._tg = valuedic
                if keydic == 'fr' : self.byRecovery._fr = valuedic
                if keydic == 'co' : self.byRecovery._co = valuedic
                if keydic == 'is' : self.byRecovery._is = valuedic
                if keydic == 'df' : self.byRecovery._df = valuedic
                if keydic == 'du' : self.byRecovery._du = valuedic
                if keydic == 'ci' : self.byRecovery._ci = valuedic
            
        if self.GroupIdentifier == 't':
             for keydic, valuedic in value[0].items():
                if keydic == 'tg' : self.byTesting._tg = valuedic
                if keydic == 'tt' : self.byTesting._tt = valuedic
                if keydic == 'tn' : self.byTesting._tn = valuedic
                if keydic == 'ma' : self.byTesting._ma = valuedic
                if keydic == 'sc' : self.byTesting._sc = valuedic
                if keydic == 'tr' : self.byTesting._tr = valuedic
                if keydic == 'co' : self.byTesting._co = valuedic
                if keydic == 'is' : self.byTesting._is = valuedic
                if keydic == 'ci' : self.byTesting._ci = valuedic
     
    
    #set la date de validité du pass sanitaire
    def QRCodeDateValidity(self):
        #Récupération de la date de vaccination 
        QRCodeDate = datetime.strptime(self.QRCodeDateGenerated, "%Y-%m-%d %H:%M:%S")
        
        #si c'est un vaccin
        if self.GroupIdentifier == 'v':
            #si nb de doses requises + nb de doses sont les mêmes
            #on ajoute 7 jours
            self.QRCodeValidityDate = QRCodeDate + timedelta(days = 7)
            self.byVaccination._dt = str(self.QRCodeValidityDate) #str(validityDate)
            
        #si c'est un test 
        elif self.GroupIdentifier == 't':
            self.QRCodeValidityDate = QRCodeDate + timedelta(days = 1)
            self.byTesting._sc = str(self.QRCodeValidityDate)
        
        #si c'est un recovery
        elif self.GroupIdentifier == 'r':
            self.QRCodeValidityDate = QRCodeDate + timedelta(days = 7)
            self.byRecovery._fr = str(self.QRCodeValidityDate)
        else:
            print("ERROR")
        
    #set la date d'expiration du pass sanitaire
    def QRCodeDateExpiration(self):
        #QRCodeDate = datetime.strptime(self.QRCodeDateGenerated, "%Y-%m-%d %H:%M:%S")
        if self.GroupIdentifier == 'v':
            self.PassExpiryDate = self.QRCodeValidityDate + timedelta(days = 155) #5 mois
            
        if self.GroupIdentifier == 'r':
            self.PassExpiryDate = self.QRCodeValidityDate + timedelta(days = 186) #certification validity #6 mois
        
        if self.GroupIdentifier == 't':
            self.PassExpiryDate = self.QRCodeValidityDate + timedelta(days = 1) 
        
        return None
    
    #indique si le QR code est valide
    def QRCodeIsValid(self):
        
        self.QRCodeDateValidity() #définie la date de validité du QR code
        self.QRCodeDateExpiration() #définie la date d'expiration du QR code
        self.isValid = True
        
        if self.QRCodeValidityDate > datetime.now():
            self.isValid = False #Pass pas encore valide
        else: 
            if self.PassExpiryDate < datetime.now(): 
                    self.isValid = False #Le pass a expiré
            
            #Pour les tests
            if self.GroupIdentifier == 't':
                if self.byTesting._tr == '260373001': #resultat positif
                    self.isValid = False
            #Pour la vaccination
            if self.GroupIdentifier == 'v':
                if self.byVaccination._dn < self.byVaccination._sd : #il manque une dose dans le processus
                    self.isValid =  False
    
        return self.isValid
        #plus simple : verifie si la date de validité du QR code est antérieure à la date du jour
        
        #si le pass est lié un test
            #cas : négatif : 
                #cas :effectué moins de 48h
                    #self.isValid = true
                #cas : effectué il y a plus de 48h
                    #self.isValid = false
            #cas : positif 
                #self.isValid = false
        
        #si le pass est lié un vaccin
            #cas toutes les doses n'ont pas été faites :
                #self.isValid = false
            #cas toutes les doses ont été faites:
                #cas: vaccin 1  doses  : 
                   #si ca fait 28 jours après pour le vaccin johnson
                    #true 
                   #si ca fait 7 jours apres le vaccin suite à un covid au cours des 6 derniers mois 
                     #self.isvalid = true
                #cas vaccin en 2 doses ou 3 doses
                   #si ca fait 7 jours = true
        
        #si le pass est lié à un rétablissement
            #date de moins de 6 mois
                #self.isValid = true
            #cas : date de plus de 6 mois
                #self.isValid = false
            
        #else : self.isValid = false
        
        
            



class application:
    
    nb_personnes_max = None
    nb_personnes_now = 0
    
    def __init__(self,nb_psrn_max):
        self.nb_personnes_max = nb_psrn_max
    
    #ajouter une nouvelle personne
    def checkIndividu(self,Pass,indiv):
        Pass.readQRcode()
        Pass.decodeQRcodeData(False)#Decodage
        Pass.QRcodeGetData()#stockage des variables
        if(Pass.QRCodeIsValid()):
            if (Pass.PersoneNameInformation._fn == indiv.Nom) or (Pass.PersoneNameInformation._fnt == indiv.Nom):
                if (Pass.PersoneNameInformation._gn == indiv.Prenom) or (Pass.PersoneNameInformation._fnt == indiv.Prenom):
                    #vérifier la ate de naissance
                    print("La personne de la carte d'identité est la même que celle sur le pass")
                    return True
                else:
                    return False
                    print("La personne de la carte d'identité n'est pas la même que celle sur le pass")
            else:
                return False
                print("La personne de la carte d'identité n'est pas la même que celle sur le pass")

    def addIndividu(self,Pass,indiv):
        if (checkIndividu(Pass,indi)):
            if nb_personnes_max != nb_personnes_now:
                self.nb_personnes_now = self.nb_personnes_now + 1 
                #On pourrait ajouter un tableau d'individus
                return True
            else:
                print("Limite atteinte")
                return False
    
    #def removeIndividu()
    #def getNb_personnesNow()
        
    #retirer une personnne
    
    #verifier le nom de la personne


class personne:
    Nom = None
    Prenom = None
    Date_Naissance = None
    
    def __init__(self,Prenom,Nom,Date):
        self.Nom = Nom
        self.Prenom = Prenom
        self.Date_Naissance = Date
