# Import a library of functions called 'pygame'
import pygame
import numpy as np
from math import pi

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Point3D:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
class Line3D():
    
    def __init__(self, start, end):
        self.start = start
        self.end = end

def loadOBJ(filename):
    
    vertices = []
    indices = []
    lines = []
    
    f = open(filename, "r")
    for line in f:
        t = str.split(line)
        if not t:
            continue
        if t[0] == "v":
            vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
            
        if t[0] == "f":
            for i in range(1,len(t) - 1):
                index1 = int(str.split(t[i],"/")[0])
                index2 = int(str.split(t[i+1],"/")[0])
                indices.append((index1,index2))
            
    f.close()
    
    #Add faces as lines
    for index_pair in indices:
        index1 = index_pair[0]
        index2 = index_pair[1]
        lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
        
    #Find duplicates
    duplicates = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            line1 = lines[i]
            line2 = lines[j]
            
            # Case 1 -> Starts match
            if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
                if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
                    duplicates.append(j)
            # Case 2 -> Start matches end
            if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
                if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
                    duplicates.append(j)
                    
    duplicates = list(set(duplicates))
    duplicates.sort()
    duplicates = duplicates[::-1]
    
    #Remove duplicates
    for j in range(len(duplicates)):
        del lines[duplicates[j]]
    
    return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
    
    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    
    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
    
    return tire

    
# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

#my colors
PASTEL_RED = (255,179,186)
PASTEL_YELLOW = (255,255,186)
PASTEL_GREEN = (186,255,201)
PASTEL_BLUE = (186,225,255)
PASTEL_PURPLE = (238,203,255)
PASTEL_ORANGE = (255,223,186)


# Set the height and width of the screen
size = [512, 512]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Lab 7 - Tyler Timothy")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)


camera_position = [0, 0, 0]
cam_x = 0
cam_y = 0
cam_z = 0
camera_rotation_y = 0

zoomx = .3
zoomy = .3
near_clip = 7
far_clip = 110
clip_matrix = np.array([
        [zoomx, 0,     0,                                               0                                                   ],
        [0,     zoomy, 0,                                               0                                                   ],
        [0,     0,     (far_clip + near_clip) / (far_clip - near_clip), (-2 * near_clip * far_clip) / (far_clip - near_clip)],
        [0,     0,     1,                                               0                                                   ]
    ])

transform_matrix_stack = np.array([])

#get transformations into world space
#object is the created object, 
def to_world_space(object, translation=[0,0,0], x_rotation=0, y_rotation=0, z_rotation=0):
    global transform_matrix_stack
    transformed_object = []

    rx = np.radians(x_rotation)
    ry = np.radians(y_rotation)
    rz = np.radians(z_rotation)
    
    rotation_matrix_x = np.array([
        [1, 0,          0,           0],
        [0, np.cos(rx), -np.sin(rx), 0],
        [0, np.sin(rx),  np.cos(rx), 0],
        [0, 0,           0,          1]
    ])

    rotation_matrix_y = np.array([
        [np.cos(ry),  0, np.sin(ry), 0],
        [0,           1, 0,          0],
        [-np.sin(ry), 0, np.cos(ry), 0],
        [0,           0, 0,          1]
    ])

    rotation_matrix_z = np.array([
        [np.cos(rz), -np.sin(rz), 0, 0],
        [np.sin(rz), np.cos(rz),  0, 0],
        [0,          0,           1, 0],
        [0,          0,           0, 1]
    ])

    translation_matrix = np.array([
        [1, 0, 0, translation[0]],
        [0, 1, 0, translation[1]],
        [0, 0, 1, translation[2]],
        [0, 0, 0, 1             ]
    ])

    
     # make the rotation matrix Z -> Y -> X
    rotation_matrix = np.matmul(rotation_matrix_x, np.matmul(rotation_matrix_y, rotation_matrix_z))
    
    # rotate then translate into one matrix
    transform_matrix = np.matmul(translation_matrix, rotation_matrix)
    transform_matrix_stack = transform_matrix

    # apply transformations
    for line in object:
        #create homogeneous matrices, multiply them by the transform, clip the homogeneous coordinate
        start = np.matmul(transform_matrix, [line.start.x, line.start.y, line.start.z, 1])[:-1]
        end = np.matmul(transform_matrix, [line.end.x, line.end.y, line.end.z, 1])[:-1]

        transformed_line = Line3D(Point3D(*start), Point3D(*end))
        transformed_object.append(transformed_line)

    return transformed_object

