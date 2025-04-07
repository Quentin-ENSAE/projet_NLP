import numpy as np
from typing import List, Optional, Union

def vectorizer(indices_positifs: Union[List[int], List[str], None], taille_vecteur: int = 26) -> np.ndarray:
    """
    Crée un vecteur booléen avec True aux indices spécifiés (1-based), False ailleurs.

    Parameters:
    ----------
    indices_positifs : list[int | str] | None
        Liste des indices (1-based) à activer. Peut contenir des entiers ou chaînes.
    taille_vecteur : int, default=26
        Taille du vecteur de sortie.

    Returns:
    -------
    np.ndarray[bool]
        Vecteur booléen de longueur `taille_vecteur`.
        Tous les indices sont à False si la liste est vide ou None.
    """
    # Si la liste est vide ou None → vecteur False
    if not indices_positifs:
        return np.zeros(taille_vecteur, dtype=bool)

    # Conversion en entiers et vérification de validité
    try:
        indices_positifs = list(map(int, indices_positifs))
    except ValueError:
        raise ValueError("Tous les éléments de `indices_positifs` doivent être convertibles en int.")

    if not all(1 <= idx <= taille_vecteur for idx in indices_positifs):
        raise ValueError(f"Tous les indices doivent être compris entre 1 et {taille_vecteur} inclus.")

    vecteur = np.zeros(taille_vecteur, dtype=bool)
    vecteur[np.array(indices_positifs, dtype=int) - 1] = True

    return vecteur


def mesh_labels_from_vector(vector: np.ndarray) -> List[str]:
    """
    Transforme un vecteur booléen en une liste de labels MeSH correspondants.

    Parameters
    ----------
    vector : np.ndarray
        Vecteur booléen de longueur 26 indiquant les catégories actives.

    Returns
    -------
    List[str]
        Liste des labels MeSH correspondant aux positions True dans le vecteur.
    """
    if vector.shape[0] != 26:
        raise ValueError("Le vecteur doit être de longueur 26.")

    mesh_labels = [
        "C01 – bacterial infections and mycoses",
        "C02 – virus diseases",
        "C03 – parasitic diseases",
        "C04 – neoplasms",
        "C05 – musculoskeletal diseases",
        "C06 – digestive system diseases",
        "C07 – stomatognathic diseases",
        "C08 – respiratory tract diseases",
        "C09 – otorhinolaryngologic diseases",
        "C10 – nervous system diseases",
        "C11 – eye diseases",
        "C12 – urologic and male genital diseases",
        "C13 – female genital diseases and pregnancy complications",
        "C14 – cardiovascular diseases",
        "C15 – hemic and lymphatic diseases",
        "C16 – congenital, hereditary, and neonatal diseases and abnormalities",
        "C17 – skin and connective tissue diseases",
        "C18 – nutritional and metabolic diseases",
        "C19 – endocrine system diseases",
        "C20 – immune system diseases",
        "C21 – disorders of environmental origin",
        "C22 – animal diseases",
        "C23 – pathological conditions, signs and symptoms",
        "C24 – occupational diseases",
        "C25 – chemically induced disorders",
        "C26 – wounds and injuries"
    ]

    return [label for is_active, label in zip(vector, mesh_labels) if is_active]