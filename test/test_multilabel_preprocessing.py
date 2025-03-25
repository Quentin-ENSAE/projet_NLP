import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import multilabel_preprocessing as mp

# Tests unitaires
def test_vectorizer():
    assert np.array_equal(mp.vectorizer([1, 8, 26]),
                          np.array([1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]))
    
    assert np.array_equal(mp.vectorizer([]), np.zeros(26, dtype=int))

    assert np.array_equal(mp.vectorizer([5]),
                          np.array([0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))

    try:
        mp.vectorizer([0, 27])
    except ValueError as e:
        assert str(e) == "Tous les indices doivent être compris entre 1 et 26."
    else:
        assert False, "Exception non levée pour des indices hors limites"

# Exécution des tests
if __name__ == "__main__":
    test_vectorizer()
    print("Tous les tests sont réussis !")