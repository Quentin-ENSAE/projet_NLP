import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import MeSH

@pytest.fixture
def racine():
    # Chargement de l'arbre MeSH depuis le fichier XML
    return MeSH.chargement_arbre_mesh("data/desc2025.xml")

def test_niveau_0(racine):
    assert MeSH.categorie_haute(racine, 'C08', level=0) == 'Diseases'

def test_niveau_1(racine):
    assert MeSH.categorie_haute(racine, 'C08.360', level=1) == 'Respiratory Tract Diseases'

def test_niveau_2(racine):
    assert MeSH.categorie_haute(racine, 'C08.360.480', level=2) == 'Laryngeal Diseases'

def test_niveau_max(racine, capsys):
    assert MeSH.categorie_haute(racine, 'C08.360', level=3) is None
    captured = capsys.readouterr()
    assert "Le niveau maximal possible pour 'C08.360' est 2" in captured.out

def test_descriptor_non_trouve(racine, capsys):
    assert MeSH.categorie_haute(racine, 'C08.999', level=2) is None
    captured = capsys.readouterr()
    assert "Aucune catégorie trouvée pour le numéro C08.999 au niveau 2." in captured.out