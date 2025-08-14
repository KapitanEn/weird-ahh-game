import pygame

#initacjalizacja

pygame.init()
pygame.font.init()
pygame.mouse.set_cursor(pygame.cursors.diamond)
pygame.display.set_caption('grzyb')
#deklaracja zmiennych

#funkcja do obrazu

def process_img_to_texture(img_str_path):
    returnal = pygame.image.load(img_str_path).convert_alpha()
    return returnal


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
stats = ['money',1000,'expirience',0,'avg power generation',0]
comic = pygame.font.SysFont('Comic Sans MS', 15)
mouse_pos = (0,0)
mouse_state = [False,False,False]
state_clock_int = 0
selected = 'wheat'

#0:left click 1:scroll click 2:right click
click_cooldown = [0,0,0]

menu = "garden"
state = 1

#tekstury/obrazki
grass = [process_img_to_texture('grass.png'),process_img_to_texture('grass_2.png'),'grass',0,0]
macerator = [process_img_to_texture('mac.png'),process_img_to_texture('mac_2.png'),'macerator',100]
wheat = [process_img_to_texture('wheat.png'),process_img_to_texture('wheat_2.png'),'wheat',0,50]
wheat_g = [process_img_to_texture('wheat_g.png'),process_img_to_texture('wheat_g_2.png'),'wheat grown',100,0,10]

tile_list_map = [grass]*240
crops = [wheat]
tile_hover_list = [wheat,macerator,grass]
crops_growth = [wheat_g]
#funkcje
def text_display(surface_obj,color_tuple_int,pos_tuple_int,text_str):
    text_surface = comic.render(text_str,False,color_tuple_int)
    surface_obj.blit(text_surface,pos_tuple_int)
    
