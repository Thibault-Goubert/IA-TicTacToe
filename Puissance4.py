                ##IMPORT##
################################################################
import tkinter
import random
import numpy as np
import time

################################################################

                ##VARIABLES##
################################################################
Grille = [[0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0]]
          
GrilleDesScores =  [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]]

Scores = [0,0]
Lignes = len(Grille);
Colonnes = len(Grille[0]);
WinValue = 4;
canvas = None
ProfondeurSimulation = 1
################################################################

                                ##TESTS##
#################################################################################
def SetGrillesDesScores(Scores, Coups):
    for i in range(len(Coups)):
        GrilleDesScores[Coups[i][0]][Coups[i][1]] = Scores[i]
def InitGrilleDesScores():
    for x in range(Lignes):
        for y in range(Colonnes):
            GrilleDesScores[x][y] = Grille[x][y]
def GrillesDesScores(Scores, Coups):
    InitGrilleDesScores()
    SetGrillesDesScores(Scores, Coups)  
    for x in range(Lignes):
        print(GrilleDesScores[x])
    InitGrilleDesScores()
#################################################################################

                                ##UTILITY##
#################################################################################
def InitGrille():
    for x in range(Lignes):
        for y in range(Colonnes):
            Grille[x][y] = 0
def DisplayGrille():
    for x in range(Lignes):
        print(Grille[x])
def GetEmptySlots():
    Slots = []
    for y in range(0,Colonnes):
        for x in range(0,Lignes):
            if Grille[(Lignes-1)-x][y]==0:
                Slots.append([(Lignes-1)-x,y])
                break
    return Slots
def DisplayGameState():
    print("GameState:")
    DisplayGrille()
    print(GetEmptySlots(),"\n")
def IsWin(playerValue):
    isWin = False;
    nbAligne = 0;
    for x in range(0,Lignes):
        for y in range(0,Colonnes):
            #Horizontal          
            nbAligne = 0;
            if(x+WinValue-1 < Lignes):
                for k in range(WinValue):
                    if(Grille[x+k][y] == playerValue): 
                        nbAligne += 1
                    else: 
                        nbAligne = 0
                        break
                if(nbAligne==WinValue): return True
            #Vertical
            nbAligne = 0;
            if(y+WinValue-1 < Colonnes):
                for k in range(WinValue):
                    if(Grille[x][y+k] == playerValue): 
                        nbAligne += 1
                    else: 
                        nbAligne = 0
                        break
                if(nbAligne==WinValue): return True
            #Diagonale Droite                
            nbAligne = 0;
            if(x+(WinValue-1) < Lignes and y+(WinValue-1) < Colonnes):
                for k in range(WinValue):
                    if(Grille[x+k][y+k] == playerValue): 
                        nbAligne += 1
                    else: 
                        nbAligne = 0
                        break
                if(nbAligne==WinValue): return True
            #Diagonale Gauche                 
            nbAligne = 0;
            if(x+(WinValue-1) < Lignes and y-(WinValue-1) >= 0):
                for k in range(WinValue):
                    if(Grille[x+k][y-k] == playerValue): 
                        nbAligne += 1
                    else: 
                        nbAligne = 0
                        break
                if(nbAligne==WinValue): return True
    return isWin
def GetScore(nbAllyAligned, nbEnnemyAligned, score):
    if score<100 and nbAllyAligned==3 : score=100   #Favorise un placement de 4    
    elif score<50 and nbEnnemyAligned==3 : score=50 #Favorise un blocage de 4    
    elif score<30 and nbAllyAligned==2 : score=30   #Favorise un placement de 3    
    elif score<15 and nbEnnemyAligned==2 : score=15 #Favorise un blocage de 3   
    elif score<10 and nbAllyAligned==1 : score=10   #Favorise un placement de 2    
    elif score<5 and nbEnnemyAligned==1 : score=5   #Favorise un blocage de 2     
    return score
