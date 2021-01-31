import pygame
from win32.win32api import GetSystemMetrics
import sys
from os.path import join
from math import ceil, sqrt
from datetime import datetime


class PygameWindow:
	def __init__(self, windowDimensions, isFullScreen=False):
		self._window = pygame.display.set_mode(
			windowDimensions, pygame.FULLSCREEN)

	def clearWindow(self):
		self._window.fill((0, 0, 0))

	def render(self, gameObject, gameObjectPos=None, gameObjectRect=None):
		if gameObjectRect == None:
			if gameObjectPos == None:
				self._window.blit(gameObject, (0, 0))
			else:
				self._window.blit(gameObject, gameObjectPos)
		else:
			self._window.blit(gameObject, gameObjectRect)


def showScreensaver():
	pygame.init()
	displayDimensions = getDisplayDimensions()
	pygameWindow = PygameWindow(displayDimensions, True)
	pygame.mouse.set_visible(False)

	isRunning = True
	framesPerSecond = 12
	mousePos = None
	displayDiagonal = sqrt(
		pow(displayDimensions[0], 2) + pow(displayDimensions[1], 2))
	# Big number here is a scaling value to keep fontsize in proportion to screen size
	fontSize = int(round(displayDiagonal*0.10213775825678311533929954954051))
	ubuntuRegularFont = getFont('fonts/Ubuntu-Regular.ttf', fontSize)
	fernImg = getImage('images/fern.jpg')
	scaleImageToFit(fernImg, displayDimensions)

	while isRunning:
		pygame.time.delay(int(round(1000/framesPerSecond)))
		pygameWindow.clearWindow()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				isRunning = False
			elif event.type == pygame.MOUSEMOTION:
				updatedMousePos = pygame.mouse.get_pos()
				if mousePos == None:
					mousePos = updatedMousePos
				elif mousePos != updatedMousePos:
					isRunning = False
			elif event.type == pygame.KEYDOWN:
				isRunning = False

		# Render background image
		displayWidth = displayDimensions[0]
		displayHeight = displayDimensions[1]
		_, _, fernImgWidth, fernImgHeight = fernImg.get_rect()
		fernImgX = int(round(displayWidth/2 - fernImgWidth/2))
		fernImgY = int(round(displayHeight/2 - fernImgHeight/2))
		pygameWindow.render(fernImg, gameObjectPos=(fernImgX, fernImgY))

		# Render time
		currentTimeStr = datetime.now().strftime('%I %M')
		colorWhite = (255, 255, 255)
		shouldAntialias = True
		timeText = ubuntuRegularFont.render(
			currentTimeStr, shouldAntialias, colorWhite)
		timeTextRect = timeText.get_rect(
			center=(displayWidth/2, displayHeight/2))
		pygameWindow.render(timeText, gameObjectRect=timeTextRect)

		pygame.display.update()

	pygame.quit()


def getDisplayDimensions():
	displayWidth = GetSystemMetrics(0)
	displayHeight = GetSystemMetrics(1)
	return (displayWidth, displayHeight)


def getFont(relativePath, fontSize):
	if getattr(sys, 'frozen', False):
		return pygame.font.Font(join(sys._MEIPASS, relativePath), fontSize)
	else:
		return pygame.font.Font(relativePath, fontSize)


def getImage(relativePath):
	if getattr(sys, 'frozen', False):
		return pygame.image.load(join(sys._MEIPASS, relativePath))
	else:
		return pygame.image.load(relativePath)


def scaleImageToFit(image, displayDimensions):
	displayWidth = displayDimensions[0]
	displayHeight = displayDimensions[1]
	_, _, imgWidth, imgHeight = image.get_rect()
	newImgWidth = displayWidth
	newImgHeight = (displayWidth/imgWidth)*imgHeight
	if newImgHeight < displayHeight:
		newImgHeight = displayHeight
		newImgWidth = (displayHeight/imgHeight)*imgWidth
	image = pygame.transform.smoothscale(
		image, (int(ceil(newImgWidth)), int(ceil(newImgHeight))))


def showOptions():
	pass


if __name__ == '__main__':
	if len(sys.argv) > 1:
		argLower = sys.argv[1].lower()
		if argLower == '/s':
			showScreensaver()
		elif argLower == '/c':
			showOptions()
		elif argLower == '/d':
			showScreensaver()
		elif argLower == '/p':
			pass
		else:
			pass
	else:
		showScreensaver()