def display_statistics():
    for i in range(len(stats)//2):
        text_display(screen,pygame.Color(0,0,0),(10+120*i,10),str(stats[i*2])+' '+str(stats[i*2+1]))
    return

def draw_rectangle(surface_obj,left_begin_tuple_int,size_tuple_int,color_tuple_int):
    try:
        f_rect = pygame.Rect(left_begin_tuple_int,size_tuple_int)
    except:
        print("tuple_invalid")
    else:
        pygame.draw.rect(surface_obj,color_tuple_int,f_rect)

def draw_rectangle_center(surface_obj,center_tuple_int,size_tuple_int,color_tuple_int):
    f_lefted_center = (center_tuple_int[0]-size_tuple_int[0],center_tuple_int[1]-size_tuple_int[1])
    f_righted_size = (size_tuple_int[0]*2,size_tuple_int[1]*2)
    try:
        draw_rectangle(surface_obj,f_lefted_center,f_righted_size,color_tuple_int)
    except:
        print("somting bwoke")

def draw_button_detect_menu(surface_obj,center_tuple_int,size_tuple_int,color_tuple_int,menu_str):
    draw_rectangle_center(surface_obj,center_tuple_int,size_tuple_int,color_tuple_int)
    global mouse_pos
    global mouse_state
    global click_cooldown
    global menu 
    if mouse_pos[0]>=(center_tuple_int[0]-size_tuple_int[0])and mouse_pos[0]<=(center_tuple_int[0]+size_tuple_int[0]):
        if mouse_pos[1]>=(center_tuple_int[1]-size_tuple_int[1])and mouse_pos[1]<=(center_tuple_int[1]+size_tuple_int[1]):
            if mouse_state[0] == True and click_cooldown[0] == 0 and menu != menu_str:
                click_cooldown = [5,click_cooldown[1],click_cooldown[2]]
                menu = menu_str
                print("activated button ",menu_str)
            elif mouse_state[0] == True and click_cooldown[0] == 0 and menu == menu_str:
                click_cooldown = [5,click_cooldown[1],click_cooldown[2]]
                menu = "graden"
    return

def display_hud():
    #background
    draw_rectangle(screen,(0,0),(1280,30),pygame.Color(255,255,255))
    #staty
    display_statistics()
    #lista menu do przycisków
    menus = ["crops","shop","unlock"]
    #przyciski
    for x in range(len(menus)):
        draw_button_detect_menu(screen,(640-(30+40*x),17),(10,10),pygame.Color(255,0,0),menus[x])

def farmland_gen():
    global tile_list_map
    main_section_rect_obj = pygame.Rect(140,40,1040,640)
    pygame.draw.rect(screen,pygame.Color(255,175,128),main_section_rect_obj)
    for y in range(640//50):
        for x in range(1040//50):
            list_hold = y*10+x
            if state == 0:
                screen.blit(tile_list_map[list_hold][0],(160+x*50,60+50*y))
            else:
                screen.blit(tile_list_map[list_hold][1],(160+x*50,60+50*y))

def crop_button_buy_select(surface_obj,texture_obj,begining_tuple_int,str_select):
    global mouse_state
    global mouse_pos
    global selected
    buy_rect = pygame.Rect(begining_tuple_int,(60,60))
    pygame.draw.rect(surface_obj,pygame.Color(255,125,0),buy_rect)
    surface_obj.blit(texture_obj,begining_tuple_int)
    text_display(surface_obj,pygame.Color(0,0,0),(begining_tuple_int[0]+60,begining_tuple_int[1]),str_select)
    if buy_rect.collidepoint(mouse_pos) == True and mouse_state[0] == True and click_cooldown[0] <= 0:
        selected = str_select
        click_cooldown[0] = 5
    
            
def display_garden():
    global selected
    farmland_gen()
    if selected != '':
        hover_handler_tile_alpha()
    return

def display_crops_menu():
    draw_rectangle(screen,(300,0),(725,720),pygame.Color(0,255,255))
    for i in range(len(crops)):
        crop_button_buy_select(screen,crops[i][0],(350,100+100*i),crops[i][2])

def debounce_handler():
    global click_cooldown
    global dt
    for x in range(len(click_cooldown)):
        if click_cooldown[x] > 0:
            click_cooldown[x] = click_cooldown[x]-dt*60
        elif click_cooldown[x] < 0:
            click_cooldown[x] = 0

def state_oscilator():
    global state
    global state_clock_int
    state_clock_int += dt*10
    if state_clock_int >= 60 and state == 0:
        state_clock_int = 0
        state = 1
    elif state_clock_int >= 60 and state == 1:
        state_clock_int = 0
        state = 0

def hover_handler_tile_alpha():
    global mouse_pos
    global tile_hover_list
    global selected
    global screen
    global mouse_state
    for x in range(len(tile_hover_list)):
        if tile_hover_list[x][2] == selected:
            display_raw = tile_hover_list[x][1]
            display_raw.set_alpha(50)
            break
    
    screen.blit(display_raw,(mouse_pos[0]-30,mouse_pos[1]-30))
    display_raw.set_alpha(255)

def buy_handler_select_place():
    global mouse_pos
    global mouse_state
    global selected
    global click_cooldown
    global tile_hover_list
    global tile_list_map
    global stats
    tile = []
    tile_hover = 0
    if selected != '' and click_cooldown[0] <= 0 and mouse_state[0] == True and mouse_pos[0] >= 160 and mouse_pos[0] <= 1160 and mouse_pos[1] >= 60 and mouse_pos[1] <= 660:
        tile_hover = int((mouse_pos[0]-160)//50+(mouse_pos[1]-60)//50*10)
        click_cooldown[0] = 10
        for x in range(len(tile_hover_list)):
            if tile_hover_list[x][2] == selected and stats[1]-tile_hover_list[x][4] >= 0:
                tile = tile_hover_list[x]
                stats[1] = stats[1]-tile_hover_list[x][4]
                stats[3] += tile_hover_list[x][4]
                tile_list_map[tile_hover] = tile
                print(tile_hover)
                break

#purely for debug
def count_item_in_list(list_obj,item_obj):
    returnal = 0
    returnal_pos = []
    for i in range(len(list_obj)):
        if item_obj == list_obj[i]:
            returnal += 1
            returnal_pos.append(i)
    return returnal , returnal_pos

#glowna petla
while running:
    
    #wykrywanie eventów
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        selected = ''
    #test


    #upd do zmiennych
    buy_handler_select_place()
    mouse_pos = pygame.mouse.get_pos()
    mouse_state = pygame.mouse.get_pressed()
    debounce_handler()
    state_oscilator()
    #sekcja do renderu
    screen.fill(pygame.Color(128,255,128))
    display_garden()
    if menu == 'crops':
        display_crops_menu()
    #display_hud()
    
    pygame.display.flip()
    dt = clock.tick(60)/1000

pygame.quit()
input('i quit out of spite dont worry')
