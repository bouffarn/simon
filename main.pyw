import pygame, random

pygame.init()
size = width, height = 500, 500
display = pygame.display.set_mode(size)
fontTitle, fontButton = pygame.font.SysFont(None, 72), pygame.font.SysFont(None, 36)

options, pattern, patternPos, patternPause = ["green", "red", "yellow", "blue"], [], 0, False
chosen, clicked, initialDifficulty, difficulty, lastScore, highScore = [], "", 1, 0, 0, 0
lastTime, status = pygame.time.get_ticks(), "menu"
gameOverPos, gameOverPause = 0, False

Running = True
while Running:
    currentTime = pygame.time.get_ticks()
    # Display
    display.fill((255, 255, 255))
    if not status == "menu":
        green = pygame.draw.rect(display, (0, 128, 0), pygame.Rect(0, 0, width / 2, height / 2))
        red = pygame.draw.rect(display, (128, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
        yellow = pygame.draw.rect(display, (128, 128, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
        blue = pygame.draw.rect(display, (0, 0, 128), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    #   Simon Says
    if patternPos < len(pattern) and status != "menu":
        if lastTime + 250 < currentTime and patternPause:
            patternPause, lastTime = not patternPause, currentTime
            lastTime = currentTime
        elif lastTime + 500 < currentTime:
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
        if lastTime + 500 < currentTime:
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
    if status == "menu":
        title = fontTitle.render("Simon!", True, (0, 0, 0))
        display.blit(title, (width / 2 - title.get_width() / 2, 50))

        scoreText = fontButton.render("Score: " + str(lastScore), True, (0,0,0))
        display.blit(scoreText, (width / 2 - scoreText.get_width() / 2, 100 + title.get_height()))
        highScoreText = fontButton.render("High Score: " + str(highScore), True, (0,0,0))
        display.blit(highScoreText, (width / 2 - highScoreText.get_width() / 2, 100 + title.get_height() + scoreText.get_height()))

        playPos = [width/2, height/2]
        playText = fontButton.render("Play!", True, (0, 0, 0))
        playButton = pygame.draw.rect(display, (128, 128, 128), (playPos[0]-playText.get_rect()[2]/2-10, playPos[1]-playText.get_rect()[3]/2-10, playText.get_rect()[2]+20, playText.get_rect()[3]+20))
        display.blit(playText, (playPos[0] - playText.get_width() / 2, playPos[1] - playText.get_height() / 2))
    elif status == "end":
        if lastTime + 250 < currentTime and gameOverPause:
            gameOverPause, lastTime = not gameOverPause, currentTime
        elif lastTime + 500 < currentTime:
            gameOverPos += 1
            if gameOverPos == 3:
                lastScore = len(pattern)-1
                if lastScore > highScore:
                    highScore = lastScore
                status = "menu"
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
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if status == "menu":
                if playButton.collidepoint(pos):
                    lastTime = currentTime
                    status, pattern, patternPos, chosen, gameOverPos = "", [], 0, [], 0
            elif patternPos == len(pattern):
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
