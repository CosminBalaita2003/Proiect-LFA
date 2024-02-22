# Balaita Cosmin Neculai grupa 141
# Spataru Mara Andreea grupa 141

#dictionarul de camere l-am folosit pentru comanda look ca sa afiseze descrierea camerei in care ne aflam si camerele in care putem merge
dictionar_camere={}
dictionar_camere['Dining Room']=["A room with a large table filled with an everlasting feast.", "Entrance Hall, Treasury, Kitchen"]
dictionar_camere['Entrance Hall']=["The grand foyer of the Castle of Illusions.", "Armoury, Dining Room"]
dictionar_camere['Kitchen']=["A room pact with peculiar ingredients.", "Dining Room, Pantry"]
dictionar_camere['Armoury']=["A chamber filled with antiquated weapons and armour.","Entrance Hall, Throne Room, Treasury"]
dictionar_camere['Treasury']=["A glittering room overflowing with gold and gemstones.","Dining Room, Armoury, Wizard's Study, Library"]
dictionar_camere['Library']=["A vast repository of ancient and enchanted texts.", "Treasury, Secret Exit"]
dictionar_camere['Pantry']=["A storage area for the kitchen.", "Kitchen"]
dictionar_camere['Throne Room']=["The command center of the castle.", "Armoury, Wizard's Study"]
dictionar_camere["Wizard's Study"]=["A room teeming with mystical artifacts.", "Throne Room, Treasury, Secret Exit"]
dictionar_camere['Secret Exit']=["A hidden passage that leads out of the Castle of Illusions.", "Library, Wizard's Study"]


#dictionarul de obiecte l-am folosit pentru comanda take ca sa afiseze obiectele din camera in care ne aflam pe care le putem lua
dictionar_obiecte={}
dictionar_obiecte['Entrance Hall']=["key"]
dictionar_obiecte['Dining Room']=["invitation", "chef's hat"]
dictionar_obiecte['Kitchen']=["spoon"]
dictionar_obiecte['Armoury']=["sword", "crown"]
dictionar_obiecte['Treasury']=["ancient coin"]
dictionar_obiecte['Library']=["spell book"]
dictionar_obiecte["Wizard's Study"]=["magic wand"]
dictionar_obiecte['Pantry']=[]
dictionar_obiecte['Throne Room']=[]
dictionar_obiecte['Secret Exit']=[]

def load_file(file_name): #functia de load a fisierului
    f = open(file_name, "r")
    d = {} #dictionar ca la dfa
    ok = 0
    alfabet = [] #alfabetul LA-ului
    for line in f:
        line = line.strip()
        if line and line[0] != "#": #ignoram comentariile si liniile goale
            if line not in d and ok == 0: #luam capul de sectiune (Transitions, Sigma, States, ListAlphabet)
                d[line] = []
                section = line
                ok += 1
            else:
                if line == "End": #sarim peste sfarsitul sectiunilor
                    ok = 0
                else:
                    if section == "Sigma": #daca am ajuns in sectiunea sigma adaugam in dictionar valorile
                        d[section].append(line)
                    elif section == "States": #daca suntem la sectiunea states avem 3 cazuri
                        d[section].append(line) #daca lg e 1 atunci dam append direct starii
                    elif section == "ListAlphabet": #daca ajungem la sectiunea cu alfabetul listei, dam append caracterelor
                        alfabet.append(line)
                        d[section].append(line)
                    elif section == "Transitions": #daca ajungem la sectiunea tranzitiilor dam append intregii linii
                        d[section].append(line)
    f.close()
    return d, alfabet #returnam tot dictionarul, lista starilor de start, lista cu starile finale si alfabetul pt LA