#################################################################################

                                ##METHOD##
#################################################################################
def Vertical(PlayerValue):
    Scores = []
    coups = GetEmptySlots()
    for coup in coups:
        Score=GrilleDesScores[coup[0]][coup[1]]
        nbAllyAligned=0
        nbEnnemyAligned=0
        last=0
        for k in range(WinValue):
            bas = coup[0]+k
            if(bas<Lignes):
                if Grille[bas][coup[1]] == PlayerValue:
                    if last == PlayerValue or last == 0:
                        last = PlayerValue
                        nbAllyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
                elif Grille[bas][coup[1]] != 0:
                    if last != PlayerValue:
                        if PlayerValue == 2:
                            last = 1
                        else:
                            last = 2
                        nbEnnemyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break

        Score = GetScore(nbAllyAligned, nbEnnemyAligned, Score)
        Scores.append(Score)
    index = Scores.index(np.amax(Scores))
    return coups[index], Scores[index]

def Horizontal(PlayerValue):
    Scores = []
    coups = GetEmptySlots()
    for coup in coups:
        Score=GrilleDesScores[coup[0]][coup[1]]
        for k in range(WinValue):
            nbAllyAligned=0
            nbEnnemyAligned=0
            last=0
            gauche = coup[1]-k
            if( gauche>=0 and gauche+(WinValue-1)<Colonnes):
                for l in range(WinValue):
                    if Grille[coup[0]][gauche+l] == PlayerValue:
                        if last == PlayerValue or last == 0:
                            last = PlayerValue
                            nbAllyAligned+=1
                        else:
                            nbAllyAligned = 0
                            nbEnnemyAligned = 0
                            break
                    elif Grille[coup[0]][gauche+l] != 0:
                        if last != PlayerValue:
                            if PlayerValue == 2:
                                last = 1
                            else:
                                last = 2
                            nbEnnemyAligned+=1
                        else:
                            nbAllyAligned = 0
                            nbEnnemyAligned = 0
                            break
                Score = GetScore(nbAllyAligned, nbEnnemyAligned, Score)
        Scores.append(Score)
    index = Scores.index(np.amax(Scores))
    return coups[index], Scores[index]

def DiagonaleGauche(PlayerValue):
    Scores = []
    coups = GetEmptySlots()
    for coup in coups:
        Score=GrilleDesScores[coup[0]][coup[1]]
        for k in range(WinValue):
            nbAllyAligned=0
            nbEnnemyAligned=0
            last=0

            bas = coup[0]+(WinValue-1)-k
            gauche = coup[1]-(WinValue-1)+k
            haut = bas-(WinValue-1)
            droite = gauche+(WinValue-1)

            if( (gauche>=0 and haut>=0) and (droite<Colonnes and bas<Lignes) ):
                for l in range(WinValue):
                    if Grille[bas-l][gauche+l] == PlayerValue:
                        if last == PlayerValue or last == 0:
                            last = PlayerValue
                            nbAllyAligned+=1
                        else:
                            nbAllyAligned = 0
                            nbEnnemyAligned = 0
                            break
                    elif Grille[bas-l][gauche+l] != 0:
                        if last != PlayerValue:
                            if PlayerValue == 2:
                                last = 1
                            else:
                                last = 2
                            nbEnnemyAligned+=1
                        else:
                            nbAllyAligned = 0
                            nbEnnemyAligned = 0
                            break
                Score = GetScore(nbAllyAligned, nbEnnemyAligned, Score)
        Scores.append(Score)
    index = Scores.index(np.amax(Scores))
    return coups[index], Scores[index]

