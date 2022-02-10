#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class recovery:
    _tg = None #Disease of agent
    _fr = None #Date of the holder's first positive test result
    _co = None #Country
    _is = None #Certificate issuer
    _df = None #Certificate valid forme
    _du = None #Certificate valid until
    _ci = None #Certificate unique identifier
    
    """
    Fonction:'getName_tg'
        Affiche la maladie à partir de son code, stocké dans la variable '_tg'. 
             Paramètres requis : aucun
             Sortie retournée  : une chaine de caractères
    """
    def getName_tg(self):
        if   self._tg == '840539006':         return 'COVID-19'
        else:                                 return 'CODE INCONNU'
    