def matrix_stack(object, translation=[0,0,0], x_rotation=0, y_rotation=0, z_rotation=0):
    global transform_matrix_stack
    transformed_object = []

    rx = np.radians(x_rotation)
    ry = np.radians(y_rotation)
    rz = np.radians(z_rotation)
    
    rotation_matrix_x = np.array([
        [1, 0,          0,           0],
        [0, np.cos(rx), -np.sin(rx), 0],
        [0, np.sin(rx),  np.cos(rx), 0],
        [0, 0,           0,          1]
    ])

    rotation_matrix_y = np.array([
        [np.cos(ry),  0, np.sin(ry), 0],
        [0,           1, 0,          0],
        [-np.sin(ry), 0, np.cos(ry), 0],
        [0,           0, 0,          1]
    ])

    rotation_matrix_z = np.array([
        [np.cos(rz), -np.sin(rz), 0, 0],
        [np.sin(rz), np.cos(rz),  0, 0],
        [0,          0,           1, 0],
        [0,          0,           0, 1]
    ])

    translation_matrix = np.array([
        [1, 0, 0, translation[0]],
        [0, 1, 0, translation[1]],
        [0, 0, 1, translation[2]],
        [0, 0, 0, 1             ]
    ])

    rotation_matrix = np.matmul(rotation_matrix_x, np.matmul(rotation_matrix_y, rotation_matrix_z))

    this_level_matrix = np.matmul(transform_matrix_stack, np.matmul(translation_matrix, rotation_matrix))
    
    transformed_object = []
    for line in object:
        start = np.matmul(this_level_matrix, [line.start.x, line.start.y, line.start.z, 1])[:-1]
        end = np.matmul(this_level_matrix, [line.end.x, line.end.y, line.end.z, 1])[:-1]
        #print(start)
        #print(end)

        transformed_line = Line3D(Point3D(*start), Point3D(*end))
        transformed_object.append(transformed_line)

    return transformed_object

#create a single matrix to convert from world space to camera space
def to_camera_space(object, cam_x, cam_y, cam_z , camera_rotation):
    transformed_object = []

    #convert rotations from degrees to radians
    ry = np.radians(camera_rotation)
    
    #rotation matrix
    rotation_matrix = np.array([
        [np.cos(ry),  0, np.sin(ry), 0],
        [0,           1, 0,          0],
        [-np.sin(ry), 0, np.cos(ry), 0],
        [0,           0, 0,          1]
    ])
    
    #translation matrix
    translation_matrix = np.array([
        [1, 0, 0, -cam_x],
        [0, 1, 0, -cam_y],
        [0, 0, 1, -cam_z],
        [0, 0, 0, 1                  ]
    ])
    
    #combine rotation and translation matrices
    transform_matrix = np.matmul(rotation_matrix, translation_matrix)
    
    #apply transformations
    for line in object:
        start = np.matmul(transform_matrix, [line.start.x, line.start.y, line.start.z, 1])[:-1]
        end = np.matmul(transform_matrix, [line.end.x, line.end.y, line.end.z, 1])[:-1]
        #print(start)
        #print(end)

        transformed_line = Line3D(Point3D(*start), Point3D(*end))
        transformed_object.append(transformed_line)

    return transformed_object


def to_clip_and_project(object):
    transformed_object = []

    for line in object:
        start_homogeneous = np.matmul(clip_matrix, [line.start.x, line.start.y, line.start.z, 1])
        end_homogeneous = np.matmul(clip_matrix, [line.end.x, line.end.y, line.end.z, 1])

        sx = start_homogeneous[0]
        sy = start_homogeneous[1]
        sz = start_homogeneous[2]
        sw = start_homogeneous[3]

        ex = start_homogeneous[0]
        ey = start_homogeneous[1]
        ez = start_homogeneous[2]
        ew = start_homogeneous[3]

        if (sx > -sw and sx < sw and sy > -sw and sy < sw and sz > -sw and sz < sw and ex > -ew and ex < ew and ey > -ew and ey < ew and ez > -ew and ez < ew):
            start = start_homogeneous[:3] / start_homogeneous[3]
            end = end_homogeneous[:3] / end_homogeneous[3]
            transformed_line = Line3D(Point3D(*start), Point3D(*end))
            transformed_object.append(transformed_line)

    return transformed_object


def to_screen_space(object):
    global size
    transformed_object = []
    
    #rotation matrices
    screen_space_matrix = np.array([
        [size[0]/2, 0,          0],
        [0,         size[1]/2, 0],
        [0,         0,          1]
    ])

    for line in object:
        start = np.matmul(screen_space_matrix, [line.start.x, line.start.y, line.start.z])
        end = np.matmul(screen_space_matrix, [line.end.x, line.end.y, line.end.z])

        transformed_line = Line3D(Point3D(*start), Point3D(*end))
        transformed_object.append(transformed_line)

    return transformed_object

