#!/usr/bin/env python
# coding: utf-8

# In[17]:


#%run greenpass.ipynb


# In[20]:


def createPassForTest(dataTest):
    p = CovidPass("test","test")
    p.setData(dataTest)
    p.QRcodeGetData()
    p.AfficherPass()
    return p


# In[1]:


class testsUnits:
    
    PassVaccinalOceaneSansRappel = CovidPass("TestsPass/OCEANE_DELETREZ_VAC.png","png")
    PassVaccinalOceaneAvecRappel = CovidPass("TestsPass/OCEANE_DELETREZ_VAC2.png","png")
    PassVaccinalPhilippeSansRappel = CovidPass("TestsPass/PHILIPPE_VAC.png","png")
    PassTestOceane = CovidPass("TestsPass/OCEANE_TEST.png","png")
    PassRetabEric = CovidPass("TestsPass/ERIC_RETAB.png","png")
    
    def __init__(self):
        None
        
    def checkReadingQRCode(self,greenPass):
        print("Lecture du QR code fournit en params....")  
        print("----------------------------------------------------------------------")
        print(greenPass.readQRcode())
        print("----------------------------------------------------------------------")
    
    def checkDecodingQRCode(self,greenPass):
        greenPass.readQRcode() #Lecture

        print("Affichage selon le schéma ....")  
        print("----------------------------------------------------------------------")
        greenPass.decodeQRcodeData(True)#Decodage
        print("----------------------------------------------------------------------")
        
        #print("Affichage brut des données....")  
        #print("----------------------------------------------------------------------")
        #greenPass.getData()
        #print("----------------------------------------------------------------------")
       
        print("Affichage des valeurs et des clefs....")  
        print("----------------------------------------------------------------------")
        greenPass.PassPrintData()
        print("----------------------------------------------------------------------")
        
    def checkStockerVariablesQRCode(self,greenPass):
        greenPass.readQRcode() #Lecture
        #greenPass.decodeQRcodeData()#Decodage
        print("Obtention et stockage des valeurs du QR code....")  
        print("----------------------------------------------------------------------")
        greenPass.QRcodeGetData()
        print("----------------------------------------------------------------------")
        
    def checkAfficherQRCode(self,greenPass):   
        #greenPass.readQRcode() #Lecture
        #greenPass.decodeQRcodeData()#Decodage
        greenPass.QRcodeGetData()#stockage des variables
        print("Affichage du Pass Sanitaire....")  
        print("----------------------------------------------------------------------")
        greenPass.AfficherPass()
        print("----------------------------------------------------------------------")
        

    def checkValidity(self,greenPass):
        print("Affichage de la validité du pass Sanitaire....")  
        print("----------------------------------------------------------------------")
        #greenPass.readQRcode()
        #greenPass.decodeQRcodeData()#Decodage
        greenPass.QRcodeGetData()#stockage des variables
        greenPass.QRCodeDateValidity()
        print("Date de validité du QRCode" , str(greenPass.QRCodeValidityDate)) ##Affichage de la date de validité du QR Code
        greenPass.QRCodeIsValid()
        print("Pass Valid : ", greenPass.isValid)
        print("----------------------------------------------------------------------")
        
    def newFakePassData(self,dataTest,date):
        p = CovidPass("test","test")
        p.QRCodeDateGenerated = date
        p.setData(dataTest)
        p.QRcodeGetData()
        p.getData()
        p.AfficherPass()
        return p






# In[1]:


data1 =  {'v': [{'ci': 'URN:UVCI:01:FR:RTMWPU0RV5BW#3','co': 'FR','dn': 2,'dt': '2021-08-22','is': 'CNAM','ma': 'ORG-100030215','mp': 'EU/1/20/1528','sd': 2,'tg': '840539006','vp': 'J07BX03'}],'dob': '1998-06-12','nam': {'fn': 'DELEAAATREZ', 'gn': 'OCEANE', 'fnt': 'DELETREZ', 'gnt': 'OCEANE'},'ver': '1.3.0'}
data2 =  {'v': [{'ci': 'URN:UVCI:01:FR:RTMWPU0RV5BW#3','co': 'FR','dn': 2,'dt': '2021-08-22','is': 'CNAM','ma': 'ORG-100030215','mp': 'EU/1/20/1528','sd': 3,'tg': '840539006','vp': 'J07BX03'}],'dob': '1998-06-12','nam': {'fn': 'DELEAAATREZ', 'gn': 'OCEANE', 'fnt': 'DELETREZ', 'gnt': 'OCEANE'},'ver': '1.3.0'}


# In[ ]:





# In[37]:





# In[ ]:





# In[ ]:




