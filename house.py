import sys
import numpy as np

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0

cameraY = 0.0
z_pos = 20.0
x_pos = 0.0
y_pos = 0.0

isPerspective = True

def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 

    #your code here
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if isPerspective:
        gluPerspective(40, DISPLAY_WIDTH / DISPLAY_HEIGHT, 5, 100)
    else:
        glOrtho(-10, 10, -10, 10, 1, 512)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    
    glRotated(cameraY, 0, 1, 0)
    glTranslated(x_pos, y_pos, -z_pos)
    
    
    drawHouse()
    glFlush()
    

def keyboard(key, x, y):

    global isPerspective
    global cameraY, z_pos, x_pos, y_pos

    if key == chr(27): 
        sys.exit(0)
  
    # move right.
    if key == b'd':
        x_pos -= np.cos(np.radians(cameraY))
        z_pos += np.sin(np.radians(cameraY))

    # move left.
    if key == b'a':
        x_pos += np.cos(np.radians(cameraY))
        z_pos -= np.sin(np.radians(cameraY))

    # move down.
    if key == b'f':
        y_pos += 1.0

    # move up.
    if key == b'r':
        y_pos -= 1.0

    # backward
    if key == b's':
        x_pos += np.sin(np.radians(cameraY))
        z_pos += np.cos(np.radians(cameraY))

    # forward
    if key == b'w':
        x_pos -= np.sin(np.radians(cameraY))
        z_pos -= np.cos(np.radians(cameraY))

    # turn left
    if key == b'q':  # Left arrow key
        cameraY -= 5

    # turn right
    if key == b'e':  # Right arrow key
        cameraY += 5

    # reset to home
    if key == b'h':
        
        cameraY = 0
        z_pos = 20.0
        x_pos = 0.0
        y_pos = 0.0
    
    # orthographic view
    if key == b'o':
        isPerspective = False
        
    # perspective view
    if key == b'p':
        isPerspective = True
  
    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()