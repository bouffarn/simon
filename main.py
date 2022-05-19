import pygame, random

pygame.init()
size = width, height = 500, 500
display = pygame.display.set_mode(size)

options, pattern, patternPos, patternPause = ["green", "red", "yellow", "blue"], [], 0, False
chosen, clicked, initialDifficulty, difficulty = [], "", 1, 0
lastTime, status = pygame.time.get_ticks(), ""
gameOverPos, gameOverPause = 0, False

Running = True
while Running:
    currentTime = pygame.time.get_ticks()
    # Display
    display.fill((255, 255, 255))
    green = pygame.draw.rect(display, (0, 128, 0), pygame.Rect(0, 0, width / 2, height / 2))
    red = pygame.draw.rect(display, (128, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
    yellow = pygame.draw.rect(display, (128, 128, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
    blue = pygame.draw.rect(display, (0, 0, 128), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    #   Simon Says
    if patternPos < len(pattern):
        if lastTime+250 < currentTime and patternPause:
            patternPause, lastTime = not patternPause, currentTime
            lastTime = currentTime
        elif lastTime+500 < currentTime:
            patternPos += 1
            patternPause, lastTime = not patternPause, currentTime
        if not patternPause:
            if pattern[patternPos] == "green":
                pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
            elif pattern[patternPos] == "red":
                pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
            elif pattern[patternPos] == "yellow":
                pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
            elif pattern[patternPos] == "blue":
                pygame.draw.rect(display, (0, 0, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    #   Clicked
    if clicked != "":
        if lastTime+500 < currentTime:
            clicked = ""
            if len(chosen) == len(pattern):
                if chosen == pattern:
                    chosen, patternPos = [], 0
                    difficulty += 1
                    lastTime = currentTime + 500
                    pattern.append(random.choice(options))
        if clicked == "green":
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
        elif clicked == "red":
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
        elif clicked == "yellow":
            pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
        elif clicked == "blue":
            pygame.draw.rect(display, (0, 0, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    #   Game Over
    if status == "end":
        if lastTime + 250 < currentTime and gameOverPause:
            gameOverPause, lastTime = not gameOverPause, currentTime
        elif lastTime + 500 < currentTime:
            gameOverPos += 1
            if gameOverPos == 3:
                status, pattern, patternPos, chosen, gameOverPos = "", [], 0, [], 0
            gameOverPause, lastTime = not gameOverPause, currentTime
        if not gameOverPause:
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
            pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
            pygame.draw.rect(display, (0, 0, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    # Logic
    #   New Game
    if len(pattern) == 0:
        difficulty = initialDifficulty
        for i in range(difficulty):
            pattern.append(random.choice(options))
        lastTime = currentTime
    #   Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.MOUSEBUTTONUP and patternPos == len(pattern):
            pos = pygame.mouse.get_pos()
            if green.collidepoint(pos):
                clicked = "green"
                chosen.append(clicked)
            elif red.collidepoint(pos):
                clicked = "red"
                chosen.append(clicked)
            elif yellow.collidepoint(pos):
                clicked = "yellow"
                chosen.append(clicked)
            elif blue.collidepoint(pos):
                clicked = "blue"
                chosen.append(clicked)
            lastTime = currentTime
            if len(chosen) == len(pattern):
                if not chosen == pattern:
                    status = "end"
    pygame.display.flip()
