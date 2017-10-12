import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class PerspectiveRenderer():

    def __init__(self, config):
        self.config = config

        self.initOpenGL()
        self.createSurfaceTexture()

        # self.render()

    def initOpenGL(self):
        glutInit(sys.argv)
        pygame.init()
        display = (800,600)
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
        gluPerspective(100, 1, 1, 100)

        
    def createSurfaceTexture(self):
        img = pygame.image.load(self.config.pattern_path)
        textureData = pygame.image.tostring(img, "RGB", 1)
        width = img.get_width()
        height = img.get_height()

        image_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, image_texture)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glEnable(GL_TEXTURE_2D)

        self.image_x = width / self.config.scale
        self.image_y = height / self.config.scale

    def renderSurface(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glBegin(GL_QUADS)
        glTexCoord2f(0,1)
        glVertex3f(0,  self.image_y, 0)
        glTexCoord2f(0,0)
        glVertex3f(0, 0, 0)
        glTexCoord2f(1,0)
        glVertex3f(self.image_x, 0, 0)
        glTexCoord2f(1,1)
        glVertex3f(self.image_x,  self.image_y, 0) 
        glEnd()
        glFlush()
        glDisable(GL_TEXTURE_2D)

    def positionCamera(self, rvec, tvec):
        # glTranslatef(-288/self.config.scale, 199/self.config.scale, -1126/self.config.scale)

        # glRotate(-10, 1, 0, 0)
        # glRotate(-7.89, 0, 1, 0)
        # glRotate(129.87, 0, 0, 1)
        glTranslatef(tvec[0] / self.config.scale, 
                     tvec[1] / self.config.scale, 
                     tvec[2] / self.config.scale)

        glRotate(rvec[0], 1, 0, 0)
        glRotate(rvec[1], 0, 1, 0)
        glRotate(rvec[2], 0, 0, 1)

    def render(self):
        self.renderSurface()

        pygame.display.flip()
        pygame.time.wait(100)

        # Wait for exit events
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()




