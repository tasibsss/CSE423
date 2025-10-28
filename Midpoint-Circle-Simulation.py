from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

W_Width, W_Height = 800,800
l = []
checker = None
speed = 0.4
flag = 1


def midpoint_line(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if dx >= 0 and dy >= 0:
        if abs(dx) > abs(dy):
            zone = 0
        else:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
            zone = 1

    if dx < 0 and dy > 0:
        if abs(dx) < abs(dy):
            x0, y0 = y0, -x0
            x1, y1 = y1, -x1
            zone = 2
        else:
            x0, y0 = -x0, y0
            x1, y1 = -x1, y1
            zone = 3

    if dx <= 0 and dy <= 0:
        if abs(dx) > abs(dy):
            x0, y0 = -x0, -y0
            x1, y1 = -x1, -y1
            zone = 4
        else:
            x0, y0 = -y0, -x0
            x1, y1 = -y1, -x1
            zone = 5

    if dx > 0 and dy < 0:
        if abs(dx) < abs(dy):
            x0, y0 = -y0, x0
            x1, y1 = -y1, x1
            zone = 6
        else:
            x0, y0 = x0, -y0
            x1, y1 = x1, -y1
            zone = 7

    draw_line(x0, y0, x1, y1, zone)


def draw_line(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dy - dx
    E = 2 * dy
    NE = 2 * (dy - dx)
    x = x0
    y = y0
    points = [[x, y]]
    while x < x1:
        if d <= 0:
            d += E
            x += 1
        else:
            d += NE
            x += 1
            y += 1
        points.append([x, y])

    if zone == 1:
        for i in points:
            i[0], i[1] = i[1], i[0]
    elif zone == 2:
        for i in points:
            i[0], i[1] = -i[1], i[0]
    elif zone == 3:
        for i in points:
            i[0], i[1] = -i[0], i[1]
    elif zone == 4:
        for i in points:
            i[0], i[1] = -i[0], -i[1]
    elif zone == 5:
        for i in points:
            i[0], i[1] = -i[1], -i[0]
    elif zone == 6:
        for i in points:
            i[0], i[1] = i[1], -i[0]
    elif zone == 7:
        for i in points:
            i[0], i[1] = i[0], -i[1]

    for i in points:
        glPointSize(1)
        glBegin(GL_POINTS)
        glVertex2f(i[0], i[1])
        glEnd()

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y
    return a,b

def midpoint_circle(c, r):
    global checker
    glColor3f(1.0, 0.0, 0.0)
    glPointSize(3)

    d = 1 - r
    x = 0
    y = r
    points = [[x, y]]
    while x < y:
        if d >= 0:
            d += (2 * x - 2 * y + 5)
            x += 1
            y -= 1
        else:
            d += (2 * x + 3)
            x += 1
        points.append([x, y])

    temp = []
    for i in points:
        temp.extend([[i[1], i[0]], [-i[0], i[1]], [-i[1], i[0]], [-i[1], -i[0]], [-i[0], -i[1]], [i[0], -i[1]], [i[1], -i[0]]])
    points += temp

    for i in points:
        i[0] += c[0]
        i[1] += c[1]
        if i[0] >= 400 or i[0] <= -400 or i[1] >= 400 or i[1] <= -400:
            checker = True
            break

    if checker == True:
        return

    for i in points:
        glBegin(GL_POINTS)
        glVertex2f(i[0], i[1])
        glEnd()

def mouseListener(button, state, x, y):

    if button == GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            c_x, c_y = convert_coordinate(x, y)
            l.append([[c_x,c_y], 30])

    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed

    if key == GLUT_KEY_RIGHT:
        speed += 0.1
    if key == GLUT_KEY_LEFT:
        if speed > 0.1:
            speed -= 0.1

    glutPostRedisplay()

def keyboardListener(key, x, y):
    global flag
    if key==b' ':
        if flag == 0:
            flag = 1
        else:
            flag = 0

    glutPostRedisplay()

def animate():
    glutPostRedisplay()
    if flag == 1:
        for i in l:
            i[1] += speed

def display():
    global checker

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0,0,0,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,401,	0,0,0,	0,1,0)
    glMatrixMode(GL_MODELVIEW)

    ind = []
    for i in range(len(l)):
        midpoint_circle(l[i][0], l[i][1])
        if checker == True:
            ind.append(i)
            checker = None
    for i in ind:
        l.pop(i)

    glutSwapBuffers()


def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90,	1,	1,	1500)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(50, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"OpenGL Coding Practice")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)

glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()