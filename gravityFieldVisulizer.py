import pygame, gravityFields, time, math


pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
running = True
width = 20
height = 20



def display():
    screen.fill((0, 0, 0))
    data_range = gravityFields.data_range
    difference = data_range[1]-data_range[0]
    for x in range(width):
        for y in range(height):
            mx = x * 400/width
            my = y * 400/height
            value = gravityFields.getFieldAtPoint(mx, my)
            value = min(max(value, data_range[0]), data_range[1])
            color_value = 255 * (value-data_range[0]) / difference
            pygame.draw.rect(screen, (color_value, color_value, color_value), (mx,my,400/width,400/height))
    pygame.draw.circle(screen, "red", gravityFields.pos, gravityFields.radius)

    pygame.display.flip()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display()

    clock.tick(60)

pygame.quit()