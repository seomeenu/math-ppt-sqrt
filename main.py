import pygame
import sys

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("sqrt")

clock = pygame.time.Clock()

target = 10
actual_value = round(target**0.5, 2)
sqrtx = target/2
start = target
end = 0

history = []
def step():
    global sqrtx, start, end, anim, selected, scale_anim
    anim = 20
    scale_anim = 10
    selected = len(history)
    history.append(sqrtx)
    if sqrtx**2 > target:
        start = sqrtx
    else:
        end = sqrtx
    sqrtx = (end+start)/2
    
def move(mx):
    global selected, scale_anim
    if 0 <= selected+mx < len(history):
        scale_anim = 10
        selected += mx
    
zoom_x = 100
zoom_y = screen_height/(target*2)
offset_x = 0
offset_y = 0
cam_x = offset_x
cam_y = offset_y

font = pygame.font.Font("data/Freesentation-4Regular.ttf")
font_b = pygame.font.Font("data/Freesentation-7Bold.ttf", 40)
anim = 0
scale_anim = 0
selected = 0

while True:
    screen.fill("#ffffff")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                step()
            if event.key == pygame.K_RIGHT:
                move(1)
            if event.key == pygame.K_LEFT:
                move(-1)

    dt = clock.tick(60)/(1000/60)

    cam_x -= (cam_x-offset_x)/10*dt
    cam_y -= (cam_y-offset_y)/10*dt
    # print(cam_x, offset_x)

    for i, y in enumerate(history):
        x = i*zoom_x
        draw_x = x-cam_x+screen_width/2
        draw_y = (target-y)*zoom_y-cam_y
        color = "#000000"
        used_font = font
        draw_scale = 8
        if i == selected:
            anim *= 0.7**dt
            scale_anim *= 0.8**dt
            draw_y += anim
            draw_scale += scale_anim
            offset_x = x
            color = "#0000ee"
            used_font = font_b
        if i-1 >= 0:
            prev_x = (i-1)*zoom_x-cam_x+screen_width/2
            prev_y = (target-history[i-1])*zoom_y-cam_y
            pygame.draw.line(screen, "#000000", [draw_x, draw_y], [prev_x, prev_y], 4)
        pygame.draw.circle(screen, color, [draw_x, draw_y], draw_scale)
        text_surface = used_font.render(str(round(y, 2)), True, color)
        screen.blit(text_surface, [draw_x-text_surface.get_width()/2, draw_y+30])
        
    text_surface = font_b.render(f"Target: {target}", True, "#000000")
    screen.blit(text_surface, [50, 50])
    text_surface = font_b.render(f"Actual Value: {actual_value}", True, "#000000")
    screen.blit(text_surface, [50, 110])
    if len(history) > 0:
        text_surface = font_b.render(f"Step: {selected}", True, "#000000")
        screen.blit(text_surface, [50, 170])

    pygame.display.update()