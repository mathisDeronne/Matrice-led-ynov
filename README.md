# Projet de matrice LED
> Mathis Déronne

Ce projet est un projet créé et utilisé à Bordeaux Ynov Campus.

![image](/images/front.jpeg)

Il utilise une ESP32 WROOM-32, 3 barrettes de 4 matrices LEDs "MAX7219" soudées ensemble, et une batterie 5V.

En utilisant le module Bluetooth de l'ESP32, on peut envoyer un message depuis notre téléphone qui sera affiché en défilement sur la matrice LED et qui sera répété jusqu'à ce qu'un nouveau message arrive.

## Setup application

Pour envoyer un message à l'ESP en Bluetooth, certains téléphones comme les iPhones ne peuvent pas simplement se connecter depuis le menu Bluetooth. Il faut installer une application pour utiliser le BLE (Bluetooth Low Energy).
L'application que j'utilise est "**nRF Connect**", disponible sur l'App Store gratuitement.

## Branchement électronique

![image](/images/back.jpeg)

Les différents pins à connecter sont **VCC, GND, DIN, CS, CLK**. Les pins VCC, GND, DIN et CLK sont reliés et partagés entre les 3 barrettes, mais ils doivent être branchés à chaque barrette et pas seulement à la première, car le signal peut s'affaiblir à travers les matrices.

### VCC 

Les pins VCC sont à alimenter en 5V. Ils sont donc connectés au + de la batterie.

### GND

Les pins GND sont à brancher au - de la batterie.

### DIN

Le pin DIN est relié entre les 3 barrettes et est branché sur le pin **G23** de l'ESP.

### CS

CS est le seul pin individuel à chaque barrette.

- Barrette 1 : **G21** sur l'ESP
- Barrette 2 : **G16** sur l'ESP
- Barrette 3 : **G17** sur l'ESP

### CLK

CLK est également relié et partagé entre les 3 barrettes. Il se branche au pin **G18** sur l'ESP.

## Utilisation

Pour utiliser le programme, il faut le lancer à l'intérieur de la carte. Pensez à aussi installer le fichier [max7219](/Programmes/max7219.py) dans cette dernière.

Si vous voulez que le programme se lance au démarrage de la carte, alors il faut enregistrer les 2 codes Python contenus dans [Programmes](/Programmes/) et renommer le programme principal en **main.py**. Les fichiers portant ce nom sont automatiquement exécutés au démarrage de l'ESP.

Une fois le programme lancé, la carte devrait apparaître sur l'application nRF Connect. Cliquez sur **No Filter** et dans **Name**, entrez **ESP**.

Une fois que vous avez trouvé la carte, cliquez sur **Connect**. Une fois la carte connectée, en haut de la page qui vient de s'ouvrir, vous verrez 5 icônes. Cliquez sur la 2e. Dans la section "**Attribute Table**", il devrait y avoir plusieurs lignes. Cliquez sur la flèche vers le haut de la dernière (tout en bas à droite). Une nouvelle fenêtre s'est ouverte, entrez le texte que vous voulez envoyer, cliquez sur **UTF8** et cliquez sur **Write**.

Une fois que la boucle actuelle est terminée, une nouvelle commencera avec le texte que vous avez écrit et sera affiché en boucle jusqu'à ce que l'ESP reçoive un nouveau message.

Il existe des messages prédéfinis dans le code pour afficher des phrases plus longues (voir Problèmes connus). La manière dont ils sont gérés est simple : si vous envoyez une commande précise au lieu d'un texte, le message prédéfini dans l'ESP sera affiché sur la matrice. Les commandes actuelles de l'ESP sont :

- !HELP : fait défiler le lien vers ce repo git.
- !Ranger : affiche la phrase "Pensez à ranger le matériel et à nettoyer les tables avant de partir".

D'autres phrases peuvent être ajoutées au besoin en ajoutant un **if** comme pour les deux commandes ci-dessus. Pensez juste à changer la commande pour ne pas avoir la même plusieurs fois.

## Problèmes connus

Certains problèmes sont déjà résolus, mais je vais les expliquer ici.

### Les matrices s'éteignent ou allument des LEDs au hasard

Si la matrice reçoit un signal qui bug (corrompu ou incomplet), elle va soit bugger, soit s'éteindre complètement. Cela doit être dû à l'état des barrettes, car ça ne se passe presque que sur la barrette du milieu. Normalement, il faudrait relancer le programme pour que les matrices se rallument, mais j'ai décidé de redéfinir les matrices à chaque début de boucle, ce qui les rallume pour le prochain passage du texte.

### Le signal BLE ne tient pas, je ne détecte plus l'ESP sur l'app

Malheureusement, j'ai cru comprendre que c'était un problème côté téléphone, car les iPhones ont tendance à ignorer les signaux des ESP et il n'existe pas de correctif possible à part relancer le programme pour connecter le téléphone à nouveau.

### Les textes trop longs sont coupés

Le problème vient du BLE qui ne peut envoyer que 20 caractères. Rien dans mon programme ne peut réparer ça. Il faut donc se limiter à faire des messages de moins de 20 caractères ou à prévoir des messages prédéfinis dans le code.

## Avancement projet et futurs ajouts

```
08/01/2026
Pour l'instant, la programmation est finie, sauf si je dois ajouter des fonctionnalités ou des correctifs. Niveau 3D, je n'ai que le boîtier pour la matrice et je vais bientôt me mettre sur le boîtier qui contiendra l'ESP et la batterie. Côté électronique, je prévois d'ajouter un interrupteur pour allumer/éteindre le système et qui servira de coupe-circuit en cas de problème, et je vais sûrement remplacer la breadboard par des barrettes de zinc pour partager mon alimentation, ma masse, et mes signaux DIN et CLK.
```

```
13/01/2026
Les phrases prédéfinies ont été ajoutées dans le code, ce qui permettra d'afficher des phrases de plus de 20 caractères sur la matrice, mais elles devront être préenregistrées dans le code pour cela. Le reste des fonctionnalités restent inchangées. J'ai essayé de réduire le nombre de câbles en les remplaçant par des jumpers, mais les signaux se perdaient, alors j'ai dû rester sur la solution câbles.
Je dois encore faire la 3D du boîtier d'alimentation et de l'ESP et décider d'un moyen de répartir mes pistes DIN, CLK, GND et VCC.
```