def DiagonaleDroite(PlayerValue):
    Scores = []
    coups = GetEmptySlots()
    for coup in coups:
        Score=GrilleDesScores[coup[0]][coup[1]]
        for k in range(WinValue):
            nbAllyAligned=0
            nbEnnemyAligned=0
            last=0

            bas = coup[0]+(WinValue-1)-k
            droite = coup[1]+(WinValue-1)-k
            haut = bas-(WinValue-1)
            gauche = droite-(WinValue-1)+k

            if( (haut>=0 and droite<Colonnes) and (gauche>=0 and bas<Lignes) ):
                for l in range(WinValue):
                    if Grille[bas-l][droite-l] == PlayerValue:
                        if last == PlayerValue or last == 0:
                            last = PlayerValue
                            nbAllyAligned+=1
                        else:
                            nbAllyAligned = 0
                            nbEnnemyAligned = 0
                            break
                    elif Grille[bas-l][droite-l] != 0:
                        if last != PlayerValue:
                            if PlayerValue == 2:
                                last = 1
                            else:
                                last = 2
                            nbEnnemyAligned+=1
                        else:
                            nbAllyAligned = 0
                            nbEnnemyAligned = 0
                            break

                Score = GetScore(nbAllyAligned, nbEnnemyAligned, Score)
        Scores.append(Score)
    index = Scores.index(np.amax(Scores))
    return coups[index], Scores[index]

def GetBestCoup(PlayerValue):
    coups = []
    scores = []
    
    coups.append(Horizontal(PlayerValue)[0]) 
    scores.append(Horizontal(PlayerValue)[1])
    
    coups.append(Vertical(PlayerValue)[0]) 
    scores.append(Vertical(PlayerValue)[1])
    
    coups.append(DiagonaleDroite(PlayerValue)[0]) 
    scores.append(DiagonaleDroite(PlayerValue)[1])
    
    coups.append(DiagonaleGauche(PlayerValue)[0]) 
    scores.append(DiagonaleGauche(PlayerValue)[1])
    
    for i in range(len(scores)):
        print(scores[i],coups[i])
    
    GrillesDesScores(scores, coups)
    
    return coups[scores.index(np.amax(scores))]
    
                        ##TEST CALCUL SCORE COUP UNIQUE##
#################################################################################
def GetScoreU(nbAllyAligned, nbEnnemyAligned):
    if nbAllyAligned==3 : return 100   #Favorise un placement de 4    
    if nbEnnemyAligned==3 : return 50  #Favorise un blocage de 3   
    if nbAllyAligned==2 : return 30    #Favorise un placement de 3    
    if nbEnnemyAligned==2 : return 15  #Favorise un blocage de 2   
    if nbAllyAligned==1 : return 10    #Favorise un placement de 2   
    return 0

def GetEmplacementsJouables():
    Slots = []
    for y in range(0,Lignes):
        for x in range(0,Colonnes):
            if Grille[(Lignes-1)-x][y]==0:
                Slots.append([(Lignes-1)-x,y])
                break
    return Slots

def GetVerticalScore(coup,pvalue):
    scores=[]
    scores.append(0)
    for k in range(WinValue):
        nbAllyAligned=0
        nbEnnemyAligned=0
        last=0
        bas = coup[0]+k
        haut = bas-(WinValue-1)
        if(bas<Lignes and haut >=0):
            for l in range(WinValue):
                if Grille[haut+l][coup[1]] == pvalue:
                    if last == pvalue or last == 0:
                        last = pvalue
                        nbAllyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
                elif Grille[haut+l][coup[1]] != 0:
                    if last != pvalue:
                        if pvalue == 2: last = 1
                        else: last = 2
                        nbEnnemyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
            scores.append(GetScoreU(nbAllyAligned, nbEnnemyAligned))        
    return np.amax(scores)
    
