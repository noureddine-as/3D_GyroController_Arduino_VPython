from numpy.core.defchararray import isdecimal
from serialmanager import *  # Import Serial Library
from visual import *

SENSIBILITY = 600;


def create_origin(orig_pt, orig, axis_length, yaxis):
    global gyro_x_axis, gyro_y_axis, gyro_z_axis
    center_pt = sphere(pos=orig_pt, radius=0.1, color=color.white, frame=orig)
    x_axis = arrow(pos=orig_pt, axis=gyro_x_axis, color=color.green, frame=orig)
    y_axis = arrow(pos=orig_pt, axis=gyro_y_axis, color=color.blue, frame=orig)
    z_axis = arrow(pos=orig_pt, axis=gyro_z_axis, color=color.red, frame=orig)

    xlabel = label(pos=orig_pt + (axis_length, 0, 0),
                   text='X', xoffset=0,
                   yoffset=0, space=10,
                   height=8, border=4,
                   font='sans', color=color.green, frame=orig)

    ylabel = label(pos=orig_pt + (0, 0, -axis_length),
                   text='Y', xoffset=0,
                   yoffset=0, space=10,
                   height=8, border=4,
                   font='sans', color=color.blue, frame=orig)

    zlabel = label(pos=orig_pt + (0, axis_length, 0),
                   text='Z', xoffset=0,
                   yoffset=0, space=10,
                   height=8, border=4,
                   font='sans', color=color.red, frame=orig)
    bx = box(pos=orig_pt, axis=yaxis, length=40, height=10, width=20, material=materials.wood, frame=orig)


s_ports = serial_ports()

if len(s_ports) == 0:
    print 'No serial ports available to read. Please connect your Arduino with the Gyro program.'
    exit()
if len(s_ports) == 1:
    arduino = serial.Serial(s_ports[0], 9600)  # Create Serial port object called arduinoSerialData
else:
    print 'Please choose which serial port you want to use, and enter its index:\n'
    i = 0
    for p in s_ports:
        print('%d - %s' % (i, s_ports[i]))
        i += 1
    choice = unicode(raw_input())
    if isdecimal(choice) and int(choice) < len(s_ports) :
        arduino = serial.Serial(s_ports[int(choice)], 9600)

if not(arduino.isOpen()) :
    exit()

scene.title = "3D GyroController - github.com/noureddine-as"
scene.height = 600
scene.width = 800

orig = frame()
orig.axis = (1, 0, 0)
orig.pos = (0, 0, 0)
orig_pt = vector(0, 0, 0)

# Axis got from the Gyroscope - see the (^)Y    (->)X    (+)Z
gyro_x_axis = (1, 0, 0)
gyro_y_axis = (0, 0, -1)
gyro_z_axis = (0, 1, 0)

create_origin(orig_pt, orig, 1.1, gyro_y_axis)

while (1):
    rate(100)
    if (arduino.inWaiting() > 0):
        # data is sent in this format: dx:dy:dz   where dx, dy, and dz are the angular displacements
        # in radians to be applied on the shapes but after being devided by SENSIBILITY
        data = arduino.readline()
        vals = data.split(':')
        if len(vals) == 3:
            # Rotate arround axis in counter-clockwise
            orig.rotate(angle=float(vals[0]) / SENSIBILITY, axis=gyro_x_axis, pos=orig.pos)
            orig.rotate(angle=float(vals[1]) / SENSIBILITY, axis=gyro_y_axis, pos=orig.pos)
            orig.rotate(angle=float(vals[2]) / SENSIBILITY, axis=gyro_z_axis, pos=orig.pos)