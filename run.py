#!/usr/bin/env python
# coding: utf-8

# _________________________
# # Détection et vérification automatique du Pass Sanitaire par une approche de Deep Learning 
# 
# ## **IMT Lille Douai - UV PROJET**
# 
# ### Océane DELETREZ (Fi22) - Alexandre LEBAS (Fi22)
# 
# #### Janvier 2022
# _________________________

# # Fichiers du projets et explication des différentes classes du code
# 
# Concernant la partie lecture du pass sanitaire, nous avons plusieurs fichiers et dossiers : 
# 
# #### Dossier **GroupIdentifiers** :
# - Fichier byrecovery.ipynb
# contient la classe ‘recovery’ , représente les informations, méthodes et fonctions liées au pass sanitaire obtenu par rétablissement.
# - Fichier bytesting.ipynb
# contient la classe ‘testing’ , représente les informations, méthodes et fonctions liées au pass sanitaire obtenu suite à un test.
# - Fichier byvaccination.ipynb
# contient la classe vaccination’ , représente les informations, méthodes et fonctions liées au pass sanitaire obtenu suite à une vaccination.
# 
# #### Dossier **Tests Pass** :
# contient différents pass sanitaires pour les tests. Des pass valides, d’autres non valides. Certains sont des pass obtenus suite à une vaccination, d’autres à partir de tests PCR, d’autres suite à un rétablissement du covid. 
# 
# #### Fichier **file.ipynb** :
# contient une classe ‘file’, représentant un objet fichier (png, jpg …), contient le chemin d’accès et le type.
# 
# #### Fichier **greenpass.ipynb** :
# contient une classe 'greenpass' représentant l’objet pass sanitaire, contient toutes les fonctions et méthodes en lien avec le pass sanitaire.
# contient une classe ‘application’, représente le programme ainsi que toutes les fonctions et méthodes en lien avec la vérification des personnes et de leur pass, le comptage des personnes etc.
# contient une classe ‘personne’ représentant une personne, contient le nom, le prénom et la date de naissance
# 
# #### Fichier **html.ipynb** :
# Ce fichier a servi pour réaliser des tests sur une page Html. L’objectif était d’afficher les informations des pass sanitaires, les résultats concernant leur validité sur un onglet avec possibilité d’upload les pass.
# 
# #### Fichier **librairies.ipynb** :
# Ce fichier appelle toutes les librairies nécessaires au fonctionnement du projet. 
# #### Fichier **modules.ipynb** :
# Ce fichier installe le module “greenpass” officiel, permetant de traiter les pass sanitaires.
# #### Fichier **nam.ipynb** :
# Ce fichier  contient la classe ‘nam’, contenant le nom, prénom standardisé ou non d’une personne.
# #### Fichier **run.ipynb** :
#  Fichier principal, sert à lancer le programme, effectuer des tests.
# #### Fichier **libraries.ipynb** :
# Comme son nom l’indique, permet de charger les librairies
# #### Fichier **testsUnitaires.ipynb** :
# Contient la classe ‘testunits’, possède toutes les fonctions et méthodes utiles pour tester le programme et vérifier les résultats
# 

# ## Intégration des fichiers dans notre programme

# In[9]:


get_ipython().run_line_magic('run', 'greenpass.ipynb')


# Nous lançons le fichier **testsUnitaires.ipynb** qui nous permet de réaliser les tests, et nous créons un objet de la classe testUnits, nommé **t**

# In[10]:


get_ipython().run_line_magic('run', 'testsUnitaires.ipynb')
t = testsUnits()


# # Lecture des QR Codes