def GetHorizontalScore(coup,pvalue):
    scores=[]
    scores.append(0)
    for k in range(WinValue):
        nbAllyAligned=0
        nbEnnemyAligned=0
        last=0
        gauche = coup[1]-k
        droite = gauche+(WinValue-1)
        if( gauche>=0 and droite<Colonnes):
            for l in range(WinValue):
                if Grille[coup[0]][gauche+l] == pvalue:
                    if last == pvalue or last == 0:
                        last = pvalue
                        nbAllyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
                elif Grille[coup[0]][gauche+l] != 0:
                    if last != pvalue:
                        if pvalue == 2:last = 1
                        else:last = 2
                        nbEnnemyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
            scores.append(GetScoreU(nbAllyAligned, nbEnnemyAligned))        
    return np.amax(scores)
    
def GetDiagonaleDroitScore(coup,pvalue):
    scores=[]
    scores.append(0)
    for k in range(WinValue):
        nbAllyAligned=0
        nbEnnemyAligned=0
        last=0

        bas = coup[0]+(WinValue-1)-k
        droite = coup[1]+(WinValue-1)-k
        haut = bas-(WinValue-1)
        gauche = droite-(WinValue-1)+k

        if( (haut>=0 and droite<Colonnes) and (gauche>=0 and bas<Lignes) ):
            for l in range(WinValue):
                if Grille[bas-l][droite-l] == pvalue:
                    if last == pvalue or last == 0:
                        last = pvalue
                        nbAllyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
                elif Grille[bas-l][droite-l] != 0:
                    if last != pvalue:
                        if pvalue == 2:last = 1
                        else:last = 2
                        nbEnnemyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
            scores.append(GetScoreU(nbAllyAligned, nbEnnemyAligned))        
    return np.amax(scores)

def GetDiagonalGaucheScore(coup,pvalue):
    scores=[]
    scores.append(0)
    for k in range(WinValue):
        nbAllyAligned=0
        nbEnnemyAligned=0
        last=0

        bas = coup[0]+(WinValue-1)-k
        gauche = coup[1]-(WinValue-1)+k
        haut = bas-(WinValue-1)
        droite = gauche+(WinValue-1)

        if( (haut>=0 and droite<Colonnes) and (gauche>=0 and bas<Lignes) ):
            for l in range(WinValue):
                if Grille[bas-l][gauche+l] == pvalue:
                    if last == pvalue or last == 0:
                        last = pvalue
                        nbAllyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
                elif Grille[bas-l][gauche+l] != 0:
                    if last != pvalue:
                        if pvalue == 2:last = 1
                        else:last = 2
                        nbEnnemyAligned+=1
                    else:
                        nbAllyAligned = 0
                        nbEnnemyAligned = 0
                        break
            scores.append(GetScoreU(nbAllyAligned, nbEnnemyAligned))        
    return np.amax(scores)
    
def CalculSlotScore(coup, pvalue):
    scores = []
    
    scores.append(GetVerticalScore(coup,pvalue))
    scores.append(GetHorizontalScore(coup,pvalue))
    scores.append(GetDiagonaleDroitScore(coup,pvalue))
    scores.append(GetDiagonalGaucheScore(coup,pvalue))
    
    return np.amax(scores)

def Note():
    if IsWin(2): return 500, None  #Profondeur
    if IsWin(1): return -500, None #Judicieux

    ScoresCoupsJouablesIA=[]     #Id=2 #Profondeur
    ScoresCoupsJouablesJoueur=[] #Id=1 #Judicieux
    
    CoupsJouables = GetEmplacementsJouables()
    if len(CoupsJouables)==0:
        return 0, None
    
    for coup in CoupsJouables:
        ScoresCoupsJouablesIA.append(CalculSlotScore(coup, 2)) #Profondeur
        ScoresCoupsJouablesJoueur.append(CalculSlotScore(coup, 1)) #Judicieux

    return np.amax(ScoresCoupsJouablesIA)-np.amax(ScoresCoupsJouablesJoueur), None


