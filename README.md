# Survivors (Python + pygame)

Um jogo estilo *Vampire Survivors*: moves-te, a arma dispara sozinha, sobrevives a hordas, apanhas XP e escolhes melhorias.

## Como correr
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Controlos
- **WASD / setas**: mover
- **1 / 2 / 3**: escolher melhoria ao subir de nível
- **R**: recomeçar | **ESC**: sair

## Estrutura
| Ficheiro | Função |
|---|---|
| `main.py` | ponto de entrada |
| `survivors/settings.py` | constantes e balanceamento |
| `survivors/player.py` | jogador, vida, XP |
| `survivors/enemy.py` | inimigos e gemas de XP |
| `survivors/weapons.py` | arma automática e projéteis |
| `survivors/upgrades.py` | melhorias do level-up |
| `survivors/game.py` | loop principal, spawns, colisões, HUD |

## Ideias para evoluir
- [ ] Mais armas (chicote, órbita de facas, área de dano)
- [ ] Sprites e sons
- [ ] Boss a cada 5 minutos
- [ ] Menu inicial e high score guardado em ficheiro
- [ ] Otimizar colisões com uma grelha espacial
