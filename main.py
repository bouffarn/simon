import pygame, random

pygame.init()
size = width, height = 500, 500
display = pygame.display.set_mode(size)

completed = True
options, pattern, patternPos, patternPause = ["green", "red", "yellow", "blue"], [], 0, False
chosen, clicked, difficulty = [], "", 3
lastTime = pygame.time.get_ticks()

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
        if lastTime+2000 < currentTime and not patternPause:
            patternPos += 1
            patternPause = not patternPause
            lastTime = currentTime
        elif lastTime+250 < currentTime and patternPause:
            patternPause = not patternPause
            lastTime = currentTime
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
        if clicked == "green":
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
        elif clicked == "red":
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
        elif clicked == "yellow":
            pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
        elif clicked == "blue":
            pygame.draw.rect(display, (0, 0, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    # Logic
    #   New Game
    if completed and len(pattern) == 0:
        for i in range(difficulty):
            pattern.append(random.choice(options))
        lastTime = currentTime
    #   Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if clicked == "":
                if green.collidepoint(pos):
                    clicked = "green"
                elif red.collidepoint(pos):
                    clicked = "red"
                elif yellow.collidepoint(pos):
                    clicked = "yellow"
                elif blue.collidepoint(pos):
                    clicked = "blue"
                chosen.append(clicked)
                lastTime = currentTime
            if len(chosen) == len(pattern):
                if chosen == pattern:
                    print("correct")
                else:
                    print("incorrect")
    pygame.display.flip()
