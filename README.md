[Mestre dos Monstros](https://ragnarok-disguise.herokuapp.com/)
===================
**GAME IS BEING HOSTED HERE** : [https://ragnarok-disguise.herokuapp.com/](https://ragnarok-disguise.herokuapp.com/)

Mestre dos Monstros is a fun and interactive web-based game that tests your knowledge about various game monsters. Players must correctly identify monsters from their favorite games to earn points and compete for the top spot on the leaderboard.

![master_of_monsters](/monster_master.png)

Features
--------

-   Simple and easy-to-use interface
-   Multiple games to choose from (Ragnarok Online Monsters, Pokémon, and more to come)
-   Three leaderboards: Overall, Monthly, and Weekly
-   Customizable player name

Getting Started
---------------

### Prerequisites

-   Python 3.10
-   Django 4.2

### Installation

1.  Clone the repository:

```bash
git clone https://github.com/jfsjunqueira/ragnarok-disguise.git
```
2.  Change into the project directory:
```bash
cd ragnarok-disguise
```
3.  Set up a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # for Linux and macOS
venv\Scripts\activate  # for Windows`
```
4.  Install the required dependencies:
```bash
pip install -r requirements.txt
```
5.  Apply migrations and create the database:
```bash
python manage.py migrate
```
6.  Run the development server:
```bash
python manage.py runserver
```
7.  Open your web browser and visit <http://127.0.0.1:8000/> to start playing the game!

Usage
-----

1.  Enter your player name and choose a game from the available options.
2.  Click "Start" to begin the game.
3.  Identify the monster shown on the screen and type in its name.
4.  You have three lives, and each incorrect guess will cost you one life. The game ends when you run out of lives.
5.  Compete for the highest score on the Overall, Monthly, and Weekly leaderboards.

Contributing
------------

We welcome contributions to improve Mestre dos Monstros! Please follow these steps to contribute:

1.  Fork the repository on GitHub.
2.  Create a new branch with a descriptive name.
3.  Make your changes in the new branch.
4.  Submit a pull request with a clear description of the changes and any relevant context.

License
-------

This project is licensed under the MIT License. See the [LICENSE](https://chat.openai.com/chat/LICENSE) file for details.

Acknowledgements
----------------

-   Developed by Johny Junqueira
-   Game data and images are the property of their respective owners