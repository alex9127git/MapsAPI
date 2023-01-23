import os
import sys
import pygame
import requests


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


def run():
    longitude = float(input("Введите долготу: "))
    latitude = float(input("Введите широту: "))
    zoom = int(input("Введите масштаб (от 0 до 17, чем больше, тем крупнее): "))
    """
    Тестовые данные:
    долгота = 37.620070
    широта = 55.753630
    масштаб = 13
    показывает фото из документации яндекса (почти)
    """
    screen = initialize()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        clock.tick(60)
        if get_map(longitude, latitude, zoom):
            screen.blit(pygame.transform.scale(pygame.image.load(TEMP_FILENAME), (WIDTH, HEIGHT)), (0, 0))
        else:
            screen.fill("black")
        pygame.display.flip()


if __name__ == '__main__':
    run()
