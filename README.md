<h3 align="center">
        <samp>&gt; Python Bomberman project
        </samp>
</h3>


<p align="center"> 
  <samp>
    <br>
    「 <b>B3 - EPSI Dev FS</b> 」
    <br>
  </samp>
</p>

<br/>

![projet bomberman](media/projet%20bomberman.png)


# Use To Code -

![PyCharms](https://img.shields.io/badge/PyCharm-000000?style=for-the-badge&logo=pycharm&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<br/>

# <center> - Installation - </center>

First, clone the repository on your PC :
```
git clone https://github.com/Feareis/epsi-dev-fs-python
```
Then move to the location where the repository was cloned :
```
cd ./wherever-you-want/epsi-dev-fs-python
```
Then install the dependencies :
```
pip install -r requirements.txt
```
To run the program, simply execute <b>Bomberman</b> :
```
py Bomberman.py
```

<br/>

# <center> - Objectifs - </center>

 <p>
- Manipuler les variables et les types de données en Python.
<br/>
- Utiliser des structures de contrôle comme les conditions et les boucles.
<br/>
- Générer des nombres aléatoires.
<br/>
- Gérer les entrées utilisateurs.
<br/>
- Implémenter des fonctionnalités de base d’un jeu et introduire des éléments de gamification (niveaux, scores, etc.).
</p>

<br/>

# <center> - Architecture du projet -

```php
├── db/
│   └── game.db
│   └── scores.db
├── media/
│   └── projet bomberman.png
├── bomb.py
├── Bomberman.py
├── db.py
├── game.py
├── game_2p.py
├── game_settings.py
├── menu.py
├── plate.py
├── player.py
├── README.md
└── requirements.txt
```

<br/>

# <center> - Choix techniques -

<p style="text-align:justify;">
Premièrement, le projet a été organisé en plusieurs modules distincts pour chaque fonctionnalité.
<br/>
Ainsi, game.py contient la logique principale du jeu, tandis que d'autres fichiers, comme player.py, plate.py, bomb.py, menu.py et db.py, gèrent respectivement les fonctionnalités relatives aux déplacements du joueur, au plateau de jeu, aux bombes, aux menus et à la gestion des données. 
<br/><br/>
Pour l’interface graphique, nous avons choisi Pygame, qui offre les outils nécessaires pour afficher le plateau, gérer les contrôles clavier, et implémenter des éléments graphiques. Les couleurs et dimensions des éléments de jeu sont centralisées dans game_settings.py, permettant des modifications rapides et cohérentes.
<br/><br/>
La gestion des scores et sauvegardes est assurée par SQLite, avec deux bases de données séparées pour plus d’organisation. Les meilleurs scores sont stockés dans scores.db, tandis que game.db conserve l’état de la partie pour permettre une reprise ultérieure.
<br/><br/>
Le jeu est également conçu pour être évolutif grâce à des fonctionnalités supplémentaires, comme la génération aléatoire de cartes et un système de détection de proximité pour les ennemis. Ces derniers se déplacent de manière aléatoire mais peuvent aussi détecter et s’approcher du joueur si celui-ci entre dans un rayon de quatre cases, ajoutant une couche d’intelligence artificielle au comportement des ennemis.
<br/><br/>
Enfin, pour enrichir l’expérience de jeu, nous avons intégré un système de score : chaque déplacement réduit le score du joueur, l’encourageant ainsi à terminer le plus rapidement possible pour maximiser ses points. Ce score est enregistré dans la base de données des scores une fois la partie terminée, permettant aux joueurs de suivre leur progression.
</p>

<br/>

# <center> - Spécificités du projet -

<p style="text-align:justify;">
Chaque aspect du jeu (gestion du joueur, des bombes, du plateau, des menus et de la base de données) est isolé dans un module spécifique (game.py, player.py, bomb.py, plate.py, menu.py, db.py).
<br/><br/>
Utilisation de la bibliothèque Pygame pour l’affichage graphique, la gestion des événements (déplacements, explosions) et l’interface du jeu.
<br/><br/>
Support du mode multijoueur permettant à deux joueurs de jouer en simultané sur le même écran.
<br/><br/>
Les scores sont stockés dans scores.db, permettant de suivre les meilleures performances des joueurs. Sauvegarde de partie : L’état du jeu est sauvegardé permettant aux joueurs de reprendre une partie là où ils l’ont laissée.
<br/><br/>
Chaque déplacement du joueur réduit le score de quelques points, encourageant les joueurs à atteindre leurs objectifs rapidement pour maximiser leur score final. Le score est automatiquement sauvegardé à la fin de la partie, permettant d’établir un classement des meilleurs scores.
<br/><br/>
Les ennemis se déplacent de manière aléatoire tout en étant capables de détecter le joueur s’il se trouve à une distance euclidienne de quatre cases ou moins. Ce système de détection encourage le joueur à élaborer des stratégies pour éviter les ennemis ou les attirer dans des pièges.
<br/><br/>
Possibilité de générer un plateau de jeu aléatoire avec des murs cassables et incassables disposés de manière irrégulière, offrant une expérience de jeu renouvelée à chaque partie. La taille du plateau est configurable dans les paramètres, permettant de varier la difficulté et les stratégies.
</p>

<br/>

# <center> - Problèmes rencontrés -

<p style="text-align:justify;">
Au cours du projet, plusieurs défis ont émergé.
<br/>
Tout d'abord, la gestion des déplacements simultanés pour un mode multijoueur s'est révélée complexe, car il fallait éviter que les joueurs puissent occuper la même case, tout en s'assurant que les commandes puissent être lues sans conflit. La synchronisation des ennemis pour qu’ils se déplacent vers les joueurs sans les "téléporter" ou qu’ils ne se chevauchent pas a également posé problème, notamment en raison des ajustements nécessaires pour une IA de poursuite tout en préservant des déplacements aléatoires lorsque les joueurs étaient hors de portée.
<br/><br/>
Ensuite, la gestion du chronomètre pour la durée limite de jeu a demandé plusieurs ajustements, surtout pour assurer que le temps s’écoule de manière réaliste (Non implenter dans la sauvegarde lors de la restauration d'une partie).
<br/><br/>
Enfin, la répartition des fonctionnalités entre différents fichiers pour un code structuré et maintenable, tout en facilitant les interactions, a été un exercice de précision pour garantir la fluidité du jeu.
</p>

<br/>

# <center> - Axes d'amélioration -

<p style="text-align:justify;">
Pour améliorer le projet à l’avenir, plusieurs axes peuvent être envisagés. 
<br/>
D’abord, une optimisation de l’IA des ennemis pourrait renforcer l’expérience de jeu. Par exemple, en adaptant leur comportement pour mieux anticiper les mouvements des joueurs ou en ajoutant des stratégies d’encerclement, les ennemis deviendraient plus imprévisibles et stimulants.
<br/><br/>
Un autre axe d'amélioration serait d'ajouter un système de niveaux, avec des difficultés progressives et des plateaux variés, incluant peut-être des obstacles spécifiques ou des zones à effets particuliers.
<br/><br/>
De plus, une meilleure gestion du chronomètre, intégrant des options pour modifier la durée de partie ou ajouter des bonus de temps, rendrait le gameplay plus flexible.
<br/><br/>
Enfin, pour la maintenance et l’évolution du code, la mise en place de tests unitaires pour chaque fonctionnalité clé permettrait de sécuriser les mises à jour et les nouvelles fonctionnalités sans risque de régression.
</p>
<br/><br/>
