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

    def initOpenGL(self):
        glutInit(sys.argv)
        pygame.init()

        pygame.display.set_mode(self.config.display_size, DOUBLEBUF|OPENGL)
        gluPerspective(100, 1, 1, 100)


    """ Initialize the pattern texture in OpenGL """
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

    """ Render a flat surface with the pattern as texture """ 
    def renderSurface(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(0, 0, 0)
        glTexCoord2f(1,0)
        glVertex3f(self.image_x, 0, 0)
        glTexCoord2f(1,1)
        glVertex3f(self.image_x,  self.image_y, 0) 
        glTexCoord2f(0,1)
        glVertex3f(0,  self.image_y, 0)
        glEnd()
        glFlush()
        glDisable(GL_TEXTURE_2D)

    """ Reconstruct the original scene by positioning the camera at the same location """
    def positionCamera(self, rvec, tvec):
        # Move the camera in position.
        glTranslatef(tvec[0] / self.config.scale, 
                     tvec[1] / self.config.scale, 
                     tvec[2] / self.config.scale)

        # Point the camera to the right location.
        glRotate(rvec[0], 1, 0, 0)
        glRotate(rvec[1], 0, 1, 0)
        glRotate(rvec[2], 0, 0, 1)

    """ Render the constructed scene in OpenGL """
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




