# AR24 - Flask Template

Template Flask complet avec page de connexion, inscription et tableau de bord.

## Installation

```bash
pip install -r requirements.txt
python app.py
```

L'application sera disponible sur http://localhost:5000

## Identifiants de test

- **E-mail :** admin@meindj.com
- **Mot de passe :** admin123

## Structure

```
flask_template/
├── app.py                 # Application Flask (routes login/dashboard/register/logout)
├── requirements.txt       # Flask, Werkzeug
├── static/
│   └── style.css          # Styles (identiques au clone React)
└── templates/
    ├── base.html          # Layout commun (header MEINDJ DJO)
    ├── login.html         # Page connexion
    ├── register.html      # Page inscription
    └── dashboard.html     # Tableau de bord (protégé)
```

## Routes

| URL                  | Méthode | Description                  |
|----------------------|---------|------------------------------|
| `/`                  | GET     | Redirige vers /fr/user/login |
| `/fr/user/login`     | GET/POST| Connexion                    |
| `/register`          | GET/POST| Création de compte           |
| `/dashboard`         | GET     | Dashboard (auth requise)     |
| `/logout`            | GET     | Déconnexion                  |

## Sécurité

- Mots de passe hashés via `werkzeug.security`
- Sessions Flask sécurisées (modifier `SECRET_KEY` en production)
- Décorateur `@login_required` pour les pages protégées

## Pour aller plus loin

- Remplacer le dict `USERS` par une vraie BDD (SQLite, PostgreSQL...)
- Ajouter Flask-Login pour une gestion d'auth plus robuste
- Ajouter Flask-WTF pour la validation/CSRF des formulaires
