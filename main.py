import os
import sys
import pygame
import requests

tool_color, tool_message = "blue", ''
cont_t = ["map", "sat", "sat,skl", "sat,skl,trf"]

WIDTH = 1200
HEIGHT = 900
TEMP_FILENAME = "temp.png"


def terminate():
    pygame.quit()
    if os.path.exists(TEMP_FILENAME):
        os.remove(TEMP_FILENAME)
    sys.exit()


def get_map(longitude, latitude, zoom, cont_type):
    request = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&z={zoom}&l={cont_t[cont_type]}&size" \
              f"=600,450"
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
        input_text1, input_text2, input_text3, cont_type = map(lambda x: x[1], input_data)
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
    do_input = list(map(lambda x: x[0], input_data[:3]))
    input_texts = list(map(lambda x: x[1], input_data[:3]))
    cont_type = input_data[3][1]
    rects = (pygame.Rect(143, 115, 230, 25), pygame.Rect(143, 165, 230, 25), pygame.Rect(143, 215, 230, 25))
    for i, rect in enumerate(rects):
        border_color = (255, 86, 0) if do_input[i] else (0, 0, 0)
        pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.draw.rect(screen, border_color, rect, 2)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0]:
        for i in range(3):
            if rects[i].collidepoint(mouse[0], mouse[1]):
                do_input = [False, False, False]
                do_input[i] = True
                break
        else:
            do_input = [False, False, False]
    for i in range(3):
        if do_input[i]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        do_input[i] = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_texts[i] = input_texts[i][:-1]
                    else:
                        if len(input_texts[i]) < 21:
                            input_texts[i] += event.unicode
        if len(input_texts[i]):
            print_text(screen, input_texts[i], rects[i].x + 10, rects[i].y + 4, font_color=(0, 0, 0), font_size=25)
    return list(map(list, zip(do_input, input_texts))) + [["", cont_type]]


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
    input_data = [[False, ''], [False, ''], [False, ''], ['', 0]]
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


def print_map(screen, lon, lat, zm, cont_type):
    screen.fill("black")
    if get_map(lon, lat, zm, cont_type):
        screen.blit(pygame.transform.scale(pygame.image.load(TEMP_FILENAME), (WIDTH, HEIGHT)), (0, 0))
    else:
        if os.path.exists(TEMP_FILENAME):
            screen.blit(pygame.transform.scale(pygame.image.load(TEMP_FILENAME), (WIDTH, HEIGHT)), (0, 0))
            print_text(screen, "Не получилось обновить карту", 10, 10, (255, 0, 0), 80)
            return
        print_text(screen, "Ошибка ввода данных:", 10, 10, (255, 0, 0), 80)
        error_text = ""
        try:
            _ = float(lon)
        except ValueError:
            error_text = "Долгота не является числом"
        try:
            _ = float(lat)
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
    longitude, latitude, zoom, cont_type = inputs
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    if 0 <= int(zoom) + 1 <= 17:
                        zoom += 1
                if event.key == pygame.K_PAGEDOWN:
                    if 0 <= int(zoom) - 1 <= 17:
                        zoom -= 1
                if event.key == pygame.K_SPACE:
                    cont_type = (cont_type + 1) % len(cont_t)
        keys = pygame.key.get_pressed()
        delta = 0.0001 * (2 ** (17 - zoom))
        if keys[pygame.K_RIGHT]:
            longitude += delta
            longitude = -180 if longitude >= 180 else longitude
        if keys[pygame.K_LEFT]:
            longitude -= delta
            longitude = 180 if longitude <= -180 else longitude
        if keys[pygame.K_UP]:
            latitude += delta
            latitude = -85 if latitude >= 85 else latitude
        if keys[pygame.K_DOWN]:
            latitude -= delta
            latitude = 85 if latitude <= -85 else latitude
        clock.tick(60)
        print_map(screen, longitude, latitude, zoom, cont_type)
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
        inputs = list(map(lambda x: x[1], input_menu()))
        screen = initialize()
        map_screen(screen, (float(inputs[0]), float(inputs[1]), int(inputs[2]), inputs[3]))
        # map_screen(screen, (37.62007, 55.75363, 13, 0))


if __name__ == '__main__':
    run()
