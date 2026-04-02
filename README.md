# CMDS
Simulação de dinâmica molecular clássica

---

## 🇧🇷 Português

### Visão Geral
Simulação de um conjunto de partículas em queda (modeladas como elétrons em formação de "gota") colidindo com partículas fixas distribuídas aleatoriamente num espaço 2D. As colisões seguem conservação de momento linear com massas distintas. O resultado é exportado como um GIF animado com as trajetórias e colisões.

### Pré-requisitos
```bash
pip install numpy matplotlib imageio
```

### Arquivos necessários
- `parameters.json` — arquivo de configuração com todos os parâmetros da simulação (deve estar na mesma pasta que o script).

### Como usar
1. Configure os parâmetros em `parameters.json`.
2. Execute o script principal:
```bash
python CMDS.py
```
3. O GIF animado será salvo na pasta raiz com o nome `multiple_particle_fall_<N>.gif`, onde `<N>` é o número de partículas fixas geradas.

### Arquivos gerados
| Arquivo | Descrição |
|---|---|
| `frames/` | Frames PNG de cada etapa da simulação |
| `coord.txt` | Coordenadas (x, y) e raios das partículas fixas |
| `radius.txt` | Raios das partículas fixas (apenas os valores, formato `.1f`) |
| `trajectory_particle_fall_<i>.txt` | Trajetória de cada partícula em queda (uma por arquivo) |
| `overlapped_particles.txt` | Partículas fixas que ficaram sobrepostas após as colisões |
| `multiple_particle_fall_<N>.gif` | Animação final da simulação |

### Parâmetros principais (`parameters.json`)
| Parâmetro | Descrição |
|---|---|
| `num_points` | Número de partículas fixas a gerar |
| `limit_x`, `limit_y` | Dimensões do domínio 2D |
| `radiu_min`, `radiu_max` | Intervalo de raios das partículas fixas |
| `xo`, `yo` | Posição base inicial das partículas em queda |
| `vpx`, `vpy` | Velocidade inicial das partículas em queda |
| `vp2x`, `vp2y` | Velocidade inicial das partículas fixas (geralmente 0) |
| `vp2x_aux`, `vp2y_aux` | Velocidades auxiliares das partículas fixas |
| `rp` | Raio das partículas em queda (elétrons) |
| `me` | Massa das partículas em queda |
| `deltat` | Passo de tempo do movimento |
| `deltat2` | Passo de tempo do deslocamento pós-colisão das partículas fixas |
| `frame_count` | Índice inicial dos frames |
| `num_falling_particles` | Número de partículas em queda (referência; a formação é definida no código) |
| `spacing` | Espaçamento entre as partículas em queda |

### Observações
- A formação das partículas em queda é definida em formato de "gota" diretamente no código (linhas com 1, 2, 4, 4, 2 partículas).
- Partículas fixas são geradas sem sobreposição inicial via tentativas aleatórias com limite de `max_attempt`.
- A massa das partículas fixas escala com o raio: `m2 = 2e12 * (1 + (r - 1) / radiu_max) * me`.
- O fator de escala entre coordenadas arbitrárias e reais é `2.5e-4` (usado nos cálculos de colisão).

---

## 🇬🇧 English

### Overview
Simulation of a group of falling particles (modeled as electrons in a "droplet" formation) colliding with randomly distributed fixed particles in a 2D space. Collisions follow linear momentum conservation with distinct masses. The result is exported as an animated GIF showing trajectories and collisions.

### Requirements
```bash
pip install numpy matplotlib imageio
```

### Required files
- `parameters.json` — configuration file with all simulation parameters (must be in the same folder as the script).

### How to use
1. Set the parameters in `parameters.json`.
2. Run the main script:
```bash
python CMDS.py
```
3. The animated GIF will be saved in the root folder as `multiple_particle_fall_<N>.gif`, where `<N>` is the number of fixed particles generated.

### Generated files
| File | Description |
|---|---|
| `frames/` | PNG frames for each simulation step |
| `coord.txt` | Coordinates (x, y) and radii of fixed particles |
| `radius.txt` | Radii of fixed particles only (`.1f` format) |
| `trajectory_particle_fall_<i>.txt` | Trajectory of each falling particle (one file each) |
| `overlapped_particles.txt` | Fixed particles that overlapped after collisions |
| `multiple_particle_fall_<N>.gif` | Final simulation animation |

### Main parameters (`parameters.json`)
| Parameter | Description |
|---|---|
| `num_points` | Number of fixed particles to generate |
| `limit_x`, `limit_y` | 2D domain dimensions |
| `radiu_min`, `radiu_max` | Radius range of fixed particles |
| `xo`, `yo` | Base initial position of falling particles |
| `vpx`, `vpy` | Initial velocity of falling particles |
| `vp2x`, `vp2y` | Initial velocity of fixed particles (usually 0) |
| `vp2x_aux`, `vp2y_aux` | Auxiliary velocities of fixed particles |
| `rp` | Radius of falling particles (electrons) |
| `me` | Mass of falling particles |
| `deltat` | Time step for movement |
| `deltat2` | Time step for post-collision displacement of fixed particles |
| `frame_count` | Starting frame index |
| `num_falling_particles` | Number of falling particles (reference; formation is defined in code) |
| `spacing` | Spacing between falling particles |

### Notes
- The falling particle formation is defined as a "droplet" shape directly in the code (rows of 1, 2, 4, 4, 2 particles).
- Fixed particles are generated without initial overlap via random attempts up to `max_attempt`.
- Fixed particle mass scales with radius: `m2 = 2e12 * (1 + (r - 1) / radiu_max) * me`.
- The scale factor between arbitrary and real coordinates is `2.5e-4` (used in collision calculations).

---

*Developed: 03/11/24 — Updated: 31/07/25*
