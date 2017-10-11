# MineSweeper
This is an agent to automatically detect all mines in a map consisting of clues and mines.
## There are 4 parts for this program
* Map: to generate a map consisting of clues and mines if given row, col and mines.
* User: to judge if agent win or lose, and give agent the clue number.
* Agent: to play the minesweeper as a man, during this process, it stores and updates all interesting information and analysize to give next click.
* Visualizaton: to display agent's each click event.
## Logics behind the agent
Denote point A and point B
* Mark all A's undetected neighbours as safe squares if len(A's mines) is equal to A's clue number.
* Mark all A's undetected neighbours as mines if A's clue number is equal to len(A's mines) + len(A's undetected neighbours).
* Mark all [A's undetected neighbours - B's undetected neighbours] as mines if [A's number - len(A's mines)] > [B's number - len(B's mines)] and len(A's undetected neighbours - B's undetected neighbours) is equal to [A's number - len(A's mines)] - [B's number - len(B's mines)]
* Mark all [A's undetected neighbours - B's undetected neighbours] as safe squares if A's undetected neighbours contains B's undetected neighbours totally and [A's number - len(A's mines)] = [B's number - len(B's mines)] 
## How to run?
* First, install all dependent packages.
* Second, run visualize.py
