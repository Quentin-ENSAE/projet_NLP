import numpy as np

def vectorizer(indices_positifs, taille_vecteur=26):
    """
    Crée un vecteur binaire avec des 1 aux indices spécifiés et 0 ailleurs.
    Retourne un vecteur de zéros si la liste d'entrée est vide.

    Parameters:
    - indices_positifs (list[int]): Liste des indices à mettre à 1 (indices de 1 à taille_vecteur).
    - taille_vecteur (int): Taille du vecteur résultat (défaut=26).

    Returns:
    - numpy.ndarray : vecteur binaire.
    """
    indices_positifs = list(map(int, indices_positifs))
    vecteur_binaire = np.zeros(taille_vecteur, dtype=int)

    if indices_positifs:
        if not all(1 <= idx <= taille_vecteur for idx in indices_positifs):
            raise ValueError(f"Tous les indices doivent être compris entre 1 et {taille_vecteur}.")
        vecteur_binaire[np.array(indices_positifs) - 1] = 1

    return vecteur_binaire