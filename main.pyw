import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import json

# pygame variables
pygame.init()
size = 500, 500
display = pygame.display.set_mode(size, pygame.RESIZABLE)
fontTitle, fontButton = pygame.font.SysFont(None, 72), pygame.font.SysFont(None, 36)

try:
    soundGreen = pygame.mixer.Sound("sound/220.wav")
    soundRed = pygame.mixer.Sound("sound/277.wav")
    soundYellow = pygame.mixer.Sound("sound/294.wav")
    soundBlue = pygame.mixer.Sound("sound/330.wav")
    sound = True
except pygame.error:
    sound = False
    print("SOUND NOT INITIALIZED!!!")
# variables
options, pattern, patternPos, patternPause, initialPatternTime, patternTime = ["green", "red", "yellow",
                                                                               "blue"], [], 1, True, 500, 500
chosen, clicked, initialDifficulty, difficulty, lastScore = [], "", 1, 0, 0
lastTime, status = pygame.time.get_ticks(), "menu"
gameOverPos, gameOverPause = 0, False
soundPlaying = False
# save data
data = {"dataVersion": 0, "highScore": 0}
if os.path.exists("save.json"):
    file = open("save.json")
    data = json.load(file)
    file.close()


def save():
    global data
    with open("save.json", "w") as f:
        json.dump(data, f)


Running = True
while Running:
    width, height = display.get_size()
    currentTime = pygame.time.get_ticks()
    # Display
    display.fill((255, 255, 255))
    if not status == "menu":
        green = pygame.draw.rect(display, (0, 128, 0), pygame.Rect(0, 0, width / 2, height / 2))
        red = pygame.draw.rect(display, (128, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
        yellow = pygame.draw.rect(display, (128, 128, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
        blue = pygame.draw.rect(display, (0, 0, 128), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    #   Simon Says
    if patternPos < len(pattern) and status != "menu" and clicked == "":
        if lastTime + patternTime * 0.75 < currentTime and not patternPause:
            patternPause, lastTime = not patternPause, currentTime
            patternPos += 1
            if sound:
                soundGreen.stop()
                soundRed.stop()
                soundYellow.stop()
                soundBlue.stop()
                soundPlaying = False
        elif lastTime + patternTime < currentTime:
            patternPause, lastTime = not patternPause, currentTime
        if not patternPause:
            if pattern[patternPos] == "green":
                pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
                if not soundPlaying and sound:
                    soundPlaying = True
                    soundGreen.play(-1)
            elif pattern[patternPos] == "red":
                pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
                if not soundPlaying and sound:
                    soundPlaying = True
                    soundRed.play(-1)
            elif pattern[patternPos] == "yellow":
                pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
                if not soundPlaying and sound:
                    soundPlaying = True
                    soundYellow.play(-1)
            elif pattern[patternPos] == "blue":
                pygame.draw.rect(display, (50, 50, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
                if not soundPlaying and sound:
                    soundPlaying = True
                    soundBlue.play(-1)
    #   Clicked
    if lastTime + patternTime < currentTime and clicked != "":
        clicked = ""
        if sound:
            soundGreen.stop()
            soundRed.stop()
            soundYellow.stop()
            soundBlue.stop()
        if len(chosen) == len(pattern):
            if chosen == pattern:
                pattern.append(random.choice(options))
                chosen, patternPos = [], 0
                difficulty += 1
                lastTime = currentTime + patternTime * 0.75
                if patternTime > 100:
                    patternTime -= 10
    if clicked == "green":
        pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
    elif clicked == "red":
        pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
    elif clicked == "yellow":
        pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
    elif clicked == "blue":
        pygame.draw.rect(display, (50, 50, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
    #   Game Over
    if status == "menu":
        # background
        pygame.draw.rect(display, (0, 128, 0), pygame.Rect(0, 0, width / 2, height / 2))
        pygame.draw.rect(display, (128, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
        pygame.draw.rect(display, (128, 128, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
        pygame.draw.rect(display, (0, 0, 128), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
        if int(currentTime/250)-int(currentTime/1000)*4 == 1:
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
        elif int(currentTime/250)-int(currentTime/1000)*4 == 2:
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
        elif int(currentTime/250)-int(currentTime/1000)*4 == 3:
            pygame.draw.rect(display, (50, 50, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
        else:
            pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
        # title
        title = fontTitle.render("Simon!", True, (0, 0, 0))
        display.blit(title, (width / 2 - title.get_width() / 2, 50))
        # score
        scoreText = fontButton.render("Score: " + str(lastScore), True, (0, 0, 0))
        display.blit(scoreText, (width / 2 - scoreText.get_width() / 2, 100 + title.get_height()))
        highScoreText = fontButton.render("High Score: " + str(data["highScore"]), True, (0, 0, 0))
        display.blit(highScoreText,
                     (width / 2 - highScoreText.get_width() / 2, 100 + title.get_height() + scoreText.get_height()))
        # play button
        playPos = [width / 2, height / 2]
        playText = fontButton.render("Play!", True, (255, 255, 255))
        playButton = pygame.draw.rect(display, (0, 0, 0), (
            playPos[0] - playText.get_rect()[2] / 2 - 10, playPos[1] - playText.get_rect()[3] / 2 - 10,
            playText.get_rect()[2] + 20, playText.get_rect()[3] + 20))
        display.blit(playText, (playPos[0] - playText.get_width() / 2, playPos[1] - playText.get_height() / 2))
    elif status == "end":
        if lastTime + 250 < currentTime and gameOverPause:
            gameOverPause, lastTime = not gameOverPause, currentTime
        elif lastTime + 500 < currentTime:
            gameOverPos += 1
            if gameOverPos == 3:
                lastScore = len(pattern) - 1
                if lastScore > data["highScore"]:
                    data["highScore"] = lastScore
                    save()
                status = "menu"
            gameOverPause, lastTime = not gameOverPause, currentTime
        if not gameOverPause:
            pygame.draw.rect(display, (0, 255, 0), pygame.Rect(0, 0, width / 2, height / 2))
            pygame.draw.rect(display, (255, 0, 0), pygame.Rect(width / 2, 0, width / 2, height / 2))
            pygame.draw.rect(display, (255, 255, 0), pygame.Rect(0, height / 2, width / 2, height / 2))
            pygame.draw.rect(display, (50, 50, 255), pygame.Rect(width / 2, height / 2, width / 2, height / 2))
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
                    status, pattern, patternPos, patternPause, chosen, gameOverPos, patternTime = "", [], 0, True, [], 0, initialPatternTime
            elif patternPos == len(pattern) and len(chosen) < len(pattern):
                if sound:
                    soundGreen.stop()
                    soundRed.stop()
                    soundYellow.stop()
                    soundBlue.stop()
                if green.collidepoint(pos):
                    clicked = "green"
                    if sound:
                        soundGreen.play(-1)
                elif red.collidepoint(pos):
                    clicked = "red"
                    if sound:
                        soundRed.play(-1)
                elif yellow.collidepoint(pos):
                    clicked = "yellow"
                    if sound:
                        soundYellow.play(-1)
                elif blue.collidepoint(pos):
                    clicked = "blue"
                    if sound:
                        soundBlue.play(-1)
                chosen.append(clicked)
                lastTime = currentTime
                if not chosen == pattern[0:len(chosen)]:
                    status = "end"
    pygame.display.flip()
