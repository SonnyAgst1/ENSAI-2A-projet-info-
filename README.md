#  Application Sportive - Suivi d'Activités
Application web complète de suivi d'activités sportives avec gestion sociale, statistiques détaillées et analyse GPX.

##  Architecture
```
ENSAI-2A-projet-info/
├── src/
│   ├── api/                    # Routes API FastAPI
│   │   ├── activite_router.py
│   │   ├── fil_router.py
│   │   ├── interaction_router.py
│   │   ├── statistiques_router.py
│   │   └── utilisateur_router.py
│   ├── business_objects/       # Modèles métier
│   │   ├── activite.py
│   │   ├── utilisateur.py
│   │   ├── commentaire.py
│   │   └── models.py          # Modèles SQLAlchemy
│   ├── dao/                    # Accès base de données
│   │   ├── activite_dao.py
│   │   ├── utilisateur_dao.py
│   │   ├── commentaire_dao.py
│   │   ├── follow_dao.py
│   │   └── like_dao.py
│   ├── service/                # Logique métier
│   │   ├── activite_service.py
│   │   ├── utilisateur_service.py
│   │   ├── fil_actualite_service.py
│   │   └── statistiques_service.py
│   ├── utils/                  # Utilitaires
│   │   └── gpx_parser.py
│   ├── database.py             # Configuration BDD
│   └── main_api.py            # Point d'entrée API
├── app.py                      # Interface Streamlit
├── data/                       # Base de données SQLite
├── uploads/gpx/                # Fichiers GPX uploadés
└── requirements.txt
```

### Étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/SonnyAgst1/ENSAI-2A-projet-info.git
cd ENSAI-2A-projet-info
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Initialiser la base de données**
```bash
python __init__db.py
```

## 💻 Utilisation

### Lancer l'API
```bash
python -m uvicorn main_api:app --reload --host 0.0.0.0 --port 8000 --app-dir src
```

### Lancer l'interface Streamlit
```bash
streamlit run app.py
```


### Tests
```bash
# Tests des DAOs
PYTHONPATH=src python -m pytest src/tests_DAO/ -v

# Tests des services
PYTHONPATH=src python -m pytest src/tests_service/ -v

# Tests des business objects
PYTHONPATH=src python -m pytest src/tests_business_objects/ -v
pour executer test service PYTHONPATH=src python -m pytest src/tests_service/ -v
```

### Groupe

- **Alexis** 
- **Denis** 
- **Maëlys** 
- **Sonny** 
