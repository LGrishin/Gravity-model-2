import pygame
from Planet import Planet
from Physic import *
from pygame.locals import *

run = True
number_of_objects = 3
count_of_planet = 0
pointer = 0
visual_configs = {'shift_x': 0, 'shift_y': 0, 'shift_range': 40, 'zoom': 1, 'zoom_change': 0.9, 'inform': False}
colors_global = {'Red': (255, 0, 0), 'Green': (0, 255, 0), 'Blue': (0, 0, 255), 'White': (255, 255, 255),
                 'Black': (0, 0, 0)}
key_config = {'time change addition': 0.025, 'time change multiply': 1.06}
real_obj = [1] * number_of_objects


def collision(planet1, planet2, n,
              index):  # absolutely inelastic impact if n == 1 and perfectly elastic collision if n == 2

    if module1(planet1.x0, planet1.y0, planet2.x0, planet2.y0) < planet1.r + planet2.r - 10 and n == 1:
        real_obj[index] = 0
        planet1.Col, planet1.r = True, 0
        vx, vy = law_of_con_moment(planet1.m, planet2.m, planet1.Vx, planet2.Vx), law_of_con_moment(
            planet1.m, planet2.m, planet1.Vy, planet2.Vy)
        planet2.m += planet1.m
        planet2.velocity(vx, vy)

    if module1(planet1.x0, planet1.y0, planet2.x0, planet2.y0) < planet1.r + planet2.r and n == 2:
        vel_x = perfectly_elastic_collision(planet1.m, planet2.m, planet1.Vx, planet2.Vy)
        vel_y = perfectly_elastic_collision(planet1.m, planet2.m, planet1.Vy, planet2.Vy)
        planet1.velocity(vel_x[0], vel_y[0])
        planet2.velocity(vel_x[1], vel_y[1])


def change_time(delta, flag=0):
    if flag == 0:
        for planet in main_array:
            planet.time_interval_p(delta)
    if flag == 1:
        for planet in main_array:
            planet.time_interval_m(delta)


def draw_vector(planet, local_color, sign=1):
    pygame.draw.aaline(sc, local_color, [planet.Vel_vec_coords[0], planet.Vel_vec_coords[1]],
                       [planet.Vel_vec_coords[0] + 10 * cos(angle(planet.Vel_vec_coords[0], planet.Vel_vec_coords[1],
                                                                  planet.x0, planet.y0) - sign * pi / 8),
                        planet.Vel_vec_coords[1] + 10 * sin(angle(planet.Vel_vec_coords[0], planet.Vel_vec_coords[1],
                                                                  planet.x0, planet.y0) - sign * pi / 8)])


def color_of_speed_vector():
    main_array[0].first_space_speed(main_array[1].x0, main_array[1].y0)
    vx, vy = main_array[0].Vx - main_array[1].Vx, main_array[1].Vy - main_array[1].Vy
    v = module2(vx, vy)
    if v < main_array[0].orbital_velocity:
        return colors_global['Red']
    if main_array[0].orbital_velocity <= v < main_array[0].escape_velocity:
        return colors_global['Blue']
    if v >= main_array[0].escape_velocity:
        return colors_global['Green']


def update_planets(planet, index):  # and draw seed's vector
    local_color = colors_global['White']
    if index == 1 and main_array[0].m / planet.m >= 40:
        local_color = color_of_speed_vector()
    pygame.draw.circle(sc, planet.color, (int(planet.x0), int(planet.y0)), int(planet.r), 0)
    pygame.draw.aaline(sc, local_color, planet.get_coordinates(), planet.get_velocity_vet())
    draw_vector(planet, local_color)
    draw_vector(planet, local_color, -1)
    pygame.display.update()


def draw_trajectory(trajectory):
    for pairs in trajectory:
        pygame.draw.rect(sc, colors_global['White'],
                         (int(pairs[0] / visual_configs['zoom']) + visual_configs['shift_x'],
                          int(pairs[1] / visual_configs['zoom']) + visual_configs['shift_y'], 1, 1))


def draw_planet(planet):  # in main cycle
    pygame.draw.circle(sc, planet.color, (
        int(planet.x0 / visual_configs['zoom']) + visual_configs['shift_x'],
        int(planet.y0 / visual_configs['zoom']) + visual_configs['shift_y']),
                       int(planet.r / visual_configs['zoom']), 0)


def out_inform():
    inform.blit(Int_font.render(u'Time interval:  ' + str(main_array[0].time_interval), 1, colors_global['White']),
                (0, 0))
    count = 0
    for k in range(number_of_objects):
        if main_array[k].Col:
            continue
        inform.blit(Int_font.render(u'Object  ' + str(k + 1) + ':', 1, colors_global['White']), (0, 20 + 120 * count))
        inform.blit(Int_font.render(u'm:  ' + str(main_array[k].m), 1, colors_global['White']), (0, 40 + 120 * count))
        inform.blit(Int_font.render(u'Vx  ' + str(main_array[k].Vx), 1, colors_global['White']), (0, 60 + 120 * count))
        inform.blit(Int_font.render(u'Vy:  ' + str(main_array[k].Vy), 1, colors_global['White']), (0, 80 + 120 * count))
        inform.blit(Int_font.render(u'Ax:  ' + str(main_array[k].Ax), 1, colors_global['White']),
                    (0, 100 + 120 * count))
        inform.blit(Int_font.render(u'Ay:  ' + str(main_array[k].Ay), 1, colors_global['White']),
                    (0, 120 + 120 * count))
        count += 1


