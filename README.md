# Python Chess Engine & Bot

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [TODO](#todo)
* [Showcase](#showcase)

## General info
I have been playing chess since elementary school and ever since learning to code, have wanted to make my own Chess Engine. This is my take on a chess engine. Eventually, I will also create a chess bot, so that you can play against a computer.

## Technologies
* Python 3.9.13
* pygame 2.5.2

## TODO
- [X] Implement removal of non-valid moves when in Check or if a piece is pinned
- [X] Implement Checkmate, and Stalemate (no valid moves but not in check)
- [X] Cleaning up the code - Separate into different files and functions
- [X] Use class objects to simplify function calls and code
- [ ] Create Chess AI/Bot
  - [X] Random Bot
  - [ ] Minimax
  - [ ] Machine learning / Neural Networks
- [ ] Menu to allow users to:
  - [X] Select player vs player/computer or even computer vs computer
  - [ ] Select type of AI for computer player
  - [X] Whether white is on the top or bottom
  - [ ] Customize look (i.e. colours, images)
- [ ] Menus
  - [X] Main Menu
  - [ ] How to Play
  - [ ] Game Review
- [ ] Optimize code
- [ ] Add timer for blitz/speed chess
- [ ] Create a chess notation system to keep a record of chess games
- [ ] Add a function to open and view old games by pulling up the chess notation logs
- [ ] Implement Stalemate due to threefold repetition (same position occurs three times during the game) or fifty-move rule (50 moves without capture/pawn advancement)

## Showcase
### Checkmate
<p align="center">
  <img src="../main/Screenshots/Chess - Checkmate.gif">
</p>

### Castling
<p align="center">
  <img src="../main/Screenshots/Chess - Castling.gif">
</p>

### Pawn Promotion
<p align="center">
  <img src="../main/Screenshots/Chess - Pawn Promotion.gif">
</p>

### En Passant
<p align="center">
  <img src="../main/Screenshots/Chess - En Passant.gif">
</p>
