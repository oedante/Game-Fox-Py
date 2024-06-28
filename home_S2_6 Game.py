#Learning group: группа Pytн-КБд-242304-25
#Autor: Ермишин Олег
#Курс 2
#Домашнее задание 6

import datetime
import os
import pygame
import random
import time

#получаем текущий час и выбираем приветствее
current_hour = datetime.datetime.now().time().hour                                                    

if current_hour < 5 or current_hour > 22:
    greeting = 'Доброй ночи'
elif current_hour < 10:
    greeting = 'Доброе утро'
elif current_hour < 19:
    greeting = 'Добрый день'
elif current_hour < 23:
    greeting = 'Добрый вечер'
else: 
    greeting = 'Доброго апокалипсиса'

#выводим приветствие
print(f'{greeting}, {os.getlogin()}.\n')
#Получаем текущую деррикторию скрипта
curr_dir = os.path.dirname(os.path.abspath(__file__))

#---------------------------------------------------------------------------------------------------------
#Свойства окна и FPS
win_width = 900
win_height = 700
fps = 60

#Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((win_width, win_height), 0, 32 )
pygame.display.set_caption("Собираем грибы в лису")
clock = pygame.time.Clock()

global victori_count
victori_count = 0

#Создаем землю
background = pygame.image.load( curr_dir + '\\image\\back.jpg').convert()
background = pygame.transform.scale(background,(win_width,win_height))

#Создаем класс игрока
class fox(pygame.sprite.Sprite):
    def __init__(self):

        #Загружаем анимацю
        animation_frames = []
        sprite = pygame.image.load( "{0}.png".format(curr_dir + '\\image\\fox') ).convert_alpha()
        #Находим длину, ширину изображения и размеры каждого кадра
        width, height = sprite.get_size()
        w, h = width/4, height/4   
        # счетчик положения кадра на изображении
        row = 0
            # итерация по строкам
        for j in range(int(height / h)):
            # производим итерацию по элементам строки
            for i in range(int(width / w)):
                    # добавляем  в список отдельные кадры
                    animation_frames.append(sprite.subsurface(pygame.Rect(i * w, row, w, h ) ) )
            # смещаемся на высоту кадра, т.е. переходим на другую строку
            row += int(h)

        pygame.sprite.Sprite.__init__(self)
        self.image = animation_frames[12]
        self.animation = animation_frames
        self.rect = self.image.get_rect()
        self.rect.centerx = win_width / 2
        self.rect.bottom = win_height - 10
        self.speed_x = 0
        self.speed_y = 0
        self.frame = 0 # текущий кадр
        self.last_update = pygame.time.get_ticks()

    def update(self):
        #Начальная скорость
        self.speed_x = 0
        self.speed_y = 0

        #Счетчик анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > fps:
            self.last_update = now
            self.frame += 1

        #Событие нажатия клавиш
        keystate = pygame.key.get_pressed() 
          
        #Вперед   
        if keystate[pygame.K_UP]:
            self.speed_x = 0
            self.speed_y = -4
            if self.frame not in list(range(12, 15)):
                self.frame = 12
            self.image = self.animation[self.frame]
        #Назад 
        elif keystate[pygame.K_DOWN]:
            self.speed_x = 0
            self.speed_y = 4
            if self.frame not in list(range(0, 3)):
                self.frame = 0
            self.image = self.animation[self.frame]
        #Налево
        elif keystate[pygame.K_LEFT]:
            self.speed_x = -4
            self.speed_y = 0
            if self.frame not in list(range(4, 7)):
                self.frame = 4
            self.image = self.animation[self.frame]
        #Направо         
        elif keystate[pygame.K_RIGHT]:
            self.speed_x = 4
            self.speed_y = 0
            if self.frame not in list(range(8, 11)):
                self.frame = 8
            self.image = self.animation[self.frame]

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top > win_height - self.image.get_height():
            self.rect.top = win_height - self.image.get_height()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > win_width:
            self.rect.right = win_width
        if self.rect.left < 0:
            self.rect.left = 0

