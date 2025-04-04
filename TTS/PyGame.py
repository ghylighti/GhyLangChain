import pygame


def init():
    pygame.mixer.init()

def play():
    pygame.mixer.music.load("tts_output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # 比 continue 更优雅
    pygame.mixer.music.unload()