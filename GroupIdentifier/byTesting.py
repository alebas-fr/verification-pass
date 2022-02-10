#!/usr/bin/env python
# coding: utf-8

# In[1]:


class testing:
    _tg = None #Disease of agent targeted
    _tt = None #The type of test
    _tn = None #Test name 
    _ma = None #Test device identifier
    _sc = None #date and time
    _tr = None #result of the test
    _co = None #Pays
    _is = None #Certificate issuer
    _ci = None #Unique certificate identifier
    
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
    Fonction:'getName_tt'
        Affiche le type de test, stocké dans la variable '_tt'. 
             Paramètres requis : aucun
             Sortie retournée  : une chaine de caractères
    """
    def getName_tt(self):
        if self._tt == 'LP6464-4' :            return 'Nucleic acid amplification with probe detection'
        if self._tt == 'LP217198-3':           return 'Rapid immunoassay'
        else:                                 return 'CODE INCONNU'
        
    def getName_tr(self):
        if self._tr == '260415000':            return 'Not detected'
        if self._tr == '260373001':            return 'Detected'
        else:                                 return 'CODE INCONNU'

        

