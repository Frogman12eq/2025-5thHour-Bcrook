code = r"""
import math
import random
import sys
from dataclasses import dataclass
from typing import List, Tuple, Optional

import pygame
Vec2 = pygame.math.Vector2

# ==============================
# CONFIG
# ==============================
WIDTH, HEIGHT = 1280, 720
FPS = 60
GRAVITY = 2200.0
AIR_FRICTION = 0.95
GROUND_FRICTION = 0.85

PLAYER_SPEED = 520.0
PLAYER_JUMP_SPEED = 980.0
PLAYER_FLY_ACCEL = 1600.0
PLAYER_MAX_FLY_SPEED = 800.0
PLAYER_DASH_SPEED = 1100.0

PLAYER_MAX_HEALTH = 1000
PLAYER_MAX_ENERGY = 300

PUNCH_COOLDOWN = 0.25
HEAT_VISION_DPS = 250
HEAT_VISION_ENERGY_DRAIN = 120 # per second
BREATH_ENERGY_DRAIN = 90       # per second
BLOCK_REDUCTION = 0.65

ENEMY_BASE_HEALTH = {
    'thug': 250,
    'drone': 160,
    'brute': 450
}
ENEMY_DAMAGE = {
    'thug': 70,
    'drone': 50,
    'brute': 110
}

SPAWN_INTERVAL = 6.0  # seconds between waves
SPAWN_TABLE = [
    [('thug', 3), ('drone', 1)],
    [('thug', 4), ('drone', 2)],
    [('thug', 4), ('brute', 1)],
    [('thug', 5), ('drone', 2), ('brute', 1)],
    [('thug', 6), ('drone', 3), ('brute', 2)],
]
MAX_WAVES = len(SPAWN_TABLE)

# Colors
WHITE  = (245, 245, 245)
BLACK  = ( 15,  15,  20)
RED    = (230,  50,  60)
BLUE   = ( 60, 120, 255)
CYAN   = ( 90, 220, 255)
YELLOW = (255, 220,  80)
GREEN  = ( 80, 220, 120)
ORANGE = (255, 150,  60)
PURPLE = (170,  90, 255)
GRAY   = (130, 130, 140)

# ==============================
# UTILS
# ==============================
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def rect_from_pos_size(pos: Vec2, size: Tuple[int, int]) -> pygame.Rect:
    return pygame.Rect(int(pos.x), int(pos.y), size[0], size[1])

def line_intersects_rect(p1: Vec2, p2: Vec2, rect: pygame.Rect) -> bool:
    return rect.clipline(p1.x, p1.y, p2.x, p2.y)

def draw_text(surface, text, pos, size=20, color=WHITE, center=False):
    font = pygame.font.SysFont("consolas", size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (int(pos[0]), int(pos[1]))
    else:
        rect.topleft = (int(pos[0]), int(pos[1]))
    surface.blit(surf, rect)

# ==============================
# GAME OBJECTS
# ==============================
@dataclass
class Particle:
    pos: Vec2
    vel: Vec2
    life: float
    color: Tuple[int,int,int]
    radius: float

    def update(self, dt):
        self.life -= dt
        self.pos += self.vel * dt
        self.vel *= 0.98
        self.radius = max(0, self.radius - 40 * dt)

    def draw(self, surf, cam):
        if self.life <= 0 or self.radius <= 0: return
        pygame.draw.circle(surf, self.color, (int(self.pos.x - cam.x), int(self.pos.y - cam.y)), int(self.radius))

class Projectile:
    def __init__(self, start: Vec2, end: Vec2, dps: float, duration: float, color: Tuple[int,int,int], width: int=4):
        self.start = Vec2(start)
        self.end = Vec2(end)
        self.dps = dps
        self.duration = duration
        self.t = 0.0
        self.color = color
        self.width = width

    def update(self, dt):
        self.t += dt

    @property
    def alive(self):
        return self.t < self.duration

    def draw(self, surf, cam):
        alpha = clamp(1.0 - self.t / self.duration, 0.2, 1.0)
        col = tuple(int(c * alpha) for c in self.color)
        pygame.draw.line(surf, col,
                         (int(self.start.x - cam.x), int(self.start.y - cam.y)),
                         (int(self.end.x - cam.x), int(self.end.y - cam.y)), self.width)
        # impact spark
        pygame.draw.circle(surf, col, (int(self.end.x - cam.x), int(self.end.y - cam.y)), 6, 1)

class Entity:
    def __init__(self, x, y, w, h):
        self.pos = Vec2(x, y)
        self.size = (w, h)
        self.vel = Vec2(0,0)
        self.on_ground = False
        self.health = 100
        self.max_health = 100
        self.facing = 1  # 1 right, -1 left
        self.dead = False

    @property
    def rect(self):
        return rect_from_pos_size(self.pos, self.size)

    def apply_gravity(self, dt):
        self.vel.y += GRAVITY * dt

    def move_and_collide(self, dt, platforms: List[pygame.Rect]):
        # X
        self.pos.x += self.vel.x * dt
        r = self.rect
        for p in platforms:
            if r.colliderect(p):
                if self.vel.x > 0:
                    self.pos.x = p.left - self.size[0]
                elif self.vel.x < 0:
                    self.pos.x = p.right
                self.vel.x = 0
                r = self.rect
        # Y
        self.pos.y += self.vel.y * dt
        r = self.rect
        self.on_ground = False
        for p in platforms:
            if r.colliderect(p):
                if self.vel.y > 0:
                    self.pos.y = p.top - self.size[1]
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.pos.y = p.bottom
                self.vel.y = 0
                r = self.rect

    def take_damage(self, amount: float, knockback: Vec2=Vec2()):
        if self.dead: return
        self.health -= amount
        self.vel += knockback
        if self.health <= 0:
            self.dead = True

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 54, 90)
        self.color = BLUE
        self.max_health = PLAYER_MAX_HEALTH
        self.health = PLAYER_MAX_HEALTH
        self.energy = PLAYER_MAX_ENERGY
        self.combo = 0
        self.combo_timer = 0.0
        self.invuln_timer = 0.0
        self.punch_cd = 0.0
        self.is_blocking = False
        self.flying = False
        self.dashing = False
        self.dash_timer = 0.0
        self.heat_vision_on = False
        self.breath_on = False

    def update(self, dt, keys, platforms, projectiles: List[Projectile], particles: List[Particle],
               enemies: List['Enemy']):
        # Timers
        self.punch_cd = max(0.0, self.punch_cd - dt)
        self.combo_timer = max(0.0, self.combo_timer - dt)
        if self.combo_timer == 0.0: self.combo = 0
        self.invuln_timer = max(0.0, self.invuln_timer - dt)
        self.dash_timer = max(0.0, self.dash_timer - dt)

        # Movement input
        accel = 0.0
        if keys[pygame.K_a]: accel -= 1.0
        if keys[pygame.K_d]: accel += 1.0
        self.facing = 1 if accel > 0 else (-1 if accel < 0 else self.facing)

        if self.flying:
            # omni movement
            target = Vec2(accel * PLAYER_MAX_FLY_SPEED, self.vel.y)
            if keys[pygame.K_w]: target.y = -PLAYER_MAX_FLY_SPEED
            elif keys[pygame.K_s]: target.y = PLAYER_MAX_FLY_SPEED
            else: target.y = 0
            # accelerate toward target
            delta = target - self.vel
            self.vel += delta * clamp(PLAYER_FLY_ACCEL * dt / (abs(delta.length())+1e-5), 0, 1)
            self.vel = Vec2(clamp(self.vel.x, -PLAYER_MAX_FLY_SPEED, PLAYER_MAX_FLY_SPEED),
                            clamp(self.vel.y, -PLAYER_MAX_FLY_SPEED, PLAYER_MAX_FLY_SPEED))
            self.vel *= 0.99
        else:
            # ground/air
            self.vel.x += accel * PLAYER_SPEED * dt
            if self.on_ground:
                self.vel.x *= GROUND_FRICTION
            else:
                self.vel.x *= AIR_FRICTION
            if keys[pygame.K_w] and self.on_ground:
                self.vel.y = -PLAYER_JUMP_SPEED
            self.apply_gravity(dt)

        # Toggle flying
        for event in pygame.event.get(pygame.KEYDOWN):
            pass  # drained by main; keep placeholder

        # Abilities
        self.is_blocking = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if keys[pygame.K_j] and self.punch_cd == 0:
            self.melee_attack(enemies, particles)
            self.punch_cd = PUNCH_COOLDOWN

        # Heat vision: hold K
        self.heat_vision_on = keys[pygame.K_k] and self.energy > 0
        if self.heat_vision_on:
            self.energy = max(0, self.energy - HEAT_VISION_ENERGY_DRAIN * dt)
            start = Vec2(self.rect.centerx, self.rect.centery - 18)
            dir_vec = Vec2(self.facing, -0.08)  # slight upward angle
            end = start + dir_vec * 900
            beam = Projectile(start, end, HEAT_VISION_DPS, 0.06, ORANGE, width=5)
            projectiles.append(beam)

        # Breath: hold L
        self.breath_on = keys[pygame.K_l] and self.energy > 0
        if self.breath_on:
            self.energy = max(0, self.energy - BREATH_ENERGY_DRAIN * dt)
            self.super_breath(enemies, particles)

        # Move and collide
        self.move_and_collide(dt, platforms)

        # Regenerate energy slowly when not using powers
        if not self.heat_vision_on and not self.breath_on:
            self.energy = min(PLAYER_MAX_ENERGY, self.energy + 40 * dt)

    def melee_attack(self, enemies, particles):
        # simple 3-hit chain based on combo timer
        self.combo = min(3, self.combo + 1)
        self.combo_timer = 0.8
        reach = 64 + self.combo * 6
        dmg = 120 + self.combo * 30
        kb = 380 + self.combo * 60
        arc_center = Vec2(self.rect.centerx + self.facing * (self.size[0]//2 + 12), self.rect.centery)
        hit_any = False
        for e in enemies:
            if e.dead: continue
            to_e = Vec2(e.rect.centerx - arc_center.x, e.rect.centery - arc_center.y)
            if (0 <= to_e.x * self.facing) and (to_e.length() < reach) and abs(to_e.y) < 60:
                e.take_damage(dmg, Vec2(self.facing*kb, -180))
                e.stun(0.2 + 0.05*self.combo)
                hit_any = True
                # hit particles
                for _ in range(12):
                    p = Particle(Vec2(e.rect.centerx, e.rect.centery),
                                 Vec2(random.uniform(-180,180), random.uniform(-220,-60)),
                                 0.4, YELLOW, random.uniform(2,4))
                    particles.append(p)
        if hit_any:
            # swoosh
            for _ in range(10):
                p = Particle(arc_center + Vec2(self.facing*20, 0) + Vec2(random.uniform(-10,10), random.uniform(-10,10)),
                             Vec2(self.facing*random.uniform(200,320), random.uniform(-60,60)),
                             0.18, WHITE, random.uniform(2,3))
                particles.append(p)

    def super_breath(self, enemies, particles):
        # Cone push
        origin = Vec2(self.rect.centerx + self.facing * (self.size[0]//2 + 8), self.rect.centery - 10)
        cone_angle = math.radians(28)
        max_dist = 360
        for e in enemies:
            if e.dead: continue
            v = Vec2(e.rect.centerx - origin.x, e.rect.centery - origin.y)
            dist = v.length()
            if dist == 0: continue
            if dist < max_dist:
                dir_f = Vec2(self.facing, 0)
                ang = dir_f.angle_to(v)
                if abs(ang) < math.degrees(cone_angle):
                    force = (1.0 - dist/max_dist)
                    e.vel += Vec2(self.facing * (600 * force + 120), -120 * force)
                    e.stun(0.2)
                    e.take_damage(8 * force)
        # breath mist particles
        for _ in range(30):
            p = Particle(origin + Vec2(random.uniform(0, 40), random.uniform(-12,12))*self.facing,
                         Vec2(self.facing*random.uniform(300, 480), random.uniform(-40, 40)),
                         0.25, CYAN, random.uniform(2,4))
            particles.append(p)

    def toggle_fly(self):
        self.flying = not self.flying
        if self.flying:
            self.vel.y = 0

    def draw(self, surf, cam):
        r = self.rect
        # cape
        cape_pts = [(r.left - self.facing*8 - cam.x, r.top + 16 - cam.y),
                    (r.left - self.facing*40 - cam.x, r.top + 40 - cam.y),
                    (r.left - self.facing*18 - cam.x, r.bottom - 10 - cam.y)]
        pygame.draw.polygon(surf, RED, cape_pts)
        pygame.draw.rect(surf, self.color, (r.x - cam.x, r.y - cam.y, r.w, r.h), border_radius=6)
        # emblem
        pygame.draw.rect(surf, YELLOW, (r.centerx - 6 - cam.x, r.y + 22 - cam.y, 12, 10), border_radius=2)
        # eyes glow if heat vision
        if self.heat_vision_on:
            pygame.draw.circle(surf, ORANGE, (r.centerx + self.facing*12 - cam.x, r.y + 24 - cam.y), 4)

class Enemy(Entity):
    def __init__(self, x, y, etype='thug'):
        if etype == 'drone':
            super().__init__(x, y, 48, 32)
        elif etype == 'brute':
            super().__init__(x, y, 64, 96)
        else:
            super().__init__(x, y, 48, 80)
        self.etype = etype
        self.color = ORANGE if etype=='drone' else (PURPLE if etype=='brute' else GREEN)
        self.max_health = ENEMY_BASE_HEALTH[etype]
        self.health = self.max_health
        self.state = 'idle'
        self.state_timer = 0.0
        self.attack_cd = random.uniform(0.4, 1.1)
        self.stun_timer = 0.0
        self.shoot_cd = 0.0

    def ai(self, dt, player: Player, platforms: List[pygame.Rect], particles: List[Particle], enemy_bullets: List[Projectile]):
        if self.dead: return
        self.state_timer += dt
        self.attack_cd = max(0.0, self.attack_cd - dt)
        self.stun_timer = max(0.0, self.stun_timer - dt)
        self.shoot_cd = max(0.0, self.shoot_cd - dt)
        if self.stun_timer > 0:
            # limited control
            self.apply_gravity(dt)
            self.move_and_collide(dt, platforms)
            return

        to_player = Vec2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        dist = to_player.length()
        if dist > 0: self.facing = 1 if to_player.x > 0 else -1

        if self.etype == 'drone':
            # hover around player and shoot
            target = Vec2(player.rect.centerx - self.size[0]/2 - 140*self.facing, player.rect.centery - 160)
            desired = target - self.pos
            self.vel += desired * 0.9 * dt
            self.vel *= 0.92
            self.move_and_collide(dt, platforms)
            # shoot
            if dist < 720 and self.shoot_cd == 0.0:
                start = Vec2(self.rect.centerx, self.rect.centery)
                dir_vec = (player.rect.center - self.rect.center)
                if dir_vec.length() == 0: dir_vec = Vec2(self.facing,0)
                dir_vec = Vec2(dir_vec).normalize()
                end = start + dir_vec * 900
                bullet = Projectile(start, end, dps=120, duration=0.08, color=GREEN, width=3)
                enemy_bullets.append(bullet)
                self.shoot_cd = 1.2
        else:
            # ground enemies
            if dist > 80:
                self.apply_gravity(dt)
                self.vel.x += self.facing * 460 * dt
                self.vel.x *= 0.86
                self.move_and_collide(dt, platforms)
            else:
                self.vel.x *= 0.8
                self.apply_gravity(dt)
                self.move_and_collide(dt, platforms)
                if self.attack_cd == 0.0 and self.on_ground:
                    self.attack_cd = 1.1 if self.etype=='brute' else 0.7
                    # melee hitbox
                    reach = 64 if self.etype=='thug' else 84
                    dmg = ENEMY_DAMAGE[self.etype]
                    kb = 200 if self.etype=='thug' else 320
                    arc_center = Vec2(self.rect.centerx + self.facing*(self.size[0]//2+10), self.rect.centery)
                    v = Vec2(player.rect.centerx - arc_center.x, player.rect.centery - arc_center.y)
                    if (0 <= v.x * self.facing) and (v.length() < reach) and abs(v.y) < 60:
                        final_dmg = dmg * (0.35 if player.is_blocking else 1.0)
                        player.take_damage(final_dmg, Vec2(self.facing*kb, -140))
                        # particles
                        for _ in range(10):
                            particles.append(Particle(Vec2(player.rect.centerx, player.rect.centery),
                                                      Vec2(random.uniform(-180,180), random.uniform(-220,-20)),
                                                      0.25, RED, random.uniform(2,3)))

    def stun(self, t):
        self.stun_timer = max(self.stun_timer, t)

    def draw(self, surf, cam):
        r = self.rect
        pygame.draw.rect(surf, self.color, (r.x - cam.x, r.y - cam.y, r.w, r.h), border_radius=5)
        # health bar
        hpw = int( r.w * clamp(self.health / self.max_health, 0, 1) )
        pygame.draw.rect(surf, RED, (r.x - cam.x, r.y - 10 - cam.y, r.w, 6), border_radius=3)
        pygame.draw.rect(surf, GREEN, (r.x - cam.x, r.y - 10 - cam.y, hpw, 6), border_radius=3)

# ==============================
# LEVEL / WORLD
# ==============================
def build_level() -> Tuple[List[pygame.Rect], List[pygame.Rect]]:
    platforms: List[pygame.Rect] = []
    hazards: List[pygame.Rect] = []

    ground = pygame.Rect(-2000, HEIGHT - 80, 5000, 160)
    platforms.append(ground)
    # scattered platforms
    platforms += [
        pygame.Rect(-200, HEIGHT-240, 300, 24),
        pygame.Rect(180, HEIGHT-360, 240, 24),
        pygame.Rect(520, HEIGHT-260, 300, 24),
        pygame.Rect(980, HEIGHT-200, 300, 24),
        pygame.Rect(1350, HEIGHT-340, 260, 24)
    ]
    # hazards (electric floor patches)
    hazards += [
        pygame.Rect(300, HEIGHT-80, 120, 10),
        pygame.Rect(860, HEIGHT-80, 120, 10),
    ]
    return platforms, hazards

# ==============================
# GAME
# ==============================
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Man of Tomorrow - Python Combat Prototype")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.platforms, self.hazards = build_level()
        self.player = Player(80, HEIGHT - 300)
        self.enemies: List[Enemy] = []
        self.particles: List[Particle] = []
        self.projectiles: List[Projectile] = []   # player beams
        self.enemy_beams: List[Projectile] = []   # enemy shots

        self.camera = Vec2(0,0)
        self.wave_index = 0
        self.spawn_timer = 1.5
        self.score = 0
        self.game_over = False

    def spawn_wave(self):
        if self.wave_index >= MAX_WAVES: return
        plan = SPAWN_TABLE[self.wave_index]
        for etype, count in plan:
            for _ in range(count):
                x = random.choice([-800, -400, 500, 1200, 1600]) + random.randint(-80,80)
                y = HEIGHT - 400 if etype=='drone' else HEIGHT - 200
                self.enemies.append(Enemy(x, y, etype))
        self.wave_index += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_f:
                    self.player.toggle_fly()
                if event.key == pygame.K_SPACE:
                    # quick dash
                    self.player.vel.x = self.player.facing * PLAYER_DASH_SPEED

    def update(self, dt):
        if self.game_over:
            return

        self.handle_events()
        keys = pygame.key.get_pressed()

        # Waves
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_wave()
            self.spawn_timer = SPAWN_INTERVAL

        # Update player
        self.player.update(dt, keys, self.platforms, self.projectiles, self.particles, self.enemies)

        # Enemy AI
        for e in self.enemies:
            e.ai(dt, self.player, self.platforms, self.particles, self.enemy_beams)

        # Projectiles influence
        for beam in self.projectiles:
            beam.update(dt)
            # damage enemies hit by beam
            for e in self.enemies:
                if e.dead: continue
                if line_intersects_rect(beam.start, beam.end, e.rect):
                    e.take_damage(beam.dps * dt, Vec2(self.player.facing*40, -20))
        for beam in self.enemy_beams:
            beam.update(dt)
            if line_intersects_rect(beam.start, beam.end, self.player.rect):
                dmg = 60 * dt
                if self.player.is_blocking: dmg *= (1.0 - BLOCK_REDUCTION)
                self.player.take_damage(dmg, Vec2(0, -40))

        # Hazards
        for hz in self.hazards:
            if self.player.rect.colliderect(hz):
                self.player.take_damage(40 * dt, Vec2(0, -20))
                if random.random()<0.12:
                    self.particles.append(Particle(Vec2(self.player.rect.centerx, hz.top),
                                                   Vec2(random.uniform(-80,80), random.uniform(-120,-40)),
                                                   0.2, CYAN, random.uniform(2,3)))

        # Remove dead beams
        self.projectiles = [b for b in self.projectiles if b.alive]
        self.enemy_beams = [b for b in self.enemy_beams if b.alive]

        # Particles
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0 and p.radius > 0]

        # Cull dead enemies, add score
        alive = []
        for e in self.enemies:
            if e.dead:
                self.score += 25 if e.etype=='thug' else (40 if e.etype=='drone' else 80)
                for _ in range(14):
                    self.particles.append(Particle(Vec2(e.rect.centerx, e.rect.centery),
                                                   Vec2(random.uniform(-220,220), random.uniform(-260, -60)),
                                                   0.5, ORANGE, random.uniform(2,4)))
            else:
                alive.append(e)
        self.enemies = alive

        # Camera follow
        target_cam_x = self.player.rect.centerx - WIDTH/2
        target_cam_y = self.player.rect.centery - HEIGHT/2
        self.camera.x += (target_cam_x - self.camera.x) * 0.08
        self.camera.y += (target_cam_y - self.camera.y) * 0.08

        # Death
        if self.player.health <= 0:
            self.game_over = True

    def draw_bg(self, surf):
        surf.fill(BLACK)
        # parallax skyline
        for i, y in enumerate([HEIGHT-300, HEIGHT-260, HEIGHT-220]):
            offset = self.camera.x * (0.2 + i*0.1)
            for x in range(-2000, 3000, 160):
                rect = pygame.Rect(int(x - offset % 160), y, 120, 400)
                pygame.draw.rect(surf, (30+10*i, 30+10*i, 46+10*i), rect)
        # ground line
        pygame.draw.line(surf, (60,60,70), (0, HEIGHT-80 - self.camera.y), (WIDTH, HEIGHT-80 - self.camera.y), 2)

    def draw_level(self, surf):
        for p in self.platforms:
            pr = pygame.Rect(p.x - self.camera.x, p.y - self.camera.y, p.w, p.h)
            pygame.draw.rect(surf, (70, 80, 90), pr, border_radius=6)
        for hz in self.hazards:
            hr = pygame.Rect(hz.x - self.camera.x, hz.y - self.camera.y, hz.w, hz.h)
            pygame.draw.rect(surf, CYAN, hr)

    def draw_hud(self, surf):
        # Health
        x, y = 24, 20
        w = 360
        pygame.draw.rect(surf, RED, (x, y, w, 18), border_radius=9)
        hpw = int(w * clamp(self.player.health / self.player.max_health, 0, 1))
        pygame.draw.rect(surf, GREEN, (x, y, hpw, 18), border_radius=9)
        draw_text(surf, f"HP: {int(self.player.health)} / {PLAYER_MAX_HEALTH}", (x+8, y-2), size=18)

        # Energy
        y2 = y + 30
        pygame.draw.rect(surf, (40,80,120), (x, y2, w, 14), border_radius=7)
        enw = int(w * clamp(self.player.energy / PLAYER_MAX_ENERGY, 0, 1))
        pygame.draw.rect(surf, CYAN, (x, y2, enw, 14), border_radius=7)
        draw_text(surf, f"Energy: {int(self.player.energy)} / {PLAYER_MAX_ENERGY}", (x+8, y2-4), size=16)

        # Score / wave
        draw_text(surf, f"Score: {self.score}", (WIDTH-220, 20), size=22)
        draw_text(surf, f"Wave: {min(self.wave_index+1, MAX_WAVES)}/{MAX_WAVES}", (WIDTH-220, 46), size=18)

        # Controls
        controls = [
            "Move: A/D   Jump: W   Fly Toggle: F   Dash: Space",
            "Punch: J   Heat Vision (hold): K   Super Breath (hold): L   Block: Shift",
        ]
        draw_text(surf, controls[0], (24, HEIGHT-56), size=18)
        draw_text(surf, controls[1], (24, HEIGHT-32), size=18)

        if self.game_over:
            draw_text(surf, "YOU'RE DOWN! Press Esc to Exit", (WIDTH/2, HEIGHT/2), 36, ORANGE, center=True)

    def draw(self):
        self.draw_bg(self.screen)
        self.draw_level(self.screen)

        # Beams under/over?
        for beam in self.enemy_beams:
            beam.draw(self.screen, self.camera)

        for e in self.enemies:
            e.draw(self.screen, self.camera)

        for beam in self.projectiles:
            beam.draw(self.screen, self.camera)

        self.player.draw(self.screen, self.camera)

        for p in self.particles:
            p.draw(self.screen, self.camera)

        self.draw_hud(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.update(dt)
            self.draw()
        pygame.quit()

def main():
    try:
        Game().run()
    except Exception as e:
        print("Error:", e)
        pygame.quit()
        sys.exit(1)

if __name__ == '__main__':
    main()
"""
# Write the code to a file
with open('/mnt/data/superman_game.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Created /mnt/data/superman_game.py")