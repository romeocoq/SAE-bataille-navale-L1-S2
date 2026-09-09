def detecter_orientation(grille, i, j):
    """
    list[list[str]],int,int -> str
    vérifie si un bateau est à l'horizontale ou à la verticale sur la grille
    retourne 'h' pour horizontal, 'v' pour vertical.
    """
    if j + 1 < len(grille[i]) and grille[i][j] == grille[i][j+1]:
        return 'h'
    return 'v'

def generer_html(joueur, grille_joueur, grille_adverse,orientation_bateau,coords):
    """
    int,list[list[str]],list[list[str]],dict[str:str],list[list[tuple,int]] -> generer_tableau
    génère le fichier HTML pour un joueur
    """
    nom_fichier = f"joueur{joueur}.html"
    
    html = f"""<!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Bataille Navale - Joueur {joueur}</title>
        <link rel="stylesheet" href="main.css">
    </head>
    <body>
        <h1>Joueur {joueur}</h1>
        
        <div id="tableaux">
            <div id="joueur">
                {generer_tableau(grille_joueur, True, joueur,orientation_bateau,coords)[0]}
            </div>
            
            <div id="adverse">
                {generer_tableau(grille_adverse, False, joueur,orientation_bateau,coords)[0]}
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(html)
    
    return generer_tableau(grille_joueur, True, joueur,orientation_bateau,coords)

def generer_tableau(grille, visible, joueur,orientation_bateau,coords):
    """
    str,bool,int,dict[str:str],list[list[tuple,int]] -> (html,dict[str:str],list[list[tuple,int]])
    génère un tableau HTML à partir d'une grille et retourne le code html, l'orientation des bateaux et leurs coordonées sur la grille
    """
    html = '<div class="plateau">'
    if visible:
        html+='<div class="titre" style="grid-column: span 10; color:blue;"><h2>Votre plateau</h2></div>'
    else:
        html+='<div class="titre" style="grid-column: span 10; color:red;"><h2>Plateau adverse</h2></div>'
    
    dict_tailles = {"C":0,"B":0,"D":0,"P":0,"S":0}
    
    if coords == []:
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                if grille[i][j]=="C" or grille[i][j]=="B" or grille[i][j]=="D" or grille[i][j]=="P" or grille[i][j]=="S" :
                    if [(i,j),dict_tailles[grille[i][j]]] not in coords:
                        coords.append([(i,j),dict_tailles[grille[i][j]]])
                    dict_tailles[grille[i][j]]+=1
    
    else:
        for i in range(len(grille)):
            for j in range(len(grille[i])):
                if grille[i][j]=="C" or grille[i][j]=="B" or grille[i][j]=="D" or grille[i][j]=="P" or grille[i][j]=="S" :
                    dict_tailles[grille[i][j]]+=1
            
    for i,ligne in enumerate(grille):
        for j,case in enumerate(ligne):
            
            if not visible and case=="?":
                img = "fogofwar.png"
            elif case == ".":
                img="free.png"
            elif case == "H" or case=="x":
                img = "fire.png"
            elif case == "M":
                img = "missed.png"
            elif visible:
                if not case in orientation_bateau:
                    orientation_bateau[case] = detecter_orientation(grille,i,j)
                orientation = orientation_bateau[case]
                taille = dict_tailles[case]
                bateau = f"{case}_{orientation}"
                for k in range(len(coords)):
                    if coords[k][0]==(i,j):
                        num=coords[k][1]
                img = f"{num}.png"
                    
                html += f'<div class="case" style="grid-column-start:{j+1}; grid-row-start:{i+2}; position:relative;">'
                html += f'<img src="./images/{bateau}/{img}" alt="{case}">'
                html += '</div>'
                    
                continue


            html += f'<div class="case" style="grid-column-start:{j+1};grid-row-start:{i+2};">'
            html += f'<img src="./images/{img}" alt="{case}">'
            html += "</div>"
    html += "</div>"
    
    return (html,orientation_bateau,coords)
