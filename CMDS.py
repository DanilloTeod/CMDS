import math
import matplotlib.pyplot as plt
import os
import time
import numpy as np
import imageio.v2 as imageio
import json

# Data: 03/11/24
# Updated: 31/07/25

init = time.time()

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def generate_points_wout_superposition(num_points, limit_x, limit_y, radiu_min, radiu_max, max_attempt=1000000):
    pontos = []
    attempts = 0
    
    while len(pontos) < num_points and attempts < max_attempt: 
        new_x = np.random.uniform(radiu_max, limit_x - radiu_max)
        new_y = np.random.uniform(radiu_max, limit_y - radiu_max)
        new_radiu = np.random.uniform(radiu_min, radiu_max)
        
        new_point = (float(f"{new_x:.6f}"), float(f"{new_y:.6f}"), float(f"{new_radiu:.6f}"))
        
        sobrepoe = False  

        for px, py, pr in pontos:
            center_distance = distance((new_x, new_y), (px, py))
            sum_radius = new_radiu + pr
            if center_distance < sum_radius:
                sobrepoe = True
                break 

        if not sobrepoe:
            pontos.append(new_point)

        attempts += 1

    return pontos

def moviment_particle(xo, yo, vpx, vpy, deltat):
    xp = xo + vpx * deltat
    yp = yo + vpy * deltat
    return (xp, yp)

def mj(pr, radiu_max, me):
    m2 = 2e12*(1+((pr-1)/radiu_max))*me
    return m2

def x_y_real(x, y):
    xr = x*2.5e-4
    yr = y*2.5e-4
    return xr, yr

def return_x_y(xr, yr):
    xp = xr/(2.5e-4)
    yp = yr/(2.5e-4)
    return xp, yp

def vp_line(vpx, vpy, dx, dy, xp, yp, x2, y2, m2, vp2x, vp2y):
    gamma = math.atan2(vpy, vpx)
    theta = math.atan2(dy, dx)
    phi = theta - gamma
    vo = math.sqrt(vpx**2 + vpy**2)

    M_cte = 2*m2/(me+m2)
    
    xr, yr = x_y_real(xp, yp)
    x2r, y2r = x_y_real(x2, y2)

    vpx = vpx - M_cte *((((vpx-vp2x)*(xr - x2r) +((vpy - vp2y)*(yr - y2r))))*(xr-x2r))/((xr-x2r)**2+(yr-y2r)**2)
    vpy = vpy - M_cte *((((vpx-vp2x)*(xr - x2r) +((vpy - vp2y)*(yr - y2r))))*(yr-y2r))/((xr-x2r)**2+(yr-y2r)**2)
    
    vpx_line = vo*math.sin(phi)
    vpy_line = vo*math.cos(phi)

    return vpx_line, vpy_line, xr, yr

def vp2_line(vp2y, vp2x, vpx, vpy, dx, dy, xp, yp, x2, y2, m2, me):
    vp2y, vp2x = 0, 0
    gamma = math.atan2(vp2y, vp2x)
    theta = math.atan2(dy, dx)
    phi = theta - gamma
    vo = math.sqrt(vp2x**2 + vp2y**2)

    xr, yr = x_y_real(xp, yp)
    x2r, y2r = x_y_real(x2, y2)
    
    M_cte_2 = 2*me/(me+m2)
    vp2x = vp2x - M_cte_2 *((((vp2x-vpx)*(x2r - xr) +((vp2y - vpy)*(y2r - yr))))*(x2r-xr))/((x2r-xr)**2+(y2r-yr)**2)
    vp2y = vp2y - M_cte_2 *((((vp2x-vpx)*(x2r - xr) +((vp2y - vpy)*(y2r - yr))))*(y2r-yr))/((x2r-xr)**2+(y2r-yr)**2)

    if vo == 0.0:
        vp2x_line, vp2y_line = vp2x, vp2y
    else:
        vp2x_line, vp2y_line = vp2x, vp2y

    return vp2x_line, vp2y_line, x2r, y2r

def collision(pontos, xp, yp, rp, radiu_min):
    for px, py, pr in pontos:
        dx = xp - px
        dy = yp - py
        center_distance = math.sqrt(dx**2 + dy**2)
        sum_radius = rp + pr
        
        if center_distance < sum_radius+radiu_min*0.3:
            return True, dx, dy, px, py, pr

    return False, 0, 0, 0, 0, 0


