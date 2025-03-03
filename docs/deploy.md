# 🐳 Déploiement de l'application
Ce guide explique comment déployer cette application Django sur un serveur Linux avec Docker et Docker Compose.

---

## 🐈‍⬛ Etape 1: Cloner le depot
```bash
git clone https://github.com/amin-elmellouki/SAE_Consolidation
cd SAE_Consolidation
```

## 🐳 Étape 2 : Construire et lancer les conteneurs
```bash
docker-compose up -d --build
```

## 🛠 Étape 4 : Appliquer les migrations 
``` bash
docker-compose exec web python manage.py migrate
```

💡 Pour créer un utilisateur, voir : [Inscription et connexion](/login)

## 🚀 Étape 5 : Accéder à l’application
L’application est maintenant accessible sur le port 8000 du serveur :  
- 
* Si c'est un serveur local : http://localhost:8000/  
* Si c'est un serveur distant : http://[adresse_du_serveur]:8000/  

## 🌍 Étape 6 (Optionnel) : Configurer un nom de domaine
Pour utiliser un domaine, il faut configurer le `ALLOWED_HOSTS` dans `consolead/settings.py`
``` python
ALLOWED_HOSTS = ["domaine.com", "www.domaine.com", "adresse_ip_du_serveur"]
```

Puis redémarrer avec :
``` bash
docker-compose restart
```