def inform_panel():
    global start_position_of_cs, inform
    if visual_configs['inform']:
        w.blit(inform, (0, 0))
        inform.fill(colors_global['Black'])
        inform = pygame.Surface((start_position_of_cs, 1080))
        if start_position_of_cs < 200:
            start_position_of_cs += 10

        else:
            out_inform()
    else:
        w.blit(inform, (0, 0))
        inform.fill(colors_global['Black'])

        if start_position_of_cs > 0:
            start_position_of_cs -= 10
            inform = pygame.Surface((start_position_of_cs, 1080))


def events_in_main_cycle():
    global run, pointer
    for ev_in_main in pygame.event.get():
        if ev_in_main.type == pygame.QUIT:
            run = False
        if ev_in_main.type == pygame.KEYDOWN:
            if ev_in_main.key == pygame.K_LEFT:  # move all objects left
                visual_configs['shift_x'] += visual_configs['shift_range']

            if ev_in_main.key == pygame.K_RIGHT:  # move all objects right
                visual_configs['shift_x'] -= visual_configs['shift_range']

            if ev_in_main.key == pygame.K_UP:  # move all objects up
                visual_configs['shift_y'] += visual_configs['shift_range']

            if ev_in_main.key == pygame.K_DOWN:  # move all objects down
                visual_configs['shift_y'] -= visual_configs['shift_range']

            if ev_in_main.key == pygame.K_EQUALS:  # zoom in on the image
                visual_configs['zoom'] *= visual_configs['zoom_change']

            if ev_in_main.key == pygame.K_MINUS:  # the distance image
                visual_configs['zoom'] /= visual_configs['zoom_change']

            if ev_in_main.key == pygame.K_TAB:  # get inform
                visual_configs['inform'] = not visual_configs['inform']

            if ev_in_main.key == pygame.K_t:  # t += time change addition
                change_time(key_config['time change addition'])

            if ev_in_main.key == pygame.K_r:  # t -= time change addition
                change_time(-key_config['time change addition'])

            if ev_in_main.key == pygame.K_g:  # t *= time change multiply
                change_time(key_config['time change multiply'], 1)

            if ev_in_main.key == pygame.K_f:  # t /= time change multiply
                change_time(1 / key_config['time change multiply'], 1)


main_array = []

for i in range(number_of_objects):  # creating planets
    main_array.append(Planet())

main_array[0].m = 990000000000000
main_array[1].m = 10000000000
main_array[2].m = 1000

pygame.init()
clock = pygame.time.Clock()
w = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
pygame.display.set_caption('Gravity_model_2_(S_J)')
bg = pygame.image.load("5.jpg")
sc = pygame.Surface((1920, 1080))
sc.set_alpha(None)
inform = pygame.Surface((0, 0))
w.blit(sc, (0, 0))
sc.blit(bg, (0, -150))

pygame.display.flip()
pygame.font.init()
Int_font = pygame.font.SysFont('Comic Sans MC', 20, False, True)
start_position_of_cs = 0
pygame.key.set_repeat(80, 10)

step_number = 0

while run and count_of_planet <= number_of_objects + 1:

    w.blit(sc, (0, 0))
    pygame.display.flip()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False

        if ev.type == pygame.MOUSEBUTTONDOWN:
            if ev.button == 1 and count_of_planet < number_of_objects and step_number % 2 == 0:  # fixing planet
                pygame.draw.circle(sc, colors_global['Red'], ev.pos, 10)  # position
                pygame.display.update()
                main_array[count_of_planet].coordinates(ev.pos[0], ev.pos[1])
                step_number += 1
                continue

            if ev.button == 1 and count_of_planet + 1 <= number_of_objects and step_number % 2 == 1:  # fixing
                main_array[count_of_planet].velocity_vector_coord(ev.pos)  # velocity vector
                main_array[count_of_planet].velocity((ev.pos[0] - main_array[count_of_planet].x0) / 10,
                                                     (ev.pos[1] - main_array[count_of_planet].y0) / 10)
                pygame.display.update()
                count_of_planet += 1
                step_number += 1
                continue

            if ev.button == 1 and count_of_planet >= number_of_objects:  # + 1 click for start
                count_of_planet += 2

        if ev.type == pygame.MOUSEMOTION and step_number % 2 \
                == 1 and count_of_planet < number_of_objects and step_number != 0:  # drawing velocity vector
            sc.blit(bg, (0, -150))
            main_array[count_of_planet].velocity_vector_coord(ev.pos)
            if count_of_planet == 1:  # for update orb vel
                main_array[count_of_planet].velocity((ev.pos[0] - main_array[count_of_planet].x0) / 10,
                                                     (ev.pos[1] - main_array[count_of_planet].y0) / 10)

            for i in range(count_of_planet + 1):
                update_planets(main_array[i], i)

while run:  # main cycle, starts only after the first cycle

    w.blit(sc, (start_position_of_cs, 0))
    sc.blit(bg, (0, -150))

    inform_panel()  # creating inform panel

    for i in main_array:  # drawing trajectory
        draw_trajectory(i.trajectory)

    for i in range(len(main_array)):  # calculating all physics and drawing planets
        if main_array[i].Col:
            continue

        main_array[i].Fx, main_array[i].Fy = 0, 0

        for j in range(len(main_array)):
            if main_array[j].Col:  # checking planet's collisions
                continue
            if j != i:
                collision(main_array[j], main_array[i], 1, j)
                Force = force(main_array[i].m, main_array[j].m, main_array[i].x0, main_array[i].y0, main_array[j].x0,
                              main_array[j].y0)  # force
                main_array[i].force_sum(Force[1], Force[2])
        main_array[i].update_planet()
        draw_planet(main_array[i])  # drawing planets

    pygame.display.update()
    events_in_main_cycle()  # processing all events in the main cycle

pygame.quit()
