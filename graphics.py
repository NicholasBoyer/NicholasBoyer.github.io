from vpython import *

scene.title = "3D Graphics"
scene.width = 800
scene.height = 600
scene.background = color.magenta
scene.camera.pos = vector(10, 3, 10)
scene.camera.axis = vector(-10, -3, -10)

# Print controls
print("Use the AWSD keys to move camera orientation. Camera orientation can also be moved with the cursor by holding down \
the right mouse button. Use the Q and E keys to zoom in and out. Press the backspace key to exit the program.")

# Create a plane
ground = box(pos=vector(0, -0.5, 0), size=vector(100, 0.5, 100), color=color.green)

# Create a platform
platform = box(pos=vector(0, -.25, 0), size=vector(10, 0.5, 10), color=vector(0,0.8,0))

# Create a sphere
sphere1 = sphere(pos=vector(-3, 1, 0), radius=1, color=color.red)

# Create a cube
cube1 = box(pos=vector(0, 1, 0), size=vector(2, 2, 2), color=color.blue)

# Create a cone
cone1 = cone(pos=vector(3, 0, 0), axis=vector(0, 2, 0), radius=1, color=color.orange)

# Function to add a basic castle with customizable position
def create_castle(x, y):
    # Castle base
    base = box(pos=vector(x + 5, 0, y + 5), size=vector(4, 2, 4), color=color.gray(0.6))
    
    # Four corner towers
    tower_radius = 0.6
    tower_height = 2.5
    tower_positions = [
        vector(x + 3, -0.5, y + 3),
        vector(x + 7, -0.5, y + 3),
        vector(x + 3, -0.5, y + 7),
        vector(x + 7, -0.5, y + 7)
    ]
    towers = []
    for pos in tower_positions:
        towers.append(cylinder(pos=pos, axis=vector(0, tower_height, 0), radius=tower_radius, color=color.gray(0.8)))
    
    # Add battlements on top of the base
    battlement_height = 0.5
    battlement_width = 0.8
    battlement_spacing = 1
    battlements = []
    for i in range(-2, 3, battlement_spacing):
        battlements.append(box(pos=vector(x + 5 + i * battlement_width, 1.5, y + 3), size=vector(battlement_width, battlement_height, 0.5), color=color.gray(0.7)))
        battlements.append(box(pos=vector(x + 5 + i * battlement_width, 1.5, y + 7), size=vector(battlement_width, battlement_height, 0.5), color=color.gray(0.7)))
        battlements.append(box(pos=vector(x + 3, 1.5, y + 5 + i * battlement_width), size=vector(0.5, battlement_height, battlement_width), color=color.gray(0.7)))
        battlements.append(box(pos=vector(x + 7, 1.5, y + 5 + i * battlement_width), size=vector(0.5, battlement_height, battlement_width), color=color.gray(0.7)))

# Create a castle at position (-10, -10)
create_castle(-15, -15)

def move_camera(evt):
    s = 0.5
    view_direction = scene.camera.axis.norm()  # normalized viewing direction
    right_direction = cross(view_direction, vector(0, 1, 0)).norm()  # right direction relative to the camera
    up_direction = cross(right_direction, view_direction).norm()  # up direction relative to the camera

    if evt.key == 'left' or evt.key == 'a':
        scene.camera.pos -= right_direction * s
    elif evt.key == 'right' or evt.key == 'd':
        scene.camera.pos += right_direction * s
    elif evt.key == 'up' or evt.key == 'w':
        scene.camera.pos += up_direction * s
    elif evt.key == 'down' or evt.key == 's':
        scene.camera.pos -= up_direction * s
    elif evt.key == 'q':
        scene.camera.pos += view_direction * s
    elif evt.key == 'e':
        scene.camera.pos -= view_direction * s

scene.bind('keydown', move_camera)


g = 9.8  # acceleration due to gravity
jump_velocity = 5  # initial jump velocity
cube1.velocity = vector(0, jump_velocity, 0)
ground_level = cube1.pos.y

while True:
    rate(100)
    # Update cube velocity + position
    cube1.velocity.y -= g * 0.01 
    cube1.pos.y += cube1.velocity.y * 0.01 

    # Plane collision check
    if cube1.pos.y < ground_level:
        cube1.pos.y = ground_level  
        cube1.velocity.y = jump_velocity  

    # Exit
    if "backspace" in keysdown():
        break