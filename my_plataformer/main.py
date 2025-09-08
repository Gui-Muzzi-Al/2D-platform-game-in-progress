import pygame, os
from levels import PLATAFORM_LIST
from config import WIDTH, HEIGHT

FPS = 60

import sys, os

import sys, os
import pygame

def resource_path(rel_path):
    """Retorna o caminho absoluto do recurso dentro ou fora do EXE."""
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS
    else:
        base = os.path.dirname(__file__)
    return os.path.join(base, rel_path)

def load_sound(rel_path):
    """Carrega e retorna um objeto Sound empacotado."""
    full_path = resource_path(rel_path)
    return pygame.mixer.Sound(full_path)

def load_idle_frames(path):
    frames = []
    full_path = resource_path(path)
    for fname in sorted(os.listdir(full_path)):
        if fname.endswith('.png'):
            img = pygame.image.load(os.path.join(full_path, fname)).convert_alpha()
            frames.append(img)
    return frames

def load_run_frames(path):
    frames = []
    full_path = resource_path(path)
    for fname in sorted(os.listdir(full_path)):
        if fname.endswith('.png'):
            img = pygame.image.load(os.path.join(full_path, fname)).convert_alpha()
            frames.append(img)
    return frames

def load_jump_frames(path):
    frames = []
    full_path = resource_path(path)
    for fname in sorted(os.listdir(full_path)):
        if fname.endswith('.png'):
            img = pygame.image.load(os.path.join(full_path, fname)).convert_alpha()
            frames.append(img)
    return frames

class Player(pygame.sprite.Sprite):
    def __init__(self, animations, pos):
        super().__init__()

        # inicializa mixer antes de carregar sons
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # carrega som de pulo
        self.jump_sound = load_sound('assets/jump.wav')

        # validações das animações…
        self.anims = animations
        self.state = 'idle'
        self.index = 0
        self.timer = 0
        self.anim_speed = 100
        self.image = self.anims[self.state][0]
        self.rect = self.image.get_rect(topleft=pos)

        # física
        self.speed_x = 5
        self.facing_right = True
        self.vel_y = 0

    def update(self, dt, platforms):
        keys = pygame.key.get_pressed()

        moving = False
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
            moving = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
            moving = True
            self.facing_right = True

        # pulo: toca self.jump_sound em vez de criar novo objeto
        if keys[pygame.K_SPACE] and self.on_ground(platforms):
            self.vel_y = -15
            self.jump_sound.play()

        # gravidade
        self.vel_y += 1
        self.rect.y += self.vel_y

        # colisão vertical
        for plat in platforms:
            if self.rect.colliderect(plat) and self.vel_y > 0:
                self.rect.bottom = plat.top
                self.vel_y = 0

        # escolhe estado de animação
        if not self.on_ground(platforms):
            new_state = 'jump'
        elif moving:
            new_state = 'run'
        else:
            new_state = 'idle'

        if new_state != self.state:
            self.state = new_state
            self.index = 0
            self.timer = 0

        # atualiza frame
        self.timer += dt
        frames = self.anims[self.state]
        if self.timer >= self.anim_speed:
            self.timer -= self.anim_speed
            self.index = (self.index + 1) % len(frames)
        self.image = frames[self.index]

    def on_ground(self, platforms):
        self.rect.y += 1
        grounded = any(self.rect.colliderect(p) for p in platforms)
        self.rect.y -= 1
        return grounded

def main():
    pygame.init()
    # inicializa mixer cedo para efeitos futuros
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    run_frames  = load_run_frames("assets/run")
    jump_frames = load_jump_frames("assets/jump")
    idle_frames = load_idle_frames("assets/idle")

    animations = {
        "idle": idle_frames,
        "jump": jump_frames,
        "run" : run_frames
    }

    player = Player(animations, pos=(50, HEIGHT-100))
    platforms = [pygame.Rect(x, y, w, h) for x, y, w, h in PLATAFORM_LIST]
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        dt = clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        all_sprites.update(dt, platforms)

        screen.fill((135, 206, 235))
        for plat in platforms:
            pygame.draw.rect(screen, (34,139,34), plat)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()