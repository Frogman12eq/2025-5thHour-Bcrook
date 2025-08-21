code = r'''import math
import random
import sys
import pygame

# ---------------
# CONFIG
# ---------------
WIDTH, HEIGHT = 960, 540
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 64, 52)
GREEN = (46, 204, 113)
BLUE = (52, 152, 219)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
ORANGE = (230, 126, 34)
GREY = (100, 100, 100)

# ---------------
# SIMPLE UTILS
# ---------------
def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def vec_length(vx, vy):
    return math.hypot(vx, vy)

# ---------------
# GAME OBJECTS
# ---------------
class Particle:
    def __init__(self, x, y, vx, vy, radius, color, life):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.radius = radius
        self.color = color
        self.life = life

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        self.radius = max(0, self.radius - 10 * dt)

    def draw(self, surf, cam):
        if self.life > 0 and self.radius > 0:
            pygame.draw.circle(surf, self.color, (int(self.x - cam.x), int(self.y - cam.y)), max(1, int(self.radius)))

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def follow(self, target):
        # Center camera on player with soft clamp
        desired_x = target.x - WIDTH // 2 + target.w // 2
        desired_y = target.y - HEIGHT // 2 + target.h // 2
        self.x += (desired_x - self.x) * 0.08
        self.y += (desired_y - self.y) * 0.08

class Projectile:
    def __init__(self, x, y, dx, dy, speed, damage, color, radius=5, lifetime=1.2, friendly=True):
        self.x, self.y = x, y
        self.dx, self.dy = dx, dy
        self.speed = speed
        self.damage = damage
        self.color = color
        self.radius = radius
        self.life = lifetime
        self.friendly = friendly
        self.alive = True

        length = vec_length(dx, dy) or 1
        self.vx = (dx / length) * speed
        self.vy = (dy / length) * speed

    def rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), int(self.radius*2), int(self.radius*2))

    def update(self, dt, world_rect):
        if not self.alive: return
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        if self.life <= 0 or not world_rect.collidepoint(self.x, self.y):
            self.alive = False

    def draw(self, surf, cam):
        if not self.alive: return
        pygame.draw.circle(surf, self.color, (int(self.x - cam.x), int(self.y - cam.y)), int(self.radius))

class Entity:
    def __init__(self, x, y, w, h, color):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.color = color
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.max_hp = 100
        self.hp = self.max_hp
        self.invuln = 0.0

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def center(self):
        r = self.rect()
        return r.centerx, r.centery

    def take_damage(self, dmg, knockback=(0,0)):
        if self.invuln > 0: 
            return
        self.hp -= dmg
        self.invuln = 0.25
        self.vx += knockback[0]
        self.vy += knockback[1]

    def alive(self):
        return self.hp > 0

    def draw_healthbar(self, surf, cam):
        r = self.rect().move(-cam.x, -cam.y)
        pct = clamp(self.hp / self.max_hp, 0, 1)
        back = pygame.Rect(r.x, r.y - 10, r.w, 6)
        front = pygame.Rect(r.x, r.y - 10, int(r.w * pct), 6)
        pygame.draw.rect(surf, GREY, back, border_radius=3)
        pygame.draw.rect(surf, GREEN if pct > 0.35 else RED, front, border_radius=3)

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 36, 48, BLUE)
        self.speed = 280
        self.fly_speed = 360
        self.jump_power = -520
        self.gravity = 1400
        self.flying = False
        self.cool_punch = 0
        self.cool_laser = 0
        self.cool_dash = 0
        self.score = 0

    def input(self, keys):
        ax = 0
        ay = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            ax -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            ax += 1

        if self.flying:
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                ay -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                ay += 1

        return ax, ay

    def attack_rect(self, facing):
        # small rectangle in front for melee
        r = self.rect()
        if facing >= 0:
            return pygame.Rect(r.right, r.y + 8, 28, r.h - 16)
        else:
            return pygame.Rect(r.left - 28, r.y + 8, 28, r.h - 16)

    def update(self, dt, world_rect, keys, projectiles, particles):
        spd = self.fly_speed if self.flying else self.speed
        ax, ay = self.input(keys)

        # Timers
        if self.invuln > 0: self.invuln -= dt
        if self.cool_punch > 0: self.cool_punch -= dt
        if self.cool_laser > 0: self.cool_laser -= dt
        if self.cool_dash > 0: self.cool_dash -= dt

        # Change mode
        if keys[pygame.K_f]:
            self.flying = True
        if keys[pygame.K_g]:
            self.flying = False

        # Movement
        self.vx += ax * spd * 6 * dt
        if self.flying:
            self.vy += ay * spd * 6 * dt
            # air drag
            self.vx *= 0.90
            self.vy *= 0.90
        else:
            # gravity
            self.vy += self.gravity * dt
            self.vx *= 0.85

        # Clamp velocities
        maxv = 520 if self.flying else 380
        self.vx = clamp(self.vx, -maxv, maxv)
        self.vy = clamp(self.vy, -maxv, maxv)

        # Dashing
        if self.cool_dash <= 0 and keys[pygame.K_k]:
            # dash in movement direction or facing
            dirx = ax if ax != 0 else (1 if self.vx >= 0 else -1)
            diry = ay if self.flying and ay != 0 else 0
            mag = vec_length(dirx, diry)
            if mag == 0: 
                dirx = 1; diry = 0; mag = 1
            self.vx = (dirx / mag) * (maxv * 1.65)
            self.vy = (diry / mag) * (maxv * 1.65)
            self.cool_dash = 0.65
            # dash particles
            cx, cy = self.center()
            for _ in range(18):
                ang = random.uniform(0, math.pi * 2)
                sp = random.uniform(120, 260)
                particles.append(Particle(cx, cy, math.cos(ang)*sp, math.sin(ang)*sp, random.randint(2,5), BLUE, 0.4))

        # Apply movement
        self.x += self.vx * dt
        self.y += self.vy * dt

        # World bounds
        if self.x < world_rect.left:
            self.x = world_rect.left; self.vx = 0
        if self.x + self.w > world_rect.right:
            self.x = world_rect.right - self.w; self.vx = 0
        if self.y < world_rect.top:
            self.y = world_rect.top; self.vy = 0
        if self.y + self.h > world_rect.bottom:
            self.y = world_rect.bottom - self.h; self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Attacks
        facing = 1 if self.vx >= 0 else -1

        # Punch
        if self.cool_punch <= 0 and keys[pygame.K_SPACE]:
            self.cool_punch = 0.28
            # spawn punch particles
            ar = self.attack_rect(facing)
            cx, cy = ar.center
            for _ in range(10):
                ang = random.uniform(-0.6, 0.6) + (0 if facing>0 else math.pi)
                sp = random.uniform(140, 240)
                particles.append(Particle(cx, cy, math.cos(ang)*sp, math.sin(ang)*sp, random.randint(2,4), YELLOW, 0.25))
            self._pending_punch = (ar, 28, (facing*220, -80 if not self.flying else 0))
        else:
            self._pending_punch = None

        # Heat vision (J)
        if self.cool_laser <= 0 and keys[pygame.K_j]:
            self.cool_laser = 0.18
            # fire small fast projectile
            cx, cy = self.center()
            dirx = 1 if facing>0 else -1
            projectiles.append(Projectile(cx + dirx*22, cy-6, dirx, 0, 780, 10, RED, radius=4, lifetime=0.9, friendly=True))

class Enemy(Entity):
    def __init__(self, x, y, kind="grunt"):
        super().__init__(x, y, 34, 44, ORANGE if kind=="grunt" else PURPLE)
        self.kind = kind
        if kind == "grunt":
            self.max_hp = 50; self.hp = self.max_hp
            self.speed = 180
            self.damage = 8
            self.attack_cool = 0
        elif kind == "ranged":
            self.max_hp = 40; self.hp = self.max_hp
            self.speed = 140
            self.damage = 6
            self.shoot_cool = 1.2
            self.timer = random.uniform(0, 1.2)
        elif kind == "brute":
            self.w, self.h = 46, 58
            self.max_hp = 140; self.hp = self.max_hp
            self.speed = 120
            self.damage = 18
            self.attack_cool = 0

    def update(self, dt, player, world_rect, projectiles, particles):
        if self.invuln > 0: self.invuln -= dt

        # AI
        dx = (player.x + player.w/2) - (self.x + self.w/2)
        dy = (player.y + player.h/2) - (self.y + self.h/2)
        dist = max(1, math.hypot(dx, dy))

        if self.kind == "ranged":
            # keep distance, strafe a bit
            desired = 240
            if dist < desired - 40:
                self.vx -= (dx/dist) * self.speed * dt
                self.vy -= (dy/dist) * self.speed * dt
            elif dist > desired + 40:
                self.vx += (dx/dist) * self.speed * dt
                self.vy += (dy/dist) * self.speed * dt
            else:
                self.vx *= 0.9; self.vy *= 0.9

            # shoot
            self.timer -= dt
            if self.timer <= 0:
                self.timer = self.shoot_cool
                cx, cy = self.center()
                projectiles.append(Projectile(cx, cy, dx, dy, 360, 8, PURPLE, radius=6, lifetime=2.2, friendly=False))

        else:
            # chase
            self.vx += (dx/dist) * self.speed * dt
            self.vy += (dy/dist) * (self.speed * (0.7 if self.kind=="brute" else 1.0)) * dt

            # attack if close
            if dist < (70 if self.kind=="brute" else 50):
                if getattr(self, "attack_cool", 0) <= 0:
                    self.attack_cool = 0.9 if self.kind=="brute" else 0.7
                    # melee "hit"
                    if player.alive():
                        player.take_damage(self.damage, knockback=(dx/dist*160, -120))
                        # particles
                        cx, cy = player.center()
                        for _ in range(12):
                            ang = random.uniform(0, math.pi*2)
                            sp = random.uniform(90, 240)
                            particles.append(Particle(cx, cy, math.cos(ang)*sp, math.sin(ang)*sp, random.randint(2,5), RED, 0.35))
            else:
                self.attack_cool = max(0, getattr(self, "attack_cool", 0) - dt)

        # Damping and movement
        self.vx = clamp(self.vx, -260, 260)
        self.vy = clamp(self.vy, -260, 260)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.92
        self.vy *= 0.92

        # bounds
        if self.x < world_rect.left: self.x = world_rect.left; self.vx = abs(self.vx)
        if self.x + self.w > world_rect.right: self.x = world_rect.right - self.w; self.vx = -abs(self.vx)
        if self.y < world_rect.top: self.y = world_rect.top; self.vy = abs(self.vy)
        if self.y + self.h > world_rect.bottom: self.y = world_rect.bottom - self.h; self.vy = -abs(self.vy)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Super Hero: Sky Clash (Python)")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.bigfont = pygame.font.SysFont("consolas", 64, bold=True)

        self.reset()

    def reset(self):
        self.world_rect = pygame.Rect(-1200, -600, 2400, 1600)
        self.player = Player(0, 0)
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.camera = Camera()
        self.spawn_timer = 0
        self.wave = 1
        self.game_over = False
        self.boss_spawned = False
        self.highscore = 0

    def spawn_enemy_wave(self):
        count = 3 + self.wave
        for _ in range(count):
            kind_roll = random.random()
            if kind_roll < 0.65:
                kind = "grunt"
            elif kind_roll < 0.9:
                kind = "ranged"
            else:
                kind = "brute"
            x = random.randint(self.world_rect.left+60, self.world_rect.right-60)
            y = random.randint(self.world_rect.top+60, self.world_rect.bottom-60)
            self.enemies.append(Enemy(x, y, kind=kind))

    def spawn_boss(self):
        boss = Enemy(self.world_rect.centerx - 30, self.world_rect.top + 80, kind="brute")
        boss.max_hp = 400; boss.hp = boss.max_hp
        boss.w, boss.h = 58, 72
        boss.speed = 140
        boss.damage = 24
        self.enemies.append(boss)
        self.boss_spawned = True

    def handle_collisions(self):
        # projectiles vs entities
        for p in self.projectiles:
            if not p.alive: continue
            if p.friendly:
                for e in self.enemies:
                    if e.alive() and p.rect().colliderect(e.rect()):
                        e.take_damage(p.damage, knockback=(p.vx*0.06, p.vy*0.06))
                        p.alive = False
                        cx, cy = p.x, p.y
                        for _ in range(8):
                            ang = random.uniform(0, math.pi*2)
                            sp = random.uniform(60, 160)
                            self.particles.append(Particle(cx, cy, math.cos(ang)*sp, math.sin(ang)*sp, random.randint(2,4), YELLOW, 0.25))
            else:
                if self.player.alive() and p.rect().colliderect(self.player.rect()):
                    self.player.take_damage(p.damage, knockback=(p.vx*0.05, -60))
                    p.alive = False

        # player melee
        if getattr(self.player, "_pending_punch", None):
            ar, dmg, kb = self.player._pending_punch
            for e in self.enemies:
                if e.alive() and ar.colliderect(e.rect()):
                    e.take_damage(dmg, knockback=kb)
                    # impact particles
                    cx, cy = ar.center
                    for _ in range(12):
                        ang = random.uniform(0, math.pi*2)
                        sp = random.uniform(120, 260)
                        self.particles.append(Particle(cx, cy, math.cos(ang)*sp, math.sin(ang)*sp, random.randint(2,5), ORANGE, 0.3))

        # enemies touching player
        for e in self.enemies:
            if e.alive() and self.player.alive() and e.rect().colliderect(self.player.rect()):
                self.player.take_damage(4, knockback=(math.copysign(140, self.player.x - e.x), -80))

    def update(self, dt):
        keys = pygame.key.get_pressed()
        if self.game_over:
            if keys[pygame.K_r]:
                self.reset()
            return

        self.player.update(dt, self.world_rect, keys, self.projectiles, self.particles)

        # update enemies
        for e in self.enemies:
            if e.alive():
                e.update(dt, self.player, self.world_rect, self.projectiles, self.particles)

        # cull dead
        alive_enemies = []
        for e in self.enemies:
            if e.alive():
                alive_enemies.append(e)
            else:
                self.player.score += 10 if e.kind != "brute" else 25
                # death burst
                cx, cy = e.center()
                for _ in range(18):
                    ang = random.uniform(0, math.pi*2)
                    sp = random.uniform(140, 320)
                    self.particles.append(Particle(cx, cy, math.cos(ang)*sp, math.sin(ang)*sp, random.randint(2,6), ORANGE, 0.5))
        self.enemies = alive_enemies

        # update projectiles
        for p in self.projectiles:
            p.update(dt, self.world_rect)
        self.projectiles = [p for p in self.projectiles if p.alive]

        # particles
        for part in self.particles:
            part.update(dt)
        self.particles = [pa for pa in self.particles if pa.life > 0 and pa.radius > 0]

        # spawn logic
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_timer = max(0.5, 2.5 - self.wave * 0.08)
            # occasional wave
            if random.random() < 0.10:
                self.wave += 1
                self.spawn_enemy_wave()
            else:
                # trickle spawn
                kind = random.choices(["grunt","ranged","brute"], weights=[0.6,0.3,0.1])[0]
                x = random.choice([self.world_rect.left+40, self.world_rect.right-80])
                y = random.randint(self.world_rect.top+80, self.world_rect.bottom-80)
                self.enemies.append(Enemy(x, y, kind=kind))

        # boss condition
        if not self.boss_spawned and self.player.score >= 200:
            self.spawn_boss()

        # camera follow
        self.camera.follow(self.player)

        # collisions
        self.handle_collisions()

        # game over
        if not self.player.alive():
            self.highscore = max(self.highscore, self.player.score)
            self.game_over = True

    def draw_grid(self, surf, cam):
        # parallax backgrounds as simple moving bands
        surf.fill((18, 22, 28))
        for i, speed in enumerate([0.2, 0.4, 0.7]):
            offset = int((-cam.x * speed) % 160)
            color = (24 + i*10, 28 + i*10, 40 + i*10)
            for x in range(-160, WIDTH+160, 160):
                pygame.draw.rect(surf, color, pygame.Rect(x+offset, 0, 140, HEIGHT))

        # world bounds
        wr = self.world_rect.move(-cam.x, -cam.y)
        pygame.draw.rect(surf, (60, 66, 80), wr, 4, border_radius=12)

    def draw(self):
        self.draw_grid(self.screen, self.camera)

        # draw particles behind
        for pa in self.particles:
            pa.draw(self.screen, self.camera)

        # draw projectiles
        for p in self.projectiles:
            p.draw(self.screen, self.camera)

        # draw entities
        def draw_entity(e, outline_color):
            r = e.rect().move(-self.camera.x, -self.camera.y)
            # invuln blink
            if e.invuln > 0 and int(pygame.time.get_ticks()*0.02) % 2 == 0:
                return
            pygame.draw.rect(self.screen, e.color, r, border_radius=6)
            pygame.draw.rect(self.screen, outline_color, r, 2, border_radius=6)
            e.draw_healthbar(self.screen, self.camera)

        draw_entity(self.player, (200, 220, 255))
        for e in self.enemies:
            draw_entity(e, (255, 215, 180) if e.kind=="grunt" else (200, 180, 255))

        # UI
        hp_txt = self.font.render(f"HP: {int(self.player.hp)}/{self.player.max_hp}", True, WHITE)
        score_txt = self.font.render(f"Score: {self.player.score}", True, WHITE)
        wave_txt = self.font.render(f"Wave: {self.wave}", True, WHITE)
        self.screen.blit(hp_txt, (14, 12))
        self.screen.blit(score_txt, (14, 36))
        self.screen.blit(wave_txt, (14, 60))

        tips = [
            "Move: WASD / Arrow keys",
            "Fly: F to start, G to stop",
            "Punch: SPACE   |   Heat Vision: J",
            "Dash: K   |   Restart: R (when down)",
        ]
        for i, t in enumerate(tips):
            txt = self.font.render(t, True, GREY)
            self.screen.blit(txt, (WIDTH - txt.get_width() - 14, 12 + i*22))

        if self.game_over:
            s1 = self.bigfont.render("YOU FELL!", True, RED)
            s2 = self.font.render("Press R to restart", True, WHITE)
            s3 = self.font.render(f"Score: {self.player.score}  Highscore: {self.highscore}", True, WHITE)
            self.screen.blit(s1, (WIDTH//2 - s1.get_width()//2, HEIGHT//2 - 80))
            self.screen.blit(s2, (WIDTH//2 - s2.get_width()//2, HEIGHT//2 - 8))
            self.screen.blit(s3, (WIDTH//2 - s3.get_width()//2, HEIGHT//2 + 24))

        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update(dt)
            self.draw()

if __name__ == "__main__":
    Game().run()
'''

path = "/mnt/data/super_hero_game.py"
with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"Wrote game to {path}")