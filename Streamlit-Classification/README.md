# Tableau de Bord d'Analyse de Service Client Free via Twitter

## Résumé Exécutif

Ce projet présente une application web interactive de visualisation et d'analyse de données destinée à l'analyse des interactions client-serveur sur le réseau social Twitter. L'application s'adresse spécifiquement à l'opérateur télécom Free et vise à améliorer la compréhension et la gestion du service client (SAV) à travers l'analyse des tweets clients.

L'application propose un tableau de bord analytique développé avec Streamlit, permettant l'exploration interactive de données structurées de tweets classifiés selon plusieurs dimensions : sentiment, urgence, type d'incident, et thématique. L'interface offre des visualisations dynamiques adaptées à différents profils utilisateurs (Manager, Data Analyst, Agent SAV), facilitant ainsi la prise de décision stratégique et opérationnelle.

## Table des Matières

1. [Introduction](#introduction)
2. [Contexte et Objectifs](#contexte-et-objectifs)
3. [Architecture Technique](#architecture-technique)
4. [Technologies Utilisées](#technologies-utilisées)
5. [Structure du Projet](#structure-du-projet)
6. [Installation et Configuration](#installation-et-configuration)
7. [Utilisation](#utilisation)
8. [Fonctionnalités Principales](#fonctionnalités-principales)
9. [Tests et Qualité du Code](#tests-et-qualité-du-code)
10. [Déploiement](#déploiement)
11. [Limitations et Perspectives](#limitations-et-perspectives)

---

## Introduction

Dans un contexte où les réseaux sociaux constituent un canal de communication privilégié entre les clients et les entreprises, l'analyse des interactions numériques représente un enjeu majeur pour améliorer la satisfaction client et optimiser les processus de service après-vente. Ce projet s'inscrit dans cette démarche en proposant un outil d'analyse de données spécialisé pour le traitement des tweets clients de l'opérateur Free.

L'application développée permet de transformer des données brutes de tweets en informations actionnables grâce à des visualisations interactives et des indicateurs de performance clés (KPI). Elle répond à un besoin identifié dans le domaine du service client numérique où la volumétrie importante des données nécessite des outils d'analyse adaptés.

## Contexte et Objectifs

### Problématique

Les entreprises modernes font face à un afflux massif de données client sur les réseaux sociaux. Pour un opérateur télécom comme Free, l'analyse de ces données représente un défi technique et organisationnel :

- Volume important de tweets à analyser quotidiennement
- Nécessité d'identifier rapidement les réclamations et leur niveau d'urgence
- Besoin de comprendre les tendances et motifs de réclamation
- Défis liés à la priorisation des interventions pour les équipes SAV

### Objectifs du Projet

L'application développée vise à répondre à plusieurs objectifs :

1. **Visualisation Interactive** : Offrir une interface utilisateur intuitive permettant l'exploration de données de tweets classifiés

2. **Analyse Multi-dimensionnelle** : Permettre l'analyse selon plusieurs axes : sentiment, urgence, type d'incident, thématique, et temporalité

3. **Personnalisation par Profil** : Adapter l'affichage des informations selon le profil utilisateur (Manager, Data Analyst, Agent SAV)

4. **Décision Opérationnelle** : Fournir des outils d'aide à la décision pour la priorisation des interventions et l'analyse des performances SAV

5. **Scalabilité** : Concevoir une architecture modulaire permettant l'évolution future de l'application

## Architecture Technique

### Principes de Conception

L'architecture de l'application suit les principes de séparation des responsabilités et de modularité. Le code est organisé en modules distincts, chacun ayant une responsabilité clairement définie :

- **Couche de Configuration** : Centralisation des paramètres et constantes
- **Couche de Données** : Chargement, validation et transformation des données
- **Couche Métier** : Calculs d'indicateurs et métriques
- **Couche de Visualisation** : Génération de graphiques et figures
- **Couche Présentation** : Interface utilisateur et orchestration

### Modèle de Données

Les données traitées correspondent à des tweets structurés contenant les informations suivantes :

- **Identifiants** : Identifiant unique du tweet
- **Métadonnées Temporelles** : Date et heure de création
- **Classification** : Sentiment (négatif, neutre, positif), urgence (basse, moyenne, haute), type d'incident
- **Thématique** : Catégorisation thématique du contenu
- **Engagement** : Métriques d'engagement (favoris, retweets, réponses)
- **Contenu** : Texte complet du tweet

### Flux de Traitement

Le traitement des données suit un flux séquentiel :

1. **Chargement** : Import des données depuis un fichier CSV ou un échantillon prédéfini
2. **Validation** : Vérification de la présence des colonnes obligatoires et validation des formats
3. **Transformation** : Normalisation des dates, extraction de dimensions temporelles, calcul de métriques dérivées
4. **Filtrage** : Application des filtres utilisateur (période, sentiment, urgence, incident)
5. **Calcul** : Génération des indicateurs et métriques selon les filtres appliqués
6. **Visualisation** : Création et affichage des graphiques interactifs

## Technologies Utilisées

### Stack Technique

**Framework Web**
- Streamlit (version 1.36+) : Framework Python pour la création d'applications web interactives. Streamlit a été choisi pour sa simplicité d'utilisation et sa capacité à créer rapidement des interfaces de visualisation de données.

**Traitement des Données**
- Pandas (version 2.1+) : Bibliothèque Python pour la manipulation et l'analyse de données tabulaires. Utilisée pour le chargement, la transformation et l'analyse des fichiers CSV.

**Visualisation**
- Plotly (version 5.18+) : Bibliothèque de visualisation interactive. Permet la création de graphiques interactifs adaptés à une utilisation web.

**Traitement du Texte**
- WordCloud (version 1.9+) : Génération de nuages de mots pour l'analyse textuelle des tweets négatifs.

**Utilitaires**
- NumPy (version 1.26+) : Bibliothèque de calcul scientifique, utilisée par les dépendances.
- Matplotlib (version 3.8+) : Bibliothèque de visualisation, utilisée pour l'affichage des nuages de mots.

**Tests**
- Pytest (version 7.4+) : Framework de test unitaire et d'intégration pour Python.

### Justification des Choix Techniques

Le choix de Streamlit comme framework principal s'explique par plusieurs facteurs :

1. **Rapidité de Développement** : Permet de créer rapidement des interfaces fonctionnelles sans nécessiter de connaissances en développement web frontend (HTML/CSS/JavaScript)

2. **Intégration Native avec Python** : Facilite l'utilisation des bibliothèques de data science (Pandas, Plotly) dans l'environnement web

3. **Déploiement Simplifié** : Streamlit Cloud offre un déploiement gratuit et automatisé depuis un dépôt Git

4. **Interactivité Native** : Gestion automatique des interactions utilisateur (filtres, widgets) sans code supplémentaire complexe

Plotly a été préféré à d'autres bibliothèques de visualisation pour ses capacités d'interactivité avancées (zoom, pan, hover) qui enrichissent l'expérience utilisateur dans un contexte d'analyse de données.

## Structure du Projet

```
streamlit/
├── app.py                      # Point d'entrée principal de l'application
├── requirements.txt            # Dépendances Python du projet
├── README.md                   # Documentation principale
│
├── app_core/                   # Modules métier de l'application
│   ├── __init__.py            # Initialisation du package
│   ├── config.py              # Configuration et constantes
│   ├── data.py                # Chargement et validation des données
│   ├── metrics.py             # Calculs de métriques métier
│   ├── plots.py               # Génération de visualisations
│   └── sections.py            # Composants d'interface utilisateur
│
├── Data/                       # Données du projet
│   ├── sample_clients.csv     # Échantillon de données clients
│   ├── reponses_free.csv      # Données de réponses SAV
│   └── free_tweet_classified_clean.csv  # Dataset complet (optionnel)
│
├── docs/                       # Documentation technique
│   ├── ARCHITECTURE.md        # Documentation de l'architecture
│   └── DEPLOYMENT.md          # Guide de déploiement
│
├── scripts/                    # Scripts utilitaires
│   ├── generate_sample.py     # Génération d'échantillons de données
│   └── pre_commit_check.py    # Vérifications pré-commit
│
└── tests/                      # Tests automatisés
    ├── test_integration.py    # Tests d'intégration
    ├── test_metrics.py        # Tests des calculs métriques
    ├── test_plots.py          # Tests des visualisations
    └── test_sections.py       # Tests des composants UI
```

### Description des Modules

**app.py**
Point d'entrée principal de l'application Streamlit. Orchestre le chargement des données, l'application des filtres, et le rendu des différentes sections du tableau de bord. Gère également la configuration de la page et les interactions utilisateur au niveau de la barre latérale.

**app_core/config.py**
Module centralisant toutes les constantes de configuration : chemins de fichiers, palettes de couleurs (identité visuelle Free), mappings de catégorisation (sentiments, urgences), et colonnes requises pour la validation des données.

**app_core/data.py**
Responsable du chargement et de la préparation des données. Implémente :
- Validation des colonnes obligatoires
- Normalisation des dates et extraction de dimensions temporelles
- Génération de colonnes dérivées (semaine, jour de la semaine, heure)
- Mise en cache des données via le décorateur `@st.cache_data` pour optimiser les performances

**app_core/metrics.py**
Contient les fonctions de calcul des métriques métier :
- Calcul du temps de réponse moyen et médian entre tweets clients et réponses SAV
- Conversion de minutes en format lisible (jours, heures, minutes)

**app_core/plots.py**
Module dédié à la génération de visualisations Plotly. Chaque fonction génère un type de graphique spécifique (camembert, barres, lignes, treemap) avec application automatique du thème visuel Free. Les fonctions sont conçues comme des fonctions pures, facilitant leur testabilité.

**app_core/sections.py**
Orchestre le rendu des différentes sections de l'interface utilisateur. Chaque fonction `render_*` est responsable de l'affichage d'une section spécifique du tableau de bord. Gère également la logique conditionnelle d'affichage selon le profil utilisateur sélectionné.

## Installation et Configuration

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour le clonage du dépôt)

### Installation Locale

1. **Cloner le dépôt**

```bash
git clone <url-du-depot>
cd streamlit
```

2. **Créer un environnement virtuel** (recommandé)

```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

Sur Windows :
```bash
venv\Scripts\activate
```

Sur Linux/Mac :
```bash
source venv/bin/activate
```

4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

### Configuration

L'application nécessite la présence de fichiers de données dans le répertoire `Data/` :

- `sample_clients.csv` : Échantillon de données pour la démonstration (requis pour la fonctionnalité échantillon)
- `reponses_free.csv` : Données des réponses SAV pour le calcul des temps de réponse (optionnel)

Les fichiers doivent respecter le format CSV avec les colonnes obligatoires définies dans `app_core/config.py` :

- `id` : Identifiant unique du tweet
- `created_at` : Date et heure de création (format datetime compatible)
- `topics` : Thématiques (format liste ou chaîne)
- `sentiment` : Sentiment (neg, neu, pos)
- `urgence` : Niveau d'urgence (basse, moyenne, haute)
- `incident` : Type d'incident
- `is_claim` : Indicateur de réclamation (0 ou 1)

## Utilisation

### Lancement de l'Application

Pour lancer l'application en local :

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse `http://localhost:8501` dans votre navigateur web.

### Workflow Utilisateur

1. **Import des Données**
   - Option A : Utiliser l'échantillon prédéfini en activant le toggle "Utiliser l'échantillon"
   - Option B : Importer un fichier CSV personnalisé via le sélecteur de fichiers dans la barre latérale

2. **Application de Filtres**
   - Sélectionner une période via le sélecteur de dates
   - Filtrer par thème, sentiment, type d'incident, ou niveau d'urgence

3. **Sélection du Profil**
   - Choisir un profil utilisateur (Manager, Data Analyst, Agent SAV) pour adapter l'affichage des informations

4. **Exploration des Données**
   - Naviguer dans les différentes sections du tableau de bord
   - Interagir avec les graphiques (zoom, survol pour détails)

5. **Export des Données**
   - Utiliser les boutons d'export pour télécharger les données filtrées au format CSV

### Fonctionnalités par Profil

**Profil Manager**
- Accès aux indicateurs généraux (KPIs globaux)
- Visualisation des temps de réponse SAV
- Vue d'ensemble des tendances

**Profil Data Analyst**
- Accès complet aux KPIs et métriques détaillées
- Visualisations analytiques approfondies
- Outils d'export de données

**Profil Agent SAV**
- File priorisée des réclamations
- Vue opérationnelle des tweets à traiter
- Classement par urgence et engagement

## Fonctionnalités Principales

### Visualisations Disponibles

1. **Distribution des Sentiments**
   - Graphique en camembert représentant la répartition des sentiments (négatif, neutre, positif) parmi les tweets SAV

2. **Niveaux d'Urgence**
   - Graphique en barres illustrant la distribution des tweets selon leur niveau d'urgence

3. **Top des Incidents**
   - Classement des types d'incidents les plus fréquents
   - Visualisation des tendances de réclamation

4. **Volume Temporel**
   - Évolution quotidienne et hebdomadaire du volume de tweets SAV
   - Histogrammes par heure et par jour de la semaine pour identifier les périodes de forte activité

5. **Distribution Thématique**
   - Analyse des thèmes principaux des tweets
   - Cartographie thématique via treemap pour visualiser les relations entre incidents et thèmes

6. **Analyse Sentiment-Thème**
   - Croisement des dimensions sentiment et thème pour identifier les sujets générant le plus de réactions négatives

7. **Nuage de Mots**
   - Visualisation textuelle des mots les plus fréquents dans les tweets négatifs pour identifier les préoccupations récurrentes

8. **Temps de Réponse SAV**
   - Calcul et affichage du temps de réponse moyen et médian
   - Analyse de la performance opérationnelle du service client

9. **File Priorisée Agent SAV**
   - Liste des réclamations classées par priorité (urgence et engagement) pour optimiser le traitement

### Indicateurs de Performance (KPI)

Les indicateurs calculés incluent :

- Nombre total de tweets analysés
- Nombre de tweets SAV (réclamations)
- Taux de réclamation (part de tweets SAV parmi tous les tweets)
- Temps de réponse moyen et médian
- Distribution des incidents et urgences

Tous les indicateurs sont dynamiques et s'adaptent automatiquement aux filtres appliqués par l'utilisateur.

## Tests et Qualité du Code

### Stratégie de Tests

L'application intègre une suite de tests automatisés couvrant plusieurs niveaux :

**Tests Unitaires**
- Tests des fonctions de calcul métier (`test_metrics.py`)
- Tests des fonctions de génération de graphiques (`test_plots.py`)
- Vérification de la gestion des cas limites (DataFrame vide, colonnes manquantes)

**Tests d'Intégration**
- Tests du workflow complet de l'application (`test_integration.py`)
- Vérification de l'orchestration des modules

**Tests des Composants**
- Tests des fonctions de rendu des sections UI (`test_sections.py`)
- Vérification du comportement avec différents types de données

### Exécution des Tests

Pour exécuter la suite de tests complète :

```bash
pytest -v
```

Pour exécuter les tests avec un rapport de couverture :

```bash
pytest --cov=app_core --cov-report=html
```

### Qualité du Code

Le code respecte plusieurs bonnes pratiques :

- **Type Hints** : Utilisation d'annotations de type pour améliorer la lisibilité et permettre la détection d'erreurs
- **Documentation** : Docstrings pour les fonctions principales
- **Modularité** : Séparation claire des responsabilités entre modules
- **Gestion d'Erreurs** : Validation des données et gestion des cas limites
- **Optimisation** : Mise en cache des données via `@st.cache_data` pour améliorer les performances

### Scripts de Vérification

Le projet inclut un script de vérification pré-commit (`scripts/pre_commit_check.py`) qui effectue :

- Vérification des imports
- Vérification de l'existence des fichiers de données
- Exécution automatique des tests

## Déploiement

### Déploiement sur Streamlit Cloud

L'application est conçue pour être déployée sur Streamlit Cloud, un service gratuit de déploiement d'applications Streamlit.

**Procédure de Déploiement**

1. **Préparation du Dépôt Git**
   - S'assurer que le code est versionné dans un dépôt Git (GitHub recommandé)
   - Vérifier que tous les fichiers nécessaires sont présents dans le dépôt

2. **Configuration sur Streamlit Cloud**
   - Se connecter à [Streamlit Cloud](https://share.streamlit.io/) avec un compte GitHub
   - Créer une nouvelle application
   - Sélectionner le dépôt et la branche à déployer
   - Spécifier le fichier principal (`app.py`)
   - Choisir une URL personnalisée pour l'application

3. **Vérification Post-Déploiement**
   - Vérifier que l'application se charge correctement
   - Tester les fonctionnalités principales
   - Valider l'affichage des visualisations

Pour plus de détails, consulter le fichier `docs/DEPLOYMENT.md`.

### Limitations du Déploiement

- Les fichiers de données doivent être présents dans le dépôt Git (limitation de taille des fichiers sur GitHub)
- Streamlit Cloud ne permet pas de persistance de données entre les sessions (chaque redémarrage recharge les données depuis les fichiers)
- Les performances peuvent être affectées par la taille des fichiers CSV importés

## Limitations et Perspectives

### Limitations Actuelles

1. **Source de Données**
   - L'application traite uniquement des fichiers CSV statiques. Une intégration en temps réel avec l'API Twitter nécessiterait des modifications architecturales significatives.

2. **Traitement du Langage**
   - L'analyse textuelle se limite actuellement à un nuage de mots. Une analyse de sentiment plus avancée ou une extraction de thèmes automatisée n'est pas implémentée.

3. **Scalabilité**
   - Le traitement de très gros volumes de données (plusieurs millions de lignes) peut poser des problèmes de performance en raison de l'absence de pagination et de chargement différé.

4. **Personnalisation**
   - Les profils utilisateurs sont statiques et définis dans le code. Un système d'authentification et de gestion de rôles permettrait une personnalisation plus avancée.

### Perspectives d'Évolution

1. **Intégration de Données en Temps Réel**
   - Connexion à l'API Twitter pour le chargement automatique des nouveaux tweets
   - Mise en place d'un système de rafraîchissement périodique des données

2. **Amélioration de l'Analyse Textuelle**
   - Intégration d'un modèle de classification automatique des sentiments
   - Extraction automatique de thèmes via des techniques de NLP (topic modeling)
   - Détection automatique de l'urgence basée sur le contenu

3. **Optimisation des Performances**
   - Implémentation d'une base de données pour le stockage des données
   - Mise en place d'un système de cache plus sophistiqué
   - Pagination des résultats pour améliorer la réactivité

4. **Fonctionnalités Avancées**
   - Système d'alerte basé sur des seuils de métriques
   - Comparaison temporelle (évolution semaine par semaine, mois par mois)
   - Export de rapports PDF automatiques
   - Tableaux de bord personnalisables par l'utilisateur

5. **Intégration avec des Outils Externes**
   - Connexion à des outils de CRM pour synchroniser les données
   - Export vers des outils de BI (Power BI, Tableau)
   - API REST pour permettre l'intégration avec d'autres systèmes

## Conclusion

Ce projet démontre l'application pratique des techniques de visualisation de données et d'analyse dans un contexte opérationnel concret. L'application développée offre une solution fonctionnelle pour l'analyse des interactions client-serveur sur Twitter, avec une interface utilisateur adaptée à différents profils d'utilisateurs.

L'architecture modulaire mise en place facilite l'évolution future du projet, tandis que la suite de tests automatisés garantit la stabilité et la maintenabilité du code. Le déploiement sur Streamlit Cloud permet une accessibilité immédiate de l'application sans nécessiter d'infrastructure serveur complexe.

Ce projet illustre comment les technologies modernes de data science et de visualisation peuvent être mises au service de problématiques business réelles, en particulier dans le domaine du service client numérique où la rapidité d'analyse et la qualité de l'information sont cruciales pour la prise de décision.

## Références Techniques

- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation Pandas](https://pandas.pydata.org/docs/)
- [Documentation Plotly](https://plotly.com/python/)
- [Documentation Pytest](https://docs.pytest.org/)

---

**Auteur** : [Votre Nom]  
**Institution** : [Votre Université/École]  
**Date** : [Année Académique]  
**Niveau** : Master