# Dans un premier temps, nous avons envisagé plusieurs hypothèses afin de lire le QR Code des pass sanitaires. 
# - La première hypothèse était de développer une fonction permettant d’ouvrir  la caméra et de lire le QR code en temps réel. Nous avons réussi à détecter les QR code en temps réel mais comme une de nos caméras n’était pas de bonne qualité (problème de calibrage), notre programme n’arrivait pas forcément à lire les données du QR code. Ainsi, nous avons opté pour une solution plus facile pour démarrer. Un exemple de code se trouve dans le fichier **Camera.ipynb**
# - La seconde hypothèse, celle sur laquelle nous avons finalement décidé de travailler, est de lire directement le QR code à partir d’un fichier de format “png”. 
# 
# Pour lire les QR Code, nous utilisons différentes fonctions :
# 
# - **greenpass:readQRcode()** : détecte et lit un QRcode sur l’image fournie à la création de l’objet greenpass. renvoie une chaine de caractères correspondant aux données cryptées. 
# - La fonction testsUnits:**checkReadingQRCode()** permet de tester la fonction greenpass:readQRcode()

# Pour les tests, nous avons mit plusieurs Pass au format png, dans la classe testUnits.

# In[11]:


#Lecture des QR CODE
t.checkReadingQRCode(t.PassVaccinalOceaneSansRappel)
t.checkReadingQRCode(t.PassVaccinalOceaneAvecRappel)
t.checkReadingQRCode(t.PassVaccinalPhilippeSansRappel)
t.checkReadingQRCode(t.PassTestOceane)
t.checkReadingQRCode(t.PassRetabEric)


# # Décodage du QR Code et affichage selon le schéma

# Comme nous l'avons vu ci-dessus, les données du QRCode sont cryptées. Nous avons cherché sur internet des documentations afin de comprendre le fonctionnement des pass sanitaires. 
# 
# Voici quelques liens que nous avons trouvés : 
# - https://gir.st/blog/greenpass.html
# - https://github.com/ehn-dcc-development/hcert-spec/blob/main/README.md
# - https://drive.google.com/file/d/1--f_0LkUmLXRxsng6iwypdAxP6ZO_AHz/view?usp=sharing
# - https://drive.google.com/file/d/1mM2cCxiuhfPqDHyPPNxfIdNtpY7ccP6W/view?usp=sharing
# 
# Pour décoder le QRCode, nous avons codé la fonction : greenpass:**decodeQRcodeData()**
# 
# Ces données une fois lisibles peuvent être sous cette forme : 
# 
# data =  {'v': [{'ci': 'URN:UVCI:01:FR:RTMWPU0RV5BW#3','co': 'FR','dn': 2,'dt': '2021-08-22','is': 'CNAM','ma': 'ORG-100030215','mp': 'EU/1/20/1528','sd': 2,'tg': '840539006','vp': 'J07BX03'}],'dob': '1998-06-12','nam': {'fn': 'DELETREZ', 'gn': 'OCEANE', 'fnt': 'DELETREZ', 'gnt': 'OCEANE'},'ver': '1.3.0'}
# 
# Elles suivent un schéma bien précis, expliqué dans les différentes documentations ci-dessus. Le schéma contient des clefs et valeurs.
# 
# ## Affichage du schéma du pass vaccinal

# Il y a 3 types de pass, vacinal, test et rétablissment qui se différencient à partir de la key **Groupidentifier** (v,t,r)

# In[12]:


sch = urlopen('https://raw.githubusercontent.com/ehn-dcc-development/ehn-dcc-schema/release/1.3.0/DCC.combined-schema.json')
glb_schema = json.load(sch)
glb_schema


# ## Décodage et Affichage du contenu du QR code selon le schema

# La fonction testUnits:**checkDecondingQRCode()** permet de tester si l'on arrive bien à décoder le QRCode et si on arrive bien à afficher les valeurs selon le schéma. 

# In[13]:


t.checkDecodingQRCode(t.PassVaccinalOceaneSansRappel) #Décodage des QR Code
t.checkDecodingQRCode(t.PassVaccinalOceaneAvecRappel)
t.checkDecodingQRCode(t.PassVaccinalPhilippeSansRappel)
t.checkDecodingQRCode(t.PassTestOceane)
t.checkDecodingQRCode(t.PassRetabEric)


# ## Stockage des valeurs du QRCode dans des variables de la classe **greenpass**

# In[14]:


t.checkStockerVariablesQRCode(t.PassVaccinalOceaneSansRappel) #Stockage des données dans des variables
t.checkStockerVariablesQRCode(t.PassVaccinalOceaneAvecRappel)
t.checkStockerVariablesQRCode(t.PassVaccinalPhilippeSansRappel)
t.checkStockerVariablesQRCode(t.PassTestOceane)
t.checkStockerVariablesQRCode(t.PassRetabEric)


