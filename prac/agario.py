import pygame, random, sys

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()

player_pos = [W//2, H//2]
player_r = 20
food = [[random.randint(0, W), random.randint(0, H)] for _ in range(50)]

def dist2(a, b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player_pos[1] -= 3
    if keys[pygame.K_s]: player_pos[1] += 3
    if keys[pygame.K_a]: player_pos[0] -= 3
    if keys[pygame.K_d]: player_pos[0] += 3

    for f in food[:]:
        if dist2(player_pos, f) < player_r**2:
            food.remove(f)
            player_r += 5

    screen.fill((30, 30, 30))
    for f in food:
        pygame.draw.circle(screen, (0, 255, 0), f, 4)
    pygame.draw.circle(screen, (0, 100, 255), player_pos, player_r)
    pygame.display.flip()
    clock.tick(60)
