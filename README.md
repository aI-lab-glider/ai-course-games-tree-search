# Lab 02 - adversarial search

Adversarial search is an AI technique used to find the best move for a player in a two-player game 🤖🕹️. It involves exploring the game tree to determine the optimal move for one player while minimizing the opponent's chances of winning 👀🎲. Adversarial search algorithms, such as minimax and alpha-beta pruning, were commonly used for game playing 🎮. Recent developments in adversarial search actively use Monte Carlo algorithms combined with Reinforcement learning (e.g. Alpha Go) 🤖🤝. Overall, adversarial search is an important tool for developing intelligent systems that can make optimal decisions in competitive environments 🧠💻.

# TODO: 

Search for `TODO` text in the repository with CTRL+F and replace it with you code written according to it.


## How To Submit Solutions

* [ ] Clone repository: git clone:
    ```bash
    git clone <repository url>
    ```
* [ ] Complete TODOS the exercises
* [ ] Commit your changes
    ```bash
    git add <path to the changed files>
    git commit -m <commit message>
    ```
* [ ] Push changes to your repository main branch
    ```bash
    git push -u origin master
    ```

The rest will be taken care of automatically. You can check the `GRADE.md` file for your grade / test results. Be aware that it may take some time (up to one hour) till this file

## How To Run

This class requires Python with version at least 3.8.
Recommended way to run is to create a virtual environment first:
 
- `python -m venv adversarial-search`
- `source adversarial-search/bin/activate`

Then install required packages:
- `pip install -r requirements.txt`

After that configure `main.py`:

- specify `game` (see `games` folder)
- specify algorithm (see `algorithm` folder) 

and run the file.


Also, you can run a tournament between bots, by configuring file `tournament.py`.
In tournament a match is played between all configured bots for every configured game and results in the following output:

![image](https://user-images.githubusercontent.com/21079319/221435950-18cb0b7b-15be-439e-b021-f30c0d018bb8.png)


You will see a summary with total wins for every engaged bot and a table presenting statistics for bot vs bot clashes.