#Loop until the user clicks the close button.
while not done:
    # This limits the while loop to a max of 100 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(100)

    # Clear the screen and set the screen background
    screen.fill(BLACK)

    #Controller Code#
    #####################################################################

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done=True
            
    pressed = pygame.key.get_pressed()

    #home
    if pressed[pygame.K_h]:
        cam_x = 0
        cam_y = 0
        cam_z = 0
        camera_rotation_y = 0

    #forward
    if pressed[pygame.K_w]:
        cam_x -= np.sin(np.radians(camera_rotation_y)) / 5
        cam_z += np.cos(np.radians(camera_rotation_y)) / 5 
        print(cam_x, ", ", cam_y, ", ", cam_z)


    #backward
    if pressed[pygame.K_s]:
        cam_x += np.sin(np.radians(camera_rotation_y)) / 5
        cam_z -= np.cos(np.radians(camera_rotation_y)) / 5
        print(cam_x, ", ", cam_y, ", ", cam_z)


    #left
    if pressed[pygame.K_a]:
        cam_x -= np.cos(np.radians(camera_rotation_y)) / 5
        cam_z -= np.sin(np.radians(camera_rotation_y)) / 5
        print(cam_x, ", ", cam_y, ", ", cam_z)


    #right
    if pressed[pygame.K_d]:
        cam_x += np.cos(np.radians(camera_rotation_y)) / 5
        cam_z += np.sin(np.radians(camera_rotation_y)) / 5
        print(cam_x, ", ", cam_y, ", ", cam_z)

    #up
    if pressed[pygame.K_r]:
        cam_y += 0.2

    #down
    if pressed[pygame.K_f]:
        cam_y -= 0.2

    #rotate left
    if pressed[pygame.K_q]:
        camera_rotation_y += .5
        print(camera_rotation_y)

    #rotate right
    if pressed[pygame.K_e]:
        camera_rotation_y -= .5
        print(camera_rotation_y)
        
    #Viewer Code#
    #####################################################################

    #create objects
    house_one = loadHouse()
    house_two = loadHouse()
    house_three = loadHouse()
    house_four = loadHouse()
    car_one = loadCar()
    tire_one = loadTire()
    tire_two = loadTire()
    tire_three = loadTire()
    tire_four = loadTire()

    #objects to world space
    house_one = to_world_space(house_one, [0, -6, 100], y_rotation = 180)
    house_two = to_world_space(house_two, [-11, -6, 100], y_rotation = 180)
    house_three = to_world_space(house_three, [11, -6, 100], y_rotation = 180)
    house_four = to_world_space(house_four, [22, -6, 100], y_rotation = 180)
    car_one = to_world_space(car_one, [4, -5, 75], y_rotation = 10)

    #matrix stack
    tire_one = matrix_stack(tire_one, [-2, 0, -2], z_rotation= 65)
    tire_two = matrix_stack(tire_two, [-2, 0, 2], z_rotation= 35)
    tire_three = matrix_stack(tire_three, [2, 0, -2], z_rotation= 0)
    tire_four = matrix_stack(tire_four, [2, 0, 2], z_rotation= 80)

    #objects to camera space
    house_one = to_camera_space(house_one, cam_x, cam_y, cam_z, camera_rotation_y)
    house_two = to_camera_space(house_two, cam_x, cam_y, cam_z, camera_rotation_y)
    house_three = to_camera_space(house_three, cam_x, cam_y, cam_z, camera_rotation_y)
    house_four = to_camera_space(house_four, cam_x, cam_y, cam_z, camera_rotation_y)
    car_one = to_camera_space(car_one, cam_x, cam_y, cam_z, camera_rotation_y)
    tire_one = to_camera_space(tire_one, cam_x, cam_y, cam_z, camera_rotation_y)
    tire_two = to_camera_space(tire_two, cam_x, cam_y, cam_z, camera_rotation_y)
    tire_three = to_camera_space(tire_three, cam_x, cam_y, cam_z, camera_rotation_y)
    tire_four = to_camera_space(tire_four, cam_x, cam_y, cam_z, camera_rotation_y)


    #objects clipping for optimization 
    house_one = to_clip_and_project(house_one)
    house_two = to_clip_and_project(house_two)
    house_three = to_clip_and_project(house_three)
    house_four = to_clip_and_project(house_four)
    car_one = to_clip_and_project(car_one)
    tire_one = to_clip_and_project(tire_one)
    tire_two = to_clip_and_project(tire_two)
    tire_three = to_clip_and_project(tire_three)
    tire_four = to_clip_and_project(tire_four)

    #objects to screen space
    house_one = to_screen_space(house_one)
    house_two = to_screen_space(house_two)
    house_three = to_screen_space(house_three)
    house_four = to_screen_space(house_four)
    car_one = to_screen_space(car_one)
    tire_one = to_screen_space(tire_one)
    tire_two = to_screen_space(tire_two)
    tire_three = to_screen_space(tire_three)
    tire_four = to_screen_space(tire_four)

    for s in house_one:
        pygame.draw.line(screen, PASTEL_YELLOW, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))
    
    for s in house_two:
        pygame.draw.line(screen, PASTEL_GREEN, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    for s in house_three:
        pygame.draw.line(screen, PASTEL_RED, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    for s in house_four:
        pygame.draw.line(screen, PASTEL_ORANGE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    for s in car_one:
        pygame.draw.line(screen, PASTEL_PURPLE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    for s in tire_one:
        pygame.draw.line(screen, PASTEL_BLUE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    for s in tire_two:
        pygame.draw.line(screen, PASTEL_BLUE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    for s in tire_three:
        pygame.draw.line(screen, PASTEL_BLUE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    for s in tire_four:
        pygame.draw.line(screen, PASTEL_BLUE, (20*s.start.x+200, -20*s.start.y+200), (20*s.end.x+200, -20*s.end.y+200))

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()
 
# Be IDLE friendly
pygame.quit()