# inicia as variaveis armazenadas no json
with open("parameters.json", "r") as f:
    config = json.load(f)

# atrubuicao variaveis com uso do json
num_points = config["num_points"]
limit_x = config["limit_x"]
limit_y = config["limit_y"]
radiu_min = config["radiu_min"]
radiu_max = config["radiu_max"]
xo = config["xo"]
yo = config["yo"]
vpx = config["vpx"]
vpy = config["vpy"]
vp2x = config["vp2x"]
vp2y = config["vp2y"]
vp2x_aux = config["vp2x_aux"]
vp2y_aux = config["vp2y_aux"]
rp = config["rp"]
me = config["me"]
deltat = config["deltat"]
deltat2 = config["deltat2"]
frame_count = config["frame_count"]
num_falling_particles = config["num_falling_particles"] # numero de eletrons
spacing = config["spacing"] # espacamento entre os eletrons, ajusatar dps pra tds ficarem centralizados

falling_particles = []
# formato de "gota"
rows = [1, 2, 4, 4, 2]  # n particulas permitidas em cada linha
dy = 2 # espaçamento vertical entre linhas
dx = 1 # espaçamento horizontal entre partículas
x_start = xo # poss base de x
y_start = yo # pos base y

for row_index, num_in_row in enumerate(rows):
    y_pos = y_start + row_index * dy
    
    # centralizar partic. em torno de x_start
    x_first = x_start - (num_in_row - 1) * dx / 2
    
    for j in range(num_in_row):
        x_pos = x_first + j * dx
        falling_particles.append({
            'xp': x_pos,
            'yp': y_pos,
            'vpx': vpx,
            'vpy': vpy,
            'rp': rp,
            'trajectory': [(x_pos, y_pos)],
            'collided': False
        })


# gera particulas do tipo2
points = generate_points_wout_superposition(num_points, limit_x, limit_y, radiu_min, radiu_max)

# salva coordenadas e raios 
with open("coord.txt", "w") as arquivo:
    for x, y, raio in points:
        arquivo.write(f"{x:.4f} {y:.4f} {raio:.4f}\n")

with open("radius.txt", "w") as arquivo:
    for x, y, raio in points:
        arquivo.write(f"{raio:.1f}\n")

print(f"Total Particles: {len(points)}")
print(f"Total Falling Particles: {len(falling_particles)}")
# Inicialização do tracker de colisões em particulas do tipo 2
collision_tracker = {i: [] for i in range(len(points))} # dicionário onde a chave é o índice da partícula fixa, e o valor é uma lista de elétrons que colidiram com ela

# [Diretório para frames]
# os.system("cd frames && rm -rf *.png")
frames_dir = "frames"
os.makedirs(frames_dir, exist_ok=True)

