# Projet de matrice LED
> Mathis Déronne

Ce projet a été créé et est utilisé au sein de Bordeaux Ynov Campus.

![image](/images/front.jpeg)

Il utilise une ESP32 WROOM-32, trois barrettes de quatre matrices LED "MAX7219" soudées ensemble, et une batterie composée de 4 cellules 18650.

En utilisant le module Bluetooth de l'ESP32, il est possible d'envoyer un message depuis un téléphone qui s'affichera en défilement sur la matrice LED et se répétera jusqu'à la réception d'un nouveau message.

## Configuration de l'application

Pour envoyer un message à l'ESP via Bluetooth, certains téléphones comme les iPhones ne peuvent pas se connecter directement depuis le menu Bluetooth. Une application dédiée au BLE (Bluetooth Low Energy) est nécessaire.
L'application utilisée est **nRF Connect**, disponible gratuitement sur l'App Store.

## Branchement électronique

![image](/images/back.jpeg)

Les broches à connecter sont **VCC, GND, DIN, CS et CLK**. Les broches VCC, GND, DIN et CLK sont partagées entre les trois barrettes, mais doivent être branchées à chacune d'elles afin d'éviter un affaiblissement du signal.

### VCC 

Les broches VCC doivent être alimentées en 5V, connectées au + de la batterie.

### GND

Les broches GND sont branchées au - de la batterie.

### DIN

La broche DIN est partagée entre les trois barrettes et connectée à la broche **G23** de l'ESP.

### CS

CS est la seule broche individuelle à chaque barrette :

- Barrette 1 : **G21**
- Barrette 2 : **G16**
- Barrette 3 : **G17**

### CLK

CLK est partagée entre les trois barrettes et connectée à la broche **G18** de l'ESP.

## Finitions 

Le système comporte de nombreux câbles et composants. Un support pour l'ESP a été créé, et les câbles ont été regroupés avec des gaines thermorétractables (le fichier STL est disponible dans le dossier [fichiers 3D](/fichiers%203D/)). Pour le partage des signaux, deux bandes +/- provenant de breadboards ont été collées avec du ruban adhésif double face sur la plaque intérieure.

![image](/images/back2.jpeg)

Un support pour la batterie a été conçu, mais l'espace disponible était insuffisant. La batterie est donc maintenue avec du ruban adhésif double face dans le boîtier arrière, qui intègre également un port de recharge, un interrupteur marche/arrêt et un régulateur de tension.

![image](/images/coque.jpeg)

Cette configuration permet de séparer le boîtier arrière en débranchant simplement les câbles +/-, facilitant ainsi la maintenance.

## Utilisation

Pour utiliser le programme, installez le fichier [max7219](/Programmes/max7219.py) dans la carte.

Pour que le programme se lance au démarrage, enregistrez les deux fichiers Python du dossier [Programmes](/Programmes/) et renommez le programme principal en **main.py**. Les fichiers portant ce nom s'exécutent automatiquement au démarrage de l'ESP.

Une fois lancé, la carte apparaît dans l'application nRF Connect. Cliquez sur **No Filter**, entrez **ESP** dans **Name** et connectez-vous.

Dans la page ouverte, cliquez sur la deuxième icône en haut. Dans la section **Attribute Table**, cliquez sur la flèche vers le haut de la dernière ligne. Entrez le texte souhaité, sélectionnez **UTF8** et cliquez sur **Write**.

Le texte s'affichera en boucle jusqu'à la réception d'un nouveau message.

Des messages prédéfinis sont disponibles pour afficher des phrases plus longues. Les commandes actuelles sont :

- !HELP : affiche le lien du dépôt Git
- !Ranger : affiche "Pensez à ranger le matériel et à nettoyer les tables avant de partir"

## Problèmes connus

### Les matrices s'éteignent ou allument des LED aléatoirement

Un signal corrompu ou incomplet peut causer un dysfonctionnement des matrices. Ce problème affecte principalement la barrette du milieu. Les matrices sont réinitialisées à chaque début de boucle pour résoudre ce problème.

### Le signal BLE ne persiste pas

Ce problème provient généralement du téléphone. Les iPhones tendent à ignorer les signaux des ESP. Un redémarrage du programme peut rétablir la connexion.

### Les textes trop longs sont coupés

Le BLE limite les envois à 20 caractères. Utilisez des messages prédéfinis dans le code pour les textes plus longs.

## Avancement du projet

```
08/01/2026
La programmation est terminée. 
La modélisation 3D progresse avec la création du boîtier pour l'ESP et la batterie. 
Des améliorations électroniques sont prévues : 
ajout d'un interrupteur marche/arrêt et remplacement de la breadboard par des barrettes de zinc.
```

```
13/01/2026
Les phrases prédéfinies ont été intégrées au code. 
Les signaux s'affaiblissaient avec les jumpers, les câbles ont été conservés. 
La modélisation 3D du boîtier d'alimentation est en cours.
```

```
04/02/2026
Le projet est terminé. 
Le câblage est finalisé et optimisé. 
La batterie et le régulateur sont fixés avec du ruban adhésif double face.
```

## Axes d'amélioration

### Support fonctionnel pour la batterie

Créer un support intégré à la coque permettant une batterie fixe et démontable sans adhésif.

### Support pour le régulateur de tension

Concevoir un support fixe pour le régulateur intégré à la coque.

### Carte PCB personnalisée

Une PCB personnalisée avec ESP32 et distribution des signaux CLK, DIN, VCC et GND réduirait considérablement l'encombrement.

### Batterie moins épaisse

Une batterie plus fine associée à une PCB personnalisée permettrait de réduire l'épaisseur de la coque.
