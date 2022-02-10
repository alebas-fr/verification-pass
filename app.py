from turtle import color
import cv2
import numpy as np
import pyzbar
from pyzbar.pyzbar import decode
import time
import greenpass

# Exécuter ce code seulement si on lance le fichier
if __name__ == "__main__":
    i=0
    # Ouvrir la caméra et définir la résolution
    cap = cv2.VideoCapture(0)
    currentFrame = 0
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float
    detector = cv2.QRCodeDetector()
    waiting = False # Nous permet d'attendre pour qu'on affiche un pass sanitaire valide
    validity_show = None # Image à afficher pour dire si le pass est valide ou non.

    # Caractéristiques du texte à afficher sur l'image pour donner des infos sur la personne
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (255,0,0)
    thickness = 3
    nombre_de_pass_valide = 0

    # Lire la caméra
    while cap.isOpened():
        ret,frame = cap.read()
        # Trouver les qrcode dans l'image
        for barcode in decode(frame):
            if barcode.type != "QRCODE":
                #print("[-] Not a qrcode", file=sys.stderr)
                pass
            # Récupérer les données du QRCODE et afficher un rectangle autour du QRCODE
            rect = barcode.rect
            pt1 = (rect.left, rect.top)
            pt2 = (rect.left + rect.width, rect.top + rect.height)
            data = barcode.data
            # Mettre les données dans un objet greenpass
            greenpass_to_decode = greenpass.CovidPass(QRCodedata=data)
            greenpass_to_decode.decodeQRcodeData()
            greenpass_to_decode.QRcodeGetData()
            # Récupérer les données nécessaires
            valid = greenpass_to_decode.QRCodeIsValid() # Si le pass est valide ou non 
            nom = greenpass_to_decode.PersoneNameInformation._fnt # Le nom de la personne
            prenom = greenpass_to_decode.PersoneNameInformation._gnt # Le prénom de la personne
            dob = greenpass_to_decode.Dob # La date de naissance
            if valid:
                nombre_de_pass_valide+=1
                validity_show = cv2.imread("PassValide.png")
            else:
                validity_show = cv2.imread("PassInvalide.png")
            # Afficher les infos sur une fenêtre 
            cv2.putText(validity_show,nom+" "+prenom,(50,430),font,font_scale,color,thickness)
            cv2.putText(validity_show,dob,(50,500),font,font_scale,color,thickness)
            frame = cv2.rectangle(frame,pt1,pt2,(255,0,0),thickness=2)
            waiting = True
            cv2.imshow("Valid",validity_show)
        cv2.imshow("Frame",frame)
        """
        Si on a choisi d'afficher des infos uniquement sur la validité, le nom, prénom et date de naissance
        c'est parce que légalement nous n'avons pas le droit d'afficher des infos sur la vaccination, le test
        ou même la guérison du covid (ce sont des données personnels).
        """
        if cv2.waitKey(10) & 0xFF == ord('q'): # Si jamais on demande la fermeture du programme
            break
        if waiting: # Attendre 10 secondes pour bloquer la lecture de la caméra et éviter de lire deux fois le même pass mais aussi pour afficher la validité du pass. 
            time_begin = time.time()
            while time.time()-time_begin<10:
                i+=1
            cv2.destroyWindow("Valid")
            waiting=False
            i=0
    cap.release()
    cv2.destroyAllWindows()