#Создаем класс грибов
class mushroom(pygame.sprite.Sprite):
    instances_count = 0
    def __init__(self, x, y):
        #Количество объектов
        mushroom.instances_count += 1
        
        #Загружаем анимацю
        animation_frames = []
        sprite = pygame.image.load( "{0}.png".format(curr_dir + '\\image\\mushroom') ).convert_alpha()
        #Находим длину, ширину изображения и размеры каждого кадра
        width, height = sprite.get_size()
        w, h = width/9, height/1   
        # счетчик положения кадра на изображении
        row = 0
            # итерация по строкам
        for j in range(int(height / h)):
            # производим итерацию по элементам строки
            for i in range(int(width / w)):
                    # добавляем  в список отдельные кадры
                    animation_frames.append(sprite.subsurface(pygame.Rect(i * w, row, w, h ) ) )
            # смещаемся на высоту кадра, т.е. переходим на другую строку
            row += int(h)

        pygame.sprite.Sprite.__init__(self)
        self.image = animation_frames[1]
        self.animation = animation_frames
        self.rect = self.image.get_rect()
        self.rect.centerx = win_width - x
        self.rect.bottom = win_height - y
        self.frame = 0 # текущий кадр
        self.last_update = pygame.time.get_ticks()

    def update(self):
        #Переменная съеденных грибов
        global victori_count

        #Счетчик анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > fps:
            self.last_update = now
            self.frame += 1

        if self.frame not in list(range(0, 8)):
                self.frame = 0
        self.image = self.animation[self.frame]

        if self.rect.colliderect(fox.rect):
            self.kill()
            mushroom.instances_count -= 1
            victori_count += 1

        if self.rect.colliderect(tree1.rect):
            mushroom.instances_count -= 1
            self.kill()

        if self.rect.colliderect(tree2.rect):
            mushroom.instances_count -= 1
            self.kill()

        if self.rect.colliderect(tree3.rect):
            mushroom.instances_count -= 1
            self.kill()

        if self.rect.colliderect(tree4.rect):
            mushroom.instances_count -= 1
            self.kill()

        if self.rect.colliderect(tree5.rect):
            mushroom.instances_count -= 1
            self.kill()

#Создаем класс деревьев
class tree(pygame.sprite.Sprite):
    def __init__(self, x, y, n):
        #Количество объектов
        
        #Загружаем анимацю
        sprite = pygame.image.load( "{0}.png".format(curr_dir + '\\image\\tree' + n) ).convert_alpha()
        sprite = pygame.transform.scale(sprite,(128,128))
        #Находим длину, ширину изображения и размеры каждого кадра

        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.centerx = win_width - x
        self.rect.bottom = win_height - y

    def update(self):
        #Коллизиия с деревом
        if self.rect.colliderect(fox.rect):         
            tree_collizion = pygame.Rect(self.rect.x + 45, self.rect.y + 20, 38, 108)
            if pygame.Rect.colliderect(fox.rect, tree_collizion):           
                    fox.rect.y -= fox.speed_y
                    fox.rect.x -= fox.speed_x 

            

#Вывод счетчика
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (200,200,200))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Создаем пользовательское событие 
ADD_MUSHROOM= pygame.USEREVENT + 1            
# Устанавливаем таймер на 5 секунд 
pygame.time.set_timer(ADD_MUSHROOM, 1000)  
# Создаем пользовательское событие 
FOX_STEP= pygame.USEREVENT + 2            
# Устанавливаем таймер на 5 секунд 
pygame.time.set_timer(FOX_STEP, 1000)  
VICTORI= pygame.USEREVENT + 3            
# Устанавливаем таймер на 5 секунд 
pygame.time.set_timer(VICTORI, 500)

# Цикл игры------------------------------------------------------------------------------------
all_sprites = pygame.sprite.Group()
fox = fox()
tree1 = tree(400,400,'1')
tree2 = tree(750,150,'2')
tree3 = tree(700,500,'3')
tree4 = tree(300,100,'4')
tree5 = tree(100,400,'5')

all_sprites.add(fox)
all_sprites.add(tree1)
all_sprites.add(tree2)
all_sprites.add(tree3)
all_sprites.add(tree4)
all_sprites.add(tree5)

running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(fps)
    now = pygame.time.get_ticks()

    # Обновление
    all_sprites.update()

    # Рендеринг
    screen.fill(( 0, 0, 0 ))
    screen.blit(background,(0,0))
    draw_text(screen, f'Вы съели грибов: {victori_count}', 18, win_width / 2 + 300, 10)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

    # Обрабатываем события 
    for event in pygame.event.get(): 
        # Если событие закрытия окна, то выходим из цикла 
        if event.type == pygame.QUIT:
            running = False 
        # Если событие удаления монеты, то выбираем случайную монету и удаляем ее 
        if event.type == ADD_MUSHROOM: 
            #Добавляем грибы
            if mushroom.instances_count < 10:
                all_sprites.add(mushroom(random.randint(50, win_width - 50),random.randint(50, win_height - 50)))
                pygame.time.set_timer(ADD_MUSHROOM, random.randint(100, 1500)) 
        if event.type == VICTORI:
            if victori_count == 30:
                draw_text(screen, f'Вы съели 30 грибов!!!', 18, win_width / 2 + 300, 10)
                print('Вы съели 30 грибов!!!')
                time.sleep(2)
                running = False 

pygame.quit()

#тормозим терминал
#input("\nНажмите любую клавишу для завершения...")