def verify_file(d): #functia de verificare a fisierului
    valid = True #pornim presupunand ca e ok
    for t in d["Transitions"]:
        tranzitii = t.split(',')
        if tranzitii[0] not in d["States"]: #daca primul elem din tranzitii nu e in States returnam false
            valid = False
            return valid
        if tranzitii[1] not in d["Sigma"]: #daca al doilea elem din tranzitii nu e in Sigma returnam false
            valid = False
            return valid
        if tranzitii[2] not in d["ListAlphabet"]: #daca al 3 lea elem din tranzitii nu e in alfabetul listei returnam false
            valid = False
            return valid
        if tranzitii[3] not in d["States"]: #daca al 4 lea elem nu e in states returnam false ptc aia e starea in care noi va trb sa mergem
            valid = False
            return valid
    return valid #la sf daca totul a fost ok se va returna True


d, alfabet = load_file("Joc.txt") #apelam functia de incarcare a fisierului

currentroom = d['States'][0] #presupunem ca plecam din dining room

#Joc propriu zis:
while(True):

    comanda = input("Introduceti comanda:") #introducem comanda pt a juca
    comanda = comanda.split(' ',1) #dam split doar dupa primul spatiu pt cazul in care avem o comanda de genul go Entrance Hall unde trebuie sa 
    #pastram Entrance Hall impreuna
    if currentroom=="Secret Exit": #daca am ajuns la iesirea secreta am castigat si oprim jocul
        print("Ai ajuns la iesirea secreta, ai castigat!")
        break
    #print(comanda)
    if comanda[0] == "go": #conditii pentru comanda de a merge in alta camera
        for tranzitie in d["Transitions"]:
            tranzitie = tranzitie.split(',') #dam split elementelor din Transitions
            if tranzitie[0] == currentroom and comanda[0]==tranzitie[1] and tranzitie[3]==comanda[1]: #daca go se afla in tranzitie, si camera din tranzitie e camera in care ne aflam si camera in care vrem sa mergem e si ea in Transitions, putem merge mai departe
                # print("tranzitie1", tranzitie[1])
                # print("tranzitie3", tranzitie[3])
                # print("comanda1", comanda[1])
                
                if(tranzitie[2] in d["ListAlphabet"]): #daca avem deja obiectul necesar pt a trece in urmatoarea camera
                    currentroom = tranzitie[3] #schimbam camera curenta
                    print("Ai ajuns in",currentroom)
                    if currentroom=="Secret Exit": #verificam din nou sa nu fi ajuns la finalul jocului
                        break
        if currentroom=="Secret Exit": 
            print("Ai ajuns la iesirea secreta, ai castigat!")
            break
    elif comanda[0] == "look": #comanda de a te uita la detaliile camerei
        print("Esti in camera",currentroom)
        print("Descrierea camerei este: ", dictionar_camere[currentroom][0])
        print("Camerele in care poti merge sunt: ", dictionar_camere[currentroom][1])
    elif comanda[0] == "inventory":#comanda care afiseaza inventarul
        if len(d['ListAlphabet'])==0: #daca nu avem nmc in inventar
            print("Inventarul tau este gol")
        else:
            print("Inventarul tau este: ",d['ListAlphabet'])
    elif comanda[0] == "take": #comanda de a lua un obiect
        if comanda[1] not in d["ListAlphabet"] and comanda[1] in dictionar_obiecte[currentroom]: #daca nu il avem deja in inventar
            #si e un obiect pe care il putem lua din camera curenta
            d['ListAlphabet'].append(comanda[1]) #il adaugam la inventar
            print("Ai luat",comanda[1]) 
    elif comanda[0] == "drop": #comanda de a renunta la un obiect 
        if comanda[1] in d["ListAlphabet"]: #daca il avem in inventar
            print("Ai aruncat",comanda[1]) #il aruncam
            d['ListAlphabet'].remove(comanda[1]) #il scoatem din inventar
        else:
            print("Nu ai inca acest item") #daca vrem sa dam drop la ceva ce nu avem e clar ca nu putem deci error
    else:
        print("Comanda invalida")