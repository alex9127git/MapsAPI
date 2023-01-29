import os
import sys
import pygame
import requests

tool_color, tool_message = "blue", ''

WIDTH = 1200
HEIGHT = 900
TEMP_FILENAME = "temp.png"


def terminate():
    pygame.quit()
    if os.path.exists(TEMP_FILENAME):
        os.remove(TEMP_FILENAME)
    sys.exit()


def get_map(longitude, latitude, zoom):
    request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&z={zoom}&l=map&size=600,450"
    response = requests.get(request)
    if response:
        map_file = TEMP_FILENAME
        with open(map_file, "wb") as file:
            file.write(response.content)
        return True
    else:
        return False


def initialize():
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    return screen


class Button:
    def __init__(self, wid1, hei1, osob=False, fs=40, in_c=(20, 17, 237), ac_c=(134, 132, 232)):
        self.width, self.height = wid1, hei1
        self.inactive_color = in_c
        self.active_color = ac_c
        self.osob = osob
        self.fs = fs

    def update(self, screen, x, y, message, input_data):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, self.active_color, (x, y, self.width, self.height))
                if click[0] == 1 and self.osob:
                    self.on_click(input_data)
            else:
                pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.inactive_color, (x, y, self.width, self.height))
        print_text(screen, message, x + self.width // 2, y + self.height // 2, font_size=self.fs, centered=True)

    def on_click(self, input_data):
        global tool_color, tool_message
        input_text1, input_text2, input_text3 = map(lambda x: x[1], input_data)
        if not (input_text1 and input_text2 and input_text3):
            tool_color, tool_message = "red", "Некорректные данные!"
            return
        tool_color, tool_message = "green", "Данные успешно добавлены"


def print_text(screen, message, x, y, font_color=(255, 255, 255), font_size=40, centered=False):
    font_type = pygame.font.Font(None, font_size)
    text = font_type.render(message, True, font_color)
    if centered:
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    else:
        screen.blit(text, (x, y))


def update_inputs(screen, input_data):
    need_input1, input_text1 = input_data[0]
    need_input2, input_text2 = input_data[1]
    need_input3, input_text3 = input_data[2]
    rects = (pygame.Rect(143, 115, 230, 25), pygame.Rect(143, 165, 230, 25), pygame.Rect(143, 215, 230, 25))
    for rect in rects:
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, (255, 86, 0), rect, 2)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rects[0].collidepoint(mouse[0], mouse[1]) and click[0] and not (need_input2 or need_input3):
        need_input1 = True
    if rects[1].collidepoint(mouse[0], mouse[1]) and click[0] and not (need_input3 or need_input1):
        need_input2 = True
    if rects[2].collidepoint(mouse[0], mouse[1]) and click[0] and not (need_input2 or need_input1):
        need_input3 = True

    if need_input1:
        for event1 in pygame.event.get():
            if event1.type == pygame.KEYDOWN:
                if event1.key == pygame.K_RETURN:
                    need_input1 = False
                elif event1.key == pygame.K_BACKSPACE:
                    input_text1 = input_text1[:-1]
                else:
                    if len(input_text1) < 21:
                        input_text1 += event1.unicode
    if need_input2:
        for event2 in pygame.event.get():
            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_RETURN:
                    need_input2 = False
                elif event2.key == pygame.K_BACKSPACE:
                    input_text2 = input_text2[:-1]
                else:
                    if len(input_text2) < 21:
                        input_text2 += event2.unicode
    if need_input3:
        for event3 in pygame.event.get():
            if event3.type == pygame.KEYDOWN:
                if event3.key == pygame.K_RETURN:
                    need_input3 = False
                elif event3.key == pygame.K_BACKSPACE:
                    input_text3 = input_text3[:-1]
                else:
                    if len(input_text3) < 21:
                        input_text3 += event3.unicode

    if len(input_text1):
        print_text(screen, input_text1, rects[0].x + 10, rects[0].y + 4, font_color=(0, 0, 0), font_size=25)
    if len(input_text2):
        print_text(screen, input_text2, rects[1].x + 10, rects[1].y + 4, font_color=(0, 0, 0), font_size=25)
    if len(input_text3):
        print_text(screen, input_text3, rects[2].x + 10, rects[2].y + 4, font_color=(0, 0, 0), font_size=25)
    return [[need_input1, input_text1], [need_input2, input_text2], [need_input3, input_text3]]