def IaProfondeur(ProfondeurExplore=0):
    L=GetEmptySlots()
    if ProfondeurExplore == ProfondeurSimulation or len(L)==0 or IsWin(1) or IsWin(2): 
        return Note()
    Scores = []
    for coup in L:
        Grille[coup[0]][coup[1]] = 2 #Profondeur
        Score, temp = IaJudicieux(ProfondeurExplore+1)
        Scores.append(Score)
        Grille[coup[0]][coup[1]] = 0
    
    max = np.amax(Scores)
    coups = []
    for i in range(len(Scores)):
        if Scores[i]==max:
            coups.append(L[i])
            
    coup = coups[random.randrange(len(coups))]
    return max, coup
    
def IaJudicieux(ProfondeurExplore): 
    L=GetEmptySlots()
    if len(L)==0 or IsWin(1) or IsWin(2): 
        return Note()
        
    Scores = []
    for coup in L:
        Grille[coup[0]][coup[1]] = 1 #Judicieux
        Score, temp = IaProfondeur(ProfondeurExplore)
        Scores.append(Score)
        Grille[coup[0]][coup[1]] = 0
        
    min = np.amin(Scores)
    coups = []
    for i in range(len(Scores)):
        if Scores[i]==min:
            coups.append(L[i])
            
    coup = coups[random.randrange(len(coups))]
    return min, coup
    
# def IaProfondeur(i = 0):
#     if  i == 2 or IsWin(1) or IsWin(2):
#         return  Note()
#     L = GetEmptySlots()
#     ScoresSim = {}
#     ScoresSimLsite = []
#     for K in L:
#         Grille[K[0]][K[1]] = 2
#         ScoreSim, nth = IaJudicieux(i+1)
#         ScoresSim.update({ScoreSim : K})
#         ScoresSimLsite.append((ScoreSim,K))
#         Grille[K[0]][K[1]] = 0
#     maxi = max(ScoresSim.keys())
#     Final = []
#     for elem in ScoresSimLsite:
#         if elem[0] == maxi:
#             Final.append(elem[1])
#     return maxi,Final[random.randrange(len(Final))]
# 
# def IaJudicieux(i):
#     if IsWin(1) or IsWin(2):
#         return Note()
#     L = GetEmptySlots()
#     ScoresSim = {}
#     ScoresSimLsite = []
#     for K in L:
#         Grille[K[0]][K[1]] = 1
#         ScoreSim, nth = IaProfondeur(i+1)
#         ScoresSim.update({ScoreSim : K})
#         ScoresSimLsite.append((ScoreSim,K))
#         Grille[K[0]][K[1]] = 0
#     mini = min(ScoresSim.keys())
#     Final = []
#     for elem in ScoresSimLsite:
#         if elem[0] == mini:
#             Final.append(elem[1])
#     return mini,Final[random.randrange(len(Final))]  


        
#################################################################################
def PlayIaVSIa():
    #IA Placements Judicieux
    CoupAJouer = GetBestCoup(1)
    print("CoupJudicieux",CoupAJouer)
    Grille[CoupAJouer[0]][CoupAJouer[1]] = 1 #Judicieux
    
    if(IsWin(1)):#Judicieux
        Scores[0] += 1
        Affiche(True)
        time.sleep(2)
        InitGrille()
    elif(len(GetEmptySlots())==0):
        InitGrille()
    else:#IA PLacement MiniMax en profondeur limitée
        CoupAJouer = IaProfondeur()
        print("CoupProfondeur",CoupAJouer)
        DisplayGrille()
        Grille[CoupAJouer[1][0]][CoupAJouer[1][1]] = 2 #Profondeur
        
        if(IsWin(2)): #Profondeur
            Scores[1] += 1
            Affiche(True)
            time.sleep(2)
            InitGrille()
        elif(len(GetEmptySlots())==0):
            InitGrille()
                            ##INTERFACE##
