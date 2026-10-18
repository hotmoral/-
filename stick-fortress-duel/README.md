# Stick Fortress Duel

1:1 browser artillery duel inspired by classic turn-based ballistic games, using skeletal stick-figure fighters instead of cannons.

## Play loop
- Create a room and share its URL.
- First two visitors become BLACK and WHITE; additional visitors spectate.
- On your turn: move a limited distance, select a weapon, set angle/power, fire.
- Wind changes every turn.
- Grenades deform terrain; all weapons have distinct ballistic profiles.
- Reduce the opponent to 0 HP to win; both players can request a rematch.

## Run
```bash
npm install
npm start
```
Open `http://localhost:3000`.
