from collections import defaultdict
from typing import List, Dict, Set
import xml.etree.ElementTree as ET


# MeSH.py
def Hello():
    return "Hello from MeSH!"


# Fonction pour analyser un fichier XML
def chargement_arbre_mesh(chemin):
    try:
        arbre = ET.parse(chemin)
        racine = arbre.getroot()
        print(f"Fichier XML analysé avec succès : {chemin}")
        return racine
    except ET.ParseError as e:
        print(f"Erreur lors de l'analyse du fichier XML : {e}")
    except FileNotFoundError:
        print(f"Le fichier spécifié est introuvable : {chemin}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")


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


def recherche_descripteur(racine, recherche, type_recherche='nom', ignore_case=True, verbose=False, format_reponse=None):
    """
    Recherche un descripteur MeSH dans un arbre XML selon l'identifiant, le nom ou le numéro MeSH.

    Args:
        racine (xml.etree.ElementTree.Element): La racine de l'arbre XML MeSH.
        recherche (str): La valeur à rechercher (identifiant, nom ou numéro MeSH).
        type_recherche (str): Type de recherche :
            - 'identifiant' : recherche par identifiant MeSH (ex : D012345)
            - 'nom' : recherche par nom exact du descripteur (ex : 'Asthma')
            - 'numero_mesh' : recherche par numéro MeSH exact (ex : 'C08.360.480')
        ignore_case (bool): Si True, la recherche par nom est insensible à la casse.
        verbose (bool): Si True, affiche un message si aucun résultat n'est trouvé.
        format_reponse (str, optionnel): Spécifie le format de réponse désiré parmi :
            - 'identifiant' : retourne uniquement l'identifiant du descripteur
            - 'nom' : retourne uniquement le nom du descripteur
            - 'numero_mesh' : retourne uniquement les numéros MeSH associés

    Returns:
        dict, str, list, or None:
            Si format_reponse est spécifié, retourne uniquement la donnée demandée.
            Sinon, retourne un dictionnaire complet du descripteur.
            Retourne None si aucune correspondance n'est trouvée.
    """

    formats_valides = ['identifiant', 'nom', 'numero_mesh', None]
    types_recherche_valides = ['identifiant', 'nom', 'numero_mesh']

    if format_reponse not in formats_valides:
        raise ValueError(f"format_reponse invalide : '{format_reponse}'. Choisissez parmi : {formats_valides[:-1]}.")

    if type_recherche not in types_recherche_valides:
        raise ValueError(f"type_recherche invalide : '{type_recherche}'. Choisissez parmi : {types_recherche_valides}.")

    for descripteur in racine.findall('DescriptorRecord'):
        ui = descripteur.findtext('DescriptorUI')
        nom = descripteur.findtext('DescriptorName/String')
        numero_mesh = [tree_number.text for tree_number in descripteur.findall('TreeNumberList/TreeNumber')]

        correspondance = False
        if type_recherche == 'identifiant' and ui == recherche:
            correspondance = True
        elif type_recherche == 'nom':
            if (ignore_case and nom.lower() == recherche.lower()) or (not ignore_case and nom == recherche):
                correspondance = True
        elif type_recherche == 'numero_mesh' and recherche in numero_mesh:
            correspondance = True

        if correspondance:
            reponse_complete = {
                'identifiant': ui,
                'nom': nom,
                'numero_mesh': numero_mesh
            }
            return reponse_complete if format_reponse is None else reponse_complete[format_reponse]

    if verbose:
        print(f"Aucun descripteur trouvé pour '{recherche}' avec type '{type_recherche}'.")

    return None



def chercher_descriptor_par_numero(racine, numero):
        for descripteur in racine.findall('DescriptorRecord'):
            tree_numbers = descripteur.findall('TreeNumberList/TreeNumber')
            for number in tree_numbers:
                if number.text == numero:
                    return descripteur.find('DescriptorName/String').text
        return None


def categorie_haute(racine, tree_number, level=None):
    """
    Recherche et retourne la catégorie de plus haut niveau associée à un numéro MeSH donné.

    Args:
        racine: L'élément racine de l'arbre XML MeSH chargé.
        tree_number (str): Le numéro MeSH à rechercher (par ex. "C08.381.746").
        level (int, optionnel): Niveau désiré dans la hiérarchie MeSH (0 correspond au niveau lettre).

    Returns:
        str or None: La catégorie trouvée ou None si aucune correspondance.
    """

    categories_lettres = {
        "A": "Anatomy",
        "B": "Organisms",
        "C": "Diseases",
        "D": "Chemicals and Drugs",
        "E": "Analytical, Diagnostic and Therapeutic Techniques, and Equipment",
        "F": "Psychiatry and Psychology",
        "G": "Phenomena and Processes",
        "H": "Disciplines and Occupations",
        "I": "Anthropology, Education, Sociology, and Social Phenomena",
        "J": "Technology, Industry, and Agriculture",
        "K": "Humanities",
        "L": "Information Science",
        "M": "Named Groups",
        "N": "Health Care",
        "V": "Publication Characteristics",
        "Z": "Geographicals"
    }

    niveaux = tree_number.split('.')
    niveau_max = len(niveaux)

    if level is None:
        level = niveau_max

    if level == 0 or (len(tree_number) == 1 and level is None):
        return categories_lettres.get(tree_number[0].upper())

    if level > niveau_max:
        print(f"Le niveau spécifié ({level}) est trop élevé. Le niveau maximal possible pour '{tree_number}' est {niveau_max}.")
        return None

    numero_recherche = '.'.join(niveaux[:level])
    descriptor = chercher_descriptor_par_numero(racine, numero_recherche)

    if descriptor is None:
        print(f"Aucune catégorie trouvée pour le numéro {numero_recherche} au niveau {level}.")

    return descriptor



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


"""VERSION CACHED"""

from functools import lru_cache

@lru_cache(maxsize=None)
def rechercher_descripteur_cached(terme, racine):
    return MeSH.recherche_descripteur(racine, terme, format_reponse='numero_mesh')


def extraire_codes_disease_C_cached(dict_mesh_ligne, racine):
    """
    Version optimisée avec cache + rapide + propre.
    """
    codes = set()

    if not isinstance(dict_mesh_ligne, dict):
        return []

    for termes in dict_mesh_ligne.values():
        for terme in termes:
            list_mesh = rechercher_descripteur_cached(terme, racine)
            if list_mesh:
                for item in list_mesh:
                    if item.startswith("C") and len(item) > 2:
                        code = item[1:3]
                        if code.isdigit():
                            codes.add(code)

    return sorted(codes)