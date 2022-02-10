#!/usr/bin/env python
# coding: utf-8

# In[8]:


"""
Classe 'vaccination'
    Représente les informations et méthodes liées au vaccin
"""   

class vaccination:
    """
    Variables
    """
    _tg = None #Disease or agent targeted
    _vp = None #Type of vaccine
    _mp = None #Medicinal production
    _ma = None #Marketing authorisation holder or manufacturer
    _dn = None #Nombre de doses réalisées
    _sd = None #Nombre de doses totales à faire dans le processus
    _dt = None #Date de vaccination
    _co = None #Pays de vaccination
    _is = None #Certificate issuer
    _ci = None #Unique Certificate identifier
    
    """
    Fonction:'getName_tg'
        Affiche la maladie à partir de son code, stocké dans la variable '_tg'. 
             Paramètres requis : aucun
             Sortie retournée  : une chaine de caractères
    """
    def getName_tg(self):
        if   self._tg == '840539006':         return 'COVID-19'
        else:                                 return 'CODE INCONNU'
    
    """
    Fonction:'getName_vp'
        Affiche le type de vaccin à partir de son code, stocké dans la variable '_vp'. 
             Paramètres requis : aucun
             Sortie retournée  : une chaine de caractères 
    """
    def getName_vp(self):
        if   self._vp == '1119305005':        return 'SARS-CoV-2 antigen vaccine'
        elif self._vp == '1119349007':        return 'SARS-CoV-2 mRNA vaccine'
        elif self._vp == 'J07BX03':           return 'covid-19 vaccines'
        else:                                 return 'CODE INCONNU'
    
    """
    Fonction:'getName_mp'
        Affiche la production médecinale à partir de son code, stocké dans la variable '_mp'. 
             Paramètres requis : aucun
             Sortie retournée  : une chaine de caractères
    """    
    def getName_mp(self):
        if   self._mp == 'EU/1/20/1528':        return 'Cominarty'
        elif self._mp == 'EU/1/20/1507':        return 'COVID-19 Vaccine Moderna'
        elif self._mp == 'EU/1/21/1529':        return 'Vaxzevria'
        elif self._mp == 'EU/1/20/1525':        return 'COVID-19 Vaccine Janssen' 
        elif self._mp == 'CVnCoV'      :        return 'CVnCoV'
        elif self._mp == 'NVX-CoV2373' :        return 'NVX-CoV2373'
        elif self._mp == 'Sputnik-V'   :        return 'Sputnik V'
        elif self._mp == 'Convidecia'  :        return 'Convidecia'
        elif self._mp == 'EpiVacCoron' :        return 'EpiVacCorona'
        elif self._mp == 'BBIBP-CorV'  :        return 'BBIBP-CorV'
        elif self._mp == 'Inactivated-SARS-CoV-2-Vero-Cell': return 'Inactivated SARSCoV-2 (Vero Cell)'
        elif self._mp == 'CoronaVac'   :        return 'CoronaVac'
        elif self._mp == 'Covaxin'     :        return 'Covaxin (also known as BBV152 A, B, C)'
        else:                                   return 'CODE INCONNU'
    
    """
    Fonction:'getName_ma'
        Affiche le titulaire de l'autorisation de mise sur le marché ou le fabricant. 
             Paramètres requis : aucun
             Sortie retournée  : une chaine de caractères
    """   
    def getName_ma(self):
        if   self._ma == 'ORG-100001699' :      return 'AstraZeneca AB'
        elif self._ma == 'ORG-100030215' :      return 'Biontech Manufacturing GmbH'
        elif self._ma == 'ORG-100001417' :      return 'Janssen-Cilag International'
        elif self._ma == 'ORG-100031184' :      return 'Moderna Biotech Spain S.L.'
        elif self._ma == 'ORG-100006270' :      return 'Curevac AG'
        elif self._ma == 'ORG-100013793' :      return 'CanSino Biologics'
        elif self._ma == 'ORG-100020693' :      return 'China Sinopharm International Corp. - Beijing location'
        elif self._ma == 'ORG-100010771' :      return 'Sinopharm Weiqida Europe Pharmaceutical s.r.o. - Prague location'
        elif self._ma == 'ORG-100024420' :      return 'Sinopharm Zhijun (Shenzhen) Pharmaceutical Co. Ltd. -Shenzhen location'
        elif self._ma == 'ORG-100032020' :      return 'Novavax CZ AS'
        elif self._ma == 'Gamaleya-Research-Institute': return 'Gamaleya Research Institute'
        elif self._ma == 'Vector-Institute':     return 'Vector Institute'
        elif self._ma == 'Sinovac-Biotech' :    return 'Sinovac Biotech'
        elif self._ma == 'Bharat-Biotech' :     return 'Bharat Biotech'
        

        
        



