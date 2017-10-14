# Mine
This is an agent to automatically detect all mines in a map consisting of clues and mines.
## There are 4 parts for this program.
* Map: to generate a map consisting of clues and mines if given row, col and mines.
* User: to judge if agent win or lose, and give agent the clue number.
* Agent: to play the minesweeper as a man, during this process, it stores and updates all interesting information and analysize to give next click.
* Visualizaton: to display agent's each click event.
## Logics behind the agent.
Denote point A and point B
* Mark all A's undetected neighbours as safe squares if len(A's mines) is equal to A's clue number.
* Mark all A's undetected neighbours as mines if A's clue number is equal to len(A's mines) + len(A's undetected neighbours).
* Mark all [A's undetected neighbours - B's undetected neighbours] as mines if [A's number - len(A's mines)] > [B's number - len(B's mines)] and len(A's undetected neighbours - B's undetected neighbours) is equal to [A's number - len(A's mines)] - [B's number - len(B's mines)]
* Mark all [A's undetected neighbours - B's undetected neighbours] as safe squares if A's undetected neighbours contains B's undetected neighbours totally and [A's number - len(A's mines)] = [B's number - len(B's mines)] 
## What the agent will do when there is no safe squares to click at all?
Denote p as a percentage given before.
* If the number of unvisited squares outside clue number circle divides the number all squares, the agent will randomly click a square outside the clue number circle.
* Else, the agent will pick an unvisited square with highest priority(an unvisited square with most clue squares around it) to mark it as a mine, then update knowledge accordingly.  
## Different reasons of failure.
It's obvious that the agent may have kinds of faults that cause it to lose the game according to its strategy that deals with uncertainty.
* Type A: Randomly click a square with a mine in it.
* Type B: Mark a fake mine.
## Some running screenshots of the agent on 30*30 map with different number of mines.
### Notations 
* Squares with **GREY** color represents that this square has **NOT** been visited.
* Squares with **YELLOW** color and **NO TEXT** represents that this square has been sweeped correctly by agent.
* Squares with **YELLOW** color and **T** represents that the agent clicks the square with a mine in it and loses the game.
* Squares with **YELLOW** color and **F** represents that the agent marks a fake mine.
* Squares with **ORANGE** color and **NUMBER** represents that this clue square has been clicked by agent. 
* Squares with **WHITE** color and **NO TEXT** represents that this is an empty square(with clue number 0).
### The percentage of mines is 0.11(100 mines)
**success screenshot**
![30_30_100 0 11 _success](https://user-images.githubusercontent.com/30862009/31573331-7a3968fe-b087-11e7-9605-9150a4392ef5.png)  
**randomClick failure screenshot**
![30_30_100 0 11 _randomclick_failure](https://user-images.githubusercontent.com/30862009/31573339-ae74be3e-b087-11e7-8942-121b692fdeb1.png)
### The percentage of mines is 0.17(150 mines)
**success screenshot**
![30_30_150 0 17 _success](https://user-images.githubusercontent.com/30862009/31573342-c684b402-b087-11e7-82c9-e1861f2870f4.png)  
**randomClick failure**
![30_30_150 0 17 _randomclick_failure](https://user-images.githubusercontent.com/30862009/31573346-d6bf069c-b087-11e7-844e-fed029452b0c.png)
**markFakeMine failure**
![30_30_150 0 17 _markfakemine_failure](https://user-images.githubusercontent.com/30862009/31573354-eeb41a08-b087-11e7-8401-e06fc1003abc.png)
### The percentage of mines is 0.22(200 mines)
**randomClick failure**
![30_30_200 0 22 _randomclick_failure](https://user-images.githubusercontent.com/30862009/31573363-158d8f10-b088-11e7-834b-352492c2351f.png)
**markFakeMine failure1**
![30_30_200 0 22 _markfakemine_failure1](https://user-images.githubusercontent.com/30862009/31573369-2733dcd8-b088-11e7-86ca-e75b4e9d39c4.png)
**markFakeMine failure2**
![30_30_200 0 22 _markfakemine_failure2](https://user-images.githubusercontent.com/30862009/31573371-300a9144-b088-11e7-86a5-ff593eefc37f.png)
### The percentage of mines is 0.28(250 mines)
**randomClick failure**
![30_30_250 0 28 _randomclick_failure](https://user-images.githubusercontent.com/30862009/31573374-3e2600a6-b088-11e7-9318-25e24fc86c56.png)  
### Analysis of these screenshots
**As we can see, when p is small, the agent will sweeper all the mines with higher possibility, as the p goes up, the agent will do more calculations and has to deal with some uncentainty, and when p is high enough( higher than 0.25), the agent will hardly win the game because it's randomly click action will become dangerous.**
## How to run?
* First, install all dependent packages.
* Second, run visualize.py