# On affiche les group identifier, pour vérifier que l'on a bien le bon type de pass sanitaire : 

# In[15]:


print(t.PassRetabEric.GroupIdentifier)
print(t.PassVaccinalOceaneSansRappel.GroupIdentifier)
print(t.PassTestOceane.GroupIdentifier)


# ## Affichage du contenu du QRCode à partir des valeurs stockées dans des variables

# In[154]:


#Affichage du QR code à partir des variables
t.checkAfficherQRCode(t.PassVaccinalOceaneSansRappel)
t.checkAfficherQRCode(t.PassVaccinalOceaneAvecRappel)
t.checkAfficherQRCode(t.PassVaccinalPhilippeSansRappel)
t.checkAfficherQRCode(t.PassTestOceane)
t.checkAfficherQRCode(t.PassRetabEric)


# In[155]:


t.checkValidity(t.PassVaccinalOceaneSansRappel)
t.checkValidity(t.PassVaccinalOceaneAvecRappel)
t.checkValidity(t.PassVaccinalPhilippeSansRappel)
t.checkValidity(t.PassTestOceane) 
t.checkValidity(t.PassRetabEric)


# In[156]:


t.PassTest1 = t.newFakePassData(data1,"2021-08-29 14:33:20")
t.checkValidity(t.PassTest1)
t.PassTest2 = t.newFakePassData(data1,"2022-01-31 14:33:20")
t.checkValidity(t.PassTest2)
t.PassTest3 = t.newFakePassData(data1,"2021-05-31 14:33:20")
t.checkValidity(t.PassTest3)
t.PassTest4 = t.newFakePassData(data2,"2021-10-31 14:33:20")
t.checkValidity(t.PassTest4)


# In[157]:



if t.PassTest1.isValid == True : 
    print("Pass 1 Test valide")
else :
    print("Problème dans le code à corriger")
    
if t.PassTest2.isValid == False : 
    print("Pass 2 Test non valide,QR code pas encore valide")
else :
    print("Problème dans le code à corriger")
    
if t.PassTest3.isValid == False : 
    print("Pass 3 Test non valide,QR plus valide, delais de plus de 6 mois entre les doses")
else :
    print("Pass 3 Test Problème dans le code à corriger")
    
if t.PassTest4.isValid == False : 
    print("Pass 4 Test non valide, manque une dose")
else :
    print("Pass 4 Test Problème dans le code à corriger")


# In[158]:


a = application(10)
Oceane_DELETREZ = personne("OCEANE","DELETREZ","12/06/1998")


# In[159]:


a.checkIndividu(t.PassVaccinalOceaneAvecRappel,Oceane_DELETREZ)


# In[160]:


dataTest = {'v': [{'ci': 'URN:UVCI:01:FR:RTMWPU0RV5BW#3',
   'co': 'FR',
   'dn': 2,
   'dt': '2021-08-22',
   'is': 'CNAM',
   'ma': 'ORG-100030215',
   'mp': 'EU/1/20/1528',
   'sd': 2,
   'tg': '840539006',
   'vp': 'J07BX03'}],
 'dob': '1998-06-12',
 'nam': {'fn': 'DELEAAATREZ', 'gn': 'OCEANE', 'fnt': 'DELETREZ', 'gnt': 'OCEANE'},
 'ver': '1.3.0'}


# Faire une fonction qui crée des pass tests

# In[161]:


Pass_test1 = CovidPass("test","test")
Pass_test1.setData(dataTest)
print(Pass_test1.getData())
Pass_test1.QRcodeGetData()
Pass_test1.AfficherPass()


# In[149]:


Pass = CovidPass("TestsPass/OCEANE_DELETREZ_VAC.png","png")
PassAvecRappel = CovidPass("TestsPass/OCEANE_DELETREZ_VAC2.png","png")


# Schéma du pass Vaccinal : 
# 

# In[146]:


_dt


# In[ ]:





# In[ ]:





# In[ ]:




