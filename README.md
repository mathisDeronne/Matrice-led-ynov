# Projet de matrice led
> Mathis Déronne

Ce projet est un projet créé et utilisé à Bordeaux Ynov Campus.

![image](/images/front.jpeg)

Il utilise une ESP32 WROOM-32, 3 barrettes de 4 matrices leds "MAX7219" soudées ensemble, et une batterie 5V.

En utilisant le module Bluetooth de l'ESP32, on peut envoyer un message depuis notre téléphone qui sera affiché en défilement sur la matrice led et qui sera répété jusqu'à ce qu'un nouveau message arrive.

## Setup application

Pour envoyer un message à l'ESP en bluetooth, certains téléphones comme les iPhones ne peuvent pas simplement se connecter depuis le menu Bluetooth, il faut installer une application pour utiliser le BLE (ou Bluetooth Low Energy).
L'application que j'utilise est "**nRF Connect**" disponible sur l'app store gratuitement.

## Branchement électronique

![image](/images/back.jpeg)

Les différents pins à connecter sont **VCC, GND, DIN, CS, CLK**. Les pins VCC, GND, DIN et CLK sont reliés et partagés entre les 3 barrettes mais ils doivent être branchés à chaque barrette et pas seulement à la première car le signal peut s'affaiblir au travers des matrices.

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

Pour utiliser le programme, il faut le lancer à l'intérieur de la carte. Pensez à également installer le fichier [max7219](/Programmes/max7219.py) dans cette dernière.

Si vous voulez que le programme se lance au démarrage de la carte, alors il faut enregistrer les 2 codes Python contenus dans [Programmes](/Programmes/) et renommez le programme principal en **main.py**. Les fichiers portant ce nom sont automatiquement exécutés au démarrage de l'ESP.

Une fois le programme lancé, la carte devrait apparaître sur l'application nRF Connect. Cliquez sur **No Filter** et dans **Name** entrez **ESP**.

Une fois que vous avez trouvé la carte, cliquez sur **Connect**. Une fois la carte connectée, en haut de la page qui vient de s'ouvrir, vous verrez 5 icônes. Cliquez sur la 2ème. Dans la section "**Attribute Table**" il devrait y avoir plusieurs lignes, cliquez sur la flèche vers le haut de la dernière (tout en bas à droite). Une nouvelle fenêtre s'est ouverte, entrez le texte que vous voulez envoyer, cliquez sur **UTF8** et cliquez sur **Write**.

Une fois que la boucle actuelle est terminée, une nouvelle commencera avec le texte que vous avez écrit et sera affiché en boucle jusqu'à ce que l'ESP reçoive un nouveau message.

## Problèmes connus

Certains problèmes sont déjà résolus mais je vais les expliquer ici.

### Les matrices s'éteignent ou allument des LEDs au hasard

Si la matrice reçoit un signal qui bug (corrompu ou incomplet), elle va soit bugger, soit s'éteindre complètement. Cela doit être dû à l'état des barrettes car ça ne se passe presque que sur la barrette du milieu. Normalement, il faudrait relancer le programme pour que les matrices se rallument, mais j'ai décidé de redéfinir les matrices à chaque début de boucle, ce qui les rallume pour le prochain passage du texte.

### Le signal BLE ne tient pas, je ne détecte plus l'ESP sur l'app

Malheureusement, j'ai cru comprendre que c'était un problème côté téléphone car les iPhones ont tendance à ignorer les signaux des ESP et il n'existe pas de fix possible à part relancer le programme pour connecter le téléphone à nouveau.

### Les textes trop longs sont coupés

Je viens de découvrir le problème, je vais travailler dessus.

## Avancement projet et futurs ajouts

Pour l'instant, la programmation est finie, sauf si je dois ajouter des fonctionnalités ou des fix. Niveau 3D, je n'ai que le boîtier pour la matrice et je vais bientôt me mettre sur le boîtier qui contiendra l'ESP et la batterie. Côté élec, je prévois d'ajouter un interrupteur pour allumer/éteindre le système et qui servira de coupe-circuit en cas de problème, et je vais sûrement remplacer la breadboard par des barrettes de zinc pour partager mon alimentation, masse, et mes signaux DIN et CLK.