while any(p['yp'] > 0 for p in falling_particles):
    # armazena colisoes deste frame
    frame_collisions = []
    
    # movimenta todos os eletrons
    for i, particle in enumerate(falling_particles):
        if particle['yp'] > 0:
            particle['xp'], particle['yp'] = moviment_particle(particle['xp'], particle['yp'], particle['vpx'], particle['vpy'], deltat)
            particle['trajectory'].append((particle['xp'], particle['yp']))
    
    # verifica colisões antes de processa-las 
    for i, particle in enumerate(falling_particles):
        if particle['yp'] > 0:
            collided, dx, dy, x2, y2, r2 = collision(points, particle['xp'], particle['yp'], particle['rp'], radiu_min)
            if collided:
                part_id = points.index((x2, y2, r2))
                frame_collisions.append({
                    'electron_id': i,
                    'particle_id': part_id,
                    'electron': particle,
                    'fixed_particle': (x2, y2, r2),
                    'dx': dx,
                    'dy': dy})
    
    # processamento de colisao
    for col in frame_collisions: # verifica se o eletron bateu em alguma particula 2
        i = col['electron_id']
        part_id = col['particle_id']
        particle = col['electron']
        x2, y2, r2 = col['fixed_particle']
        
        # calculo massa real 
        m2 = mj(r2, radiu_max, me)
        
        # calcula vel. dos eletrons e p2
        vp2x, vp2y, x2r, y2r = vp2_line(vp2y, vp2x, particle['vpx'], particle['vpy'], col['dx'], col['dy'], particle['xp'], particle['yp'], x2, y2, m2, me)
        
        # att velocidade eletrons
        particle['vpx'], particle['vpy'], xr, yr = vp_line(particle['vpx'], particle['vpy'], col['dx'], col['dy'], particle['xp'], particle['yp'], x2, y2, m2, vp2x, vp2y)
        
        # atualiza valores arb dos eletrons
        particle['xp'], particle['yp'] = return_x_y(xr, yr)
        
        #  acumula deslocamento da partícula tipo 2 (colisão múltipla no frame)
        x2_new, y2_new = return_x_y(x2r, y2r) #retorno para os pontos arbitrarios
        xf2, yf2 = moviment_particle(x2_new, y2_new, vp2x, vp2y, deltat2)
        dx_final = xf2 - x2
        dy_final = yf2 - y2
        collision_tracker[part_id].append((dx_final, dy_final))
        
        if particle['vpy'] > 0:
            particle['vpy'] = -abs(particle['vpy'])
    
    #  aplica deslocamentos acumulados por partícula após processar todas as colisões do frame
    for part_id, displacements in collision_tracker.items():
        if displacements:  # só se houve colisões para essa partícula
            x0, y0, r2 = points[part_id]
            dx_total = sum(d[0] for d in displacements)
            dy_total = sum(d[1] for d in displacements)
            xf = x0 + dx_total
            yf = y0 + dy_total
            points[part_id] = (xf, yf, r2)
            collision_tracker[part_id] = []  # limpa para o próximo frame
            
    # feracao de frames
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, limit_x)
    ax.set_ylim(0, limit_y)
    ax.set_aspect('equal')
    
    # graos de areia
    for x, y, raio in points:
        circle = plt.Circle((x, y), raio, color="green", alpha=0.6)
        ax.add_patch(circle)
    
    # salva as trajetoria dos eletrons
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'red', 'blue', 'green', 'purple', 'orange', 'red', 'blue', 'green', 'purple', 'orange']
    for i, particle in enumerate(falling_particles):
        for j, (x, y) in enumerate(particle['trajectory']):
            color = colors[i] if j == len(particle['trajectory']) - 1 else "black"
            circ = plt.Circle((x, y), particle['rp'], color=color, alpha=0.9)
            ax.add_patch(circ)
    
    ax.set_title(f"Frame {frame_count}")
    plt.grid(True)
    plt.savefig(f"{frames_dir}/frame_{frame_count:04d}.png", dpi=100)
    plt.close()
    frame_count += 1

for i, particle in enumerate(falling_particles):
    with open(f"trajectory_particle_fall_{i}.txt", "w") as f:
        for x, y in particle['trajectory']:
            f.write(f"{x:.4f} {y:.4f}\n")

with imageio.get_writer(f"multiple_particle_fall_{len(points)}.gif", mode='I', duration=0.1) as writer:
    for i in range(frame_count):
        frame_path = f"{frames_dir}/frame_{i:04d}.png"
        if os.path.exists(frame_path):
            image = imageio.imread(frame_path)
            writer.append_data(image)

print(f"GIF saved as: multiple_particle_fall_{len(points)}.gif")
end = time.time()
print(f"Time: {end - init:.4f} sec.")

# verifica e salva particulas tipo 2 coladas (sobrepostas)
overlapped = []
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        x1, y1, r1 = points[i]
        x2, y2, r2 = points[j]
        dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        if dist < (r1 + r2):  # tem sobreposição
            overlapped.append((x1, y1, r1))
            overlapped.append((x2, y2, r2))

# remove duplicatas mantendo a ordem
unique_overlapped = []
for p in overlapped:
    if p not in unique_overlapped:
        unique_overlapped.append(p)

with open("overlapped_particles.txt", "w") as f:
    for x, y, r in unique_overlapped:
        f.write(f"{x:.4f} {y:.4f} {r:.4f}\n")

print(f"Overlapped Particles Saved: {len(unique_overlapped)}")



