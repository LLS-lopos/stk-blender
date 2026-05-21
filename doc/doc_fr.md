# io_artiste (fr)

### Liste de Nœuds

- **operator** : nœuds primaire et/ou essentiels pour lancer le(s) test(s)
- **mode** : lance les différents modes de jeu existants
- **debug** : débogage et options supplémentaires

---
|Node|catégorie|image|description|
|:---:|:---:|:---:|:---:|
|Init|operator|![](./IMG/init_01.jpeg)| est le point de départ de l'arbre de nœud|
|CLI|operator|![](./IMG/CLI_01.jpeg)| est un nœuds qui s'utilise comme un terminal|
|Go Run Test|operator|![](./IMG/running_01.jpeg)|est le nœud qui exécute l'arbre de nœud (commande terminal)|
|Preview CMD|debug|![](./IMG/preview_01.jpeg)|est un nœud de prévisualisation de commande|
---

## Nœud Init
- **SuperUser** : permet d'exécuté une commande en tant qu'administrateur (n'est pas disponible sur Windows ouvrir directement en mode administrateur pour un comportement similaire)
- **Password (si SuperUser Checked)** : votre mot de passe personnel.

![](./IMG/init_sudo_02.jpeg)
- **Executable Custom** : active le choix d'un exécutable custom.
- **Game (file) path (si Executable Custom Checked)** : Utilisez un exécutable STK autre que celui installer sur le system.

![](./IMG/init_git_custom_02.jpeg)
- **Track (folder) path** : chargé son propre dossier de "Track/Battle/Soccers".
- **Kart (folder) path** : chargé son propre dossier de "Kart".
- **Disable addon tracks** : si activé ne charge pas les extension "Tracks/Battle/Soccers" télécharger depuis le jeu.
- **Disable addon karts** : si activé ne charge pas les extension "Karts" télécharger depuis le jeu.
- **v(2.x or 1.x)** : Permet d'ajuster la commande en fonction de si l'on veut utilise SupertuxKart 1.x ou SuperTuxKart Evolution (2.x)
- **Difficulty** : choisir un niveau de difficulté (Novice/Intermediare/Expert/SuperTux) si v(2.x or 1.x) est vrai un nouveau de difficulté supplémentaire est disponible.

Quand il est utilisez il est toujours au départ de l'arbre de nœud

![](./IMG/init_04.jpeg)

## Nœuds CLI

est à considérer comme un terminal

![](./IMG/CLI_02.jpeg)

Peuvent être utilsez à la suite pour un visuel plus agréable

![](./IMG/CLI_03.jpeg)

## Nœuds Go Run Test

est le seul nœud réellement obligatoire car c'est lui qui lance l'excution de la commande construit avec l'arbre de nœud
- **Run** : lance la commande à partir de Blender (bloc l'interface utilisateur de Blender)
- **Popen** : lance la commande indépendament de Blender (ne bloc pas l'interface utilisateur de Blender)

![](./IMG/running_02.jpeg)

il se place toujours à la fin de l'arbre de nœud

## Nœuds Preview CMD

ce nœud permet de prévisualisez la/les commande(s) construit dans l'arbre de nœud ce qui peut pratique pour s'assurer du lancement de la bonne commande en vérifiant les option choisi

il peut afficher de longue commande sur plusieur ligne

![](./IMG/preview_02.jpeg)
![](./IMG/preview_03.jpeg)
![](./IMG/preview_04.jpeg)

### Les nœuds peuvent être associé les un au autre sans problème

![](./IMG/tree_01.jpeg)
![](./IMG/tree_02.jpeg)
![](./IMG/tree_03.jpeg)


---
### [retour acceuil](./../doc_io_artiste.md)
