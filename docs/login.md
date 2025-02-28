# 🤓 Gestion du compte

## Création d'un compte
Pour créer un compte, il suffit d'executer la commande suivante:
=== "Avec Docker" 
    ``` bash
    $ docker-compose exec web python manage.py createsuperuser
    ```

=== "Sans docker"
    ``` bash
    $ python manage.py createsuperuser
    ```

Et de remplir les champs demandés.

## Connexion
![Page de connexion](images/login.png)

## Mot de passe oublié
TODO