############################################################################

          
def Affiche(PartieGagnee = False):
        ## DOC canvas : http://tkinter.fdex.eu/doc/caw.html
        canvas.delete("all")
        
        for i in range(7):
            canvas.create_line(i*100,0,i*100,600,fill="blue", width="4" )
            canvas.create_line(0,i*100,700,i*100,fill="blue", width="4" )
            
        for x in range(Lignes):
            for y in range(Colonnes):
                xc = x * 100 
                yc = y * 100 
                if ( Grille[x][y] == 1):
                    canvas.create_oval(yc+10,xc+10,yc+90,xc+90,outline="red", width="4", fill="red" )
                if ( Grille[x][y] == 2):
                    canvas.create_oval(yc+10,xc+10,yc+90,xc+90,outline="yellow", width="4", fill="yellow" )
        
        msg = 'SCORES : ' + str(Scores[0]) + '-' + str(Scores[1])
        fillcoul = 'gray'
        if (PartieGagnee) : fillcoul = 'red'
        canvas.create_text(350,700, font=('Helvetica', 30), text = msg, fill=fillcoul)  
    
        canvas.update()   #force la mise a jour de la zone de dessin

def MouseClick(event):
    window.focus_set()
    x = event.x // 100 
    y = event.y // 100
    if ( (x<0) or (x>Colonnes-1) or (y<0) or (y>Lignes-1) ) : return
    Play(y,x)
    Affiche()

# fenetre
window = tkinter.Tk()
window.geometry("700x800") 
window.title('Mon Super Jeu')
window.protocol("WM_DELETE_WINDOW", lambda : window.destroy())
window.bind("<Button-1>", MouseClick)

#zone de dessin
WIDTH = 700
HEIGHT = 800
canvas = tkinter.Canvas(window, width=WIDTH , height=HEIGHT, bg="#000000")
canvas.place(x=0,y=0)
Affiche()


while True:               
    PlayIaVSIa() 
    Affiche()
 
# active la fenetre 
window.mainloop()


# def JoueurIA():
#     L=GetEmptySlots()
#     if IsWin(2): return 1
#     if IsWin(1): return -1
#     if len(L)==0: return 0
#     
#     Scores = []
#     for coup in L:
#         Grille[coup[0]][coup[1]] = 2
#         test = JoueurHumainSimule()
#         Score = 0 
#         if isinstance(test, int):
#             Score = test
#         else:
#             Score = test[0]
#         Scores.append(Score)
#         Grille[coup[0]][coup[1]] = 0
#     
#     return np.amax(Scores), L[Scores.index(np.amax(Scores))]
#     
# def JoueurHumainSimule():
#     L=GetEmptySlots()
#     if IsWin(2): return 1
#     if IsWin(1): return -1
#     if len(L)==0: return 0
#     
#     Scores = []
#     for coup in L:
#         Grille[coup[0]][coup[1]] = 1
#         test = JoueurIA()
#         Score = 0 
#         if isinstance(test, int):
#             Score = test
#         else:
#             Score = test[0]
#         Scores.append(Score)
#         Grille[coup[0]][coup[1]] = 0
#     
#     return np.amin(Scores), L[Scores.index(np.amin(Scores))]
# def Play(x,y):
#     if(Grille[x][y]==0):
#         es = GetEmptySlots()
#         print(es)
#         for s in es:
#             if s[1] == y:
#                 Grille[s[0]][s[1]] = 1
#                 print("Joueur Joue en:",s[0],s[1],"\n")
#                 if(IsWin(1)):
#                     Scores[0] += 1
#                     InitGrille()
#                 elif(len(GetEmptySlots())==0):
#                     InitGrille()
#                 else:#IA PLacement MiniMax en profondeur limitée
#                     CoupAJouer = JoueurIA()
#                     print("CoupAJouer",CoupAJouer)
#                     Grille[CoupAJouer[1][0]][CoupAJouer[1][1]] = 2
#                     Affiche()
#                     if(IsWin(2)):
#                         time.sleep(2)
#                         Scores[1] += 1
#                         InitGrille()
#                     elif(len(GetEmptySlots())==0):
#                         InitGrille()
#         DisplayGameState()