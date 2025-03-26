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