def draw(screen):
    # общие настройки + авторизация
    font = pygame.font.SysFont('arial', 45)
    text = font.render("Генерация карты", False, (0, 5, 0))
    text_x, text_y = 135, 20
    screen.blit(text, (text_x, text_y))

    font = pygame.font.SysFont("Segoe UI black", 15)
    text = font.render("Координата x", True, (0, 0, 0))
    text_x, text_y = 10, 120
    screen.blit(text, (text_x, text_y))

    font = pygame.font.SysFont("Segoe UI black", 15)
    text = font.render("Координата y", True, (0, 0, 0))
    text_x, text_y = 10, 170
    screen.blit(text, (text_x, text_y))

    font = pygame.font.SysFont("Segoe UI black", 14)
    text = font.render("Масштаб", True, (0, 0, 0))
    text_x, text_y = 10, 220
    screen.blit(text, (text_x, text_y))


def input_menu():
    pygame.init()
    size = 450, 350
    screen = pygame.display.set_mode(size)
    button = Button(130, 45, True, 32)
    button2 = Button(40, 40, in_c=(247, 104, 164), ac_c=(252, 174, 207))
    running = True
    input_data = [[False, ''], [False, ''], [False, '']]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if tool_color == "green":
            running = False
        pygame.display.set_caption('Maps API')
        screen.fill("black")
        bg = pygame.transform.scale(pygame.image.load("fon.jpg"), (700, 490))
        screen.blit(bg, (-50, -75))
        draw(screen)
        # рисуем кнопку
        button.update(screen, 185, 265, "Создать", input_data)
        button2.update(screen, 25, 25, 'A', input_data)

        pygame.draw.rect(screen, (255, 255, 255), (185, 265, 130, 45), 2)
        pygame.draw.rect(screen, (255, 255, 255), (25, 25, 40, 40), 2)

        input_data = update_inputs(screen, input_data)
        print_text(screen, tool_message, 5, 320, tool_color, font_size=30)
        pygame.display.flip()
    return input_data


def print_map(screen, lat, lon, zm):
    if get_map(lat, lon, zm):
        screen.blit(pygame.transform.scale(pygame.image.load(TEMP_FILENAME), (WIDTH, HEIGHT)), (0, 0))
    else:
        screen.fill("black")
        print_text(screen, "Ошибка ввода данных:", 10, 10, (255, 0, 0), 80)
        error_text = ""
        try:
            _ = float(lat)
        except ValueError:
            error_text = "Долгота не является числом"
        try:
            _ = float(lon)
        except ValueError:
            error_text = "Широта не является числом"
        try:
            z = int(zm)
            if z < 0 or 17 < z:
                raise ValueError
        except ValueError:
            error_text = "Неправильно задан масштаб"
        print_text(screen, error_text, 10, 100, (255, 0, 0), 80)


def map_screen(screen, inputs):
    latitude, longitude, zoom = inputs
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.K_PAGEUP and zoom:
                if 0 <= int(zoom) + 1 <= 17:
                    zoom = str(int(zoom) + 1)
            if event.type == pygame.K_PAGEDOWN and zoom:
                if 0 <= int(zoom) - 1 <= 17:
                    zoom = str(int(zoom) - 1)
        clock.tick(60)
        print_map(screen, latitude, longitude, zoom)
        pygame.display.flip()


def run():
    while True:
        """
        Тестовые данные:
        долгота = 37.620070
        широта = 55.753630
        масштаб = 13
        показывает фото из документации яндекса (почти)
        """
        inputs = map(lambda x: x[1], input_menu())
        screen = initialize()
        map_screen(screen, inputs)


if __name__ == '__main__':
    run()
