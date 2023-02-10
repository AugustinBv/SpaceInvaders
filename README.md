# SpaceInvaders
Project led by BOIDSON Hugues and BOUVEAU Augustin
Press Start to start the game, the player appears at the bottom of the screen and is controlled by the directionnal keys. Spacebar to shoot on the aliens appearing at the top of the screen, of which only a set amount can shoot at the player. The player is protected by walls that can only be hit by the random shots of the aliens. 
Cheat codes are available to increase the number of lives, increase the points or destroy all aliens at once. The cheat codes are implemented by listening and registering the keys pressed in a FIFO list.




Projet réalisé par Hugues BOISDON et Augustin BOUVEAU

Le jeu se lance en appuyant sur Start, un joueur apparaît en bas de l'écran et est contrôlable à l'aide des touches directionnelles. La touche espace sert à tirer un missile sur les aliens qui apparaissent en haut de l'écran et dont seulement un certain nombre peut tirer. Le joueur est protégé par des murs que les missiles du joueur traversent mais pas ceux des aliens qui tirent de manière aléatoire d'après un paramètre défini.
Des cheat code sont disponibles pour augmenter le nombre de vies du joueur, augmenter son nombre de points ou encore détruire tous les ennemis d'un coup.
On peut retrouver l'implémentation d'une file dans les cheat codes, les inputs au clavier autres que les touches directionnelles et la barre d'espace sont enregistrés, chaque nouveau caractère prennant la dernière place de la liste et poussant le premier de la liste, le supprimant (FIFO)
