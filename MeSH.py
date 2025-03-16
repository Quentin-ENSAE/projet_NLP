from collections import defaultdict
from typing import List, Dict, Set

# MeSH.py
def Hello():
    return "Hello from MeSH!"


def list_to_dict(mesh_list: List[str]) -> Dict[str, Set[str]]:
    """
    Transforme une liste de termes MeSH en un dictionnaire où les clés sont les qualificateurs
    et les valeurs sont des ensembles de termes MeSH associés.
    
    Paramètres:
    mesh_list (List[str]): Liste de termes MeSH sous la forme 'Terme MeSH / Qualificateur'

    Retourne:
    Dict[str, Set[str]]: Dictionnaire avec les qualificateurs en clés et les ensembles de termes MeSH en valeurs.
    """
    mesh_dict = defaultdict(set)  # Dictionnaire avec ensemble pour éviter les doublons
    
    for entry in mesh_list:
        parts = entry.split(" / ")  # Séparer le terme MeSH et le qualificateur
        
        if len(parts) == 2:
            term, qualifier = parts
        else:
            term, qualifier = parts[0], "No Qualifier"

        mesh_dict[qualifier].add(term)  # Ajouter le terme sous le bon qualificateur
    
    return dict(mesh_dict)


def recherche_descripteur(racine, recherche, type_recherche='nom'):
    """
    Recherche un descripteur MeSH dans un arbre XML en fonction de l'identifiant,
    du nom du descripteur ou d'un numéro MeSH.

    Args:
        racine (xml.etree.ElementTree.Element): La racine de l'arbre XML MeSH.
        recherche (str): La valeur à rechercher (identifiant, nom ou numéro MeSH).
        type_recherche (str): Le type de recherche ('identifiant', 'nom', 'numero_mesh').

    Returns:
        dict: Contient l'identifiant, le nom et les numéros MeSH associés du descripteur trouvé.
              Retourne None si aucun descripteur n'est trouvé.
    """
    for descripteur in racine.findall('DescriptorRecord'):
        ui = descripteur.find('DescriptorUI').text
        nom = descripteur.find('DescriptorName/String').text
        numeros_mesh = [tree_number.text for tree_number in descripteur.findall('TreeNumberList/TreeNumber')]

        if type_recherche == 'identifiant' and ui == recherche:
            return {
                'identifiant': ui,
                'nom': nom,
                'numeros_mesh': numeros_mesh
            }
        elif type_recherche == 'nom' and nom.lower() == recherche.lower():
            return {
                'identifiant': ui,
                'nom': nom,
                'numeros_mesh': numeros_mesh
            }
        elif type_recherche == 'numero_mesh' and recherche in numeros_mesh:
            return {
                'identifiant': ui,
                'nom': nom,
                'numeros_mesh': numeros_mesh
            }

    return None


def resultats_descripteur(resultat):
    """
    Affiche les informations d'un descripteur MeSH.

    Args:
        resultat (dict): Dictionnaire contenant les informations du descripteur.
    """
    if resultat:
        print(f"Identifiant : {resultat['identifiant']}")
        print(f"Nom du descripteur : {resultat['nom']}")
        if resultat['numeros_mesh']:
            print("Numéros MeSH associés :")
            for numero in resultat['numeros_mesh']:
                print(f" - {numero}")
        else:
            print("Aucun numéro MeSH associé trouvé.")
    else:
        print("Descripteur non trouvé.")



def categorie_haute(tree_number, racine):
    """
    Recherche et retourne la catégorie de plus haut niveau associée à un numéro MeSH.

    Args:
    - tree_number (str): Le numéro MeSH à rechercher (par ex. "C10").
    - racine: L'élément racine de l'arbre XML chargé.

    Retourne:
    - La catégorie la plus haute (str) ou None si aucune correspondance n'est trouvée.
    """
    for descripteur in racine.findall('DescriptorRecord'):
        tree_numbers = descripteur.findall('TreeNumberList/TreeNumber')
        for number in tree_numbers:
            if number.text == tree_number:  # Recherche exacte du numéro
                return descripteur.find('DescriptorName/String').text

    print(f"Aucune catégorie trouvée pour le numéro {tree_number}.")
    return None


def distance_categorie(maladie1, maladie2, racine):
    """
    Calcule la distance entre deux maladies MeSH basées sur leurs Tree Numbers.

    Args:
        maladie1 (str): Nom ou identifiant de la première maladie.
        maladie2 (str): Nom ou identifiant de la seconde maladie.
        racine (xml.etree.ElementTree.Element): Racine de l'arbre XML MeSH.

    Returns:
        float: Distance calculée entre les deux maladies.
    """
    # Recherche des descripteurs pour les deux maladies
    descripteur1 = recherche_descripteur(racine, maladie1, type_recherche='nom')
    descripteur2 = recherche_descripteur(racine, maladie2, type_recherche='nom')

    if not descripteur1 or not descripteur2:
        print("Une ou les deux maladies n'ont pas été trouvées.")
        return float('inf')

    # Récupération des Tree Numbers
    tree_numbers1 = descripteur1['numeros_mesh']
    tree_numbers2 = descripteur2['numeros_mesh']

    if not tree_numbers1 or not tree_numbers2:
        print("Une ou les deux maladies n'ont pas de Tree Numbers associés.")
        return float('inf')

    # Trouver le plus haut ancêtre commun
    min_distance = float('inf')
    for tree1 in tree_numbers1:
        for tree2 in tree_numbers2:
            ancetre_communs = ancetre_commun(tree1, tree2)
            if ancetre_communs:
                distance = (len(tree1.split('.')) - len(ancetre_communs.split('.'))) + \
                           (len(tree2.split('.')) - len(ancetre_communs.split('.')))
                min_distance = min(min_distance, distance)

    return min_distance if min_distance != float('inf') else 10


def ancetre_commun(tree1, tree2):
    """
    Trouve le plus haut ancêtre commun entre deux Tree Numbers.

    Args:
        tree1 (str): Premier Tree Number.
        tree2 (str): Deuxième Tree Number.

    Returns:
        str: L'ancêtre commun le plus élevé ou None s'il n'y a pas de correspondance.
    """
    segments1 = tree1.split('.')
    segments2 = tree2.split('.')
    ancetre = []

    for seg1, seg2 in zip(segments1, segments2):
        if seg1 == seg2:
            ancetre.append(seg1)
        else:
            break

    return '.'.join(ancetre) if ancetre else None