from flask import Flask, render_template, redirect, Response, url_for
import RPi.GPIO as GPIO
import io
import adafruit_us100
import serial
from picamera import PiCamera
import threading
import random
import time


app = Flask(__name__)

# Setting up GPIO nummbering to physcial pin numbers
GPIO.setmode(GPIO.BOARD)

# Defining UART pins for ultrasonic sensor
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3)
print(uart)
us100 = adafruit_us100.US100(uart)

# Warming up the US_100

distance = us100.distance
print(distance)

# Motor driver a pins
in1_a = 13
in2_a = 15
in3_a = 16
in4_a = 18

# Motor driver b pins
in1_b = 29
in2_b = 31
in3_b = 32
in4_b = 33

# Setting motor pins
GPIO.setup(in1_a, GPIO.OUT)
GPIO.setup(in2_a, GPIO.OUT)
GPIO.setup(in3_a, GPIO.OUT)
GPIO.setup(in4_a, GPIO.OUT)
GPIO.setup(in1_b, GPIO.OUT)
GPIO.setup(in2_b, GPIO.OUT)
GPIO.setup(in3_b, GPIO.OUT)
GPIO.setup(in4_b, GPIO.OUT)

# Setting up picamera
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 30

# Directory location to save pictures
save_directory = "/home/neko/Desktop/py_projects/rc_projects/py_images"

@app.route('/')
def index():
    return render_template('index.html')

# Defining a route for cleanup
@app.route('/cleanup')
def cleanup():
    GPIO.cleanup()
    camera.close()
    return redirect(url_for('index'))

@app.route('/move/forward')
def moveForward():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)

    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)
    return ''

@app.route('/move/backward')
def moveBackward():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)

    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)
    return ''

@app.route('/move/left')
def moveLeft():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)

    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)
    return ''

@app.route('/move/right')
def moveRight():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)

    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)
    return ''

// Inter cardinal directions(nw, ne, sw, se) 
@app.route('/move/nw')
def moveNW():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)

    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)
    return ''

@app.route('/move/ne')
def moveNE():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.LOW)

    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.LOW)
    return ''

@app.route('/move/sw')
def moveSW():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.LOW)

    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.LOW)
    return ''

@app.route('/move/se')
def moveSE():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)

    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)
    return ''

@app.route('/rotate/left')
def rotateLeft():
    GPIO.output(in1_a, GPIO.HIGH)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.HIGH)

    GPIO.output(in1_b, GPIO.HIGH)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.HIGH)
    return ''

@app.route('/rotate/right')
def rotateRight():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.HIGH)
    GPIO.output(in3_a, GPIO.HIGH)
    GPIO.output(in4_a, GPIO.LOW)

    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.HIGH)
    GPIO.output(in3_b, GPIO.HIGH)
    GPIO.output(in4_b, GPIO.LOW)
    return ''


@app.route('/stop')
def stop():
    GPIO.output(in1_a, GPIO.LOW)
    GPIO.output(in2_a, GPIO.LOW)
    GPIO.output(in3_a, GPIO.LOW)
    GPIO.output(in4_a, GPIO.LOW)

    GPIO.output(in1_b, GPIO.LOW)
    GPIO.output(in2_b, GPIO.LOW)
    GPIO.output(in3_b, GPIO.LOW)
    GPIO.output(in4_b, GPIO.LOW)
    return ''

# Defining function for image capture
def capture_image():
    camera.stop_preview()
    camera.resolution = (1920, 1080)
    timestamp = time.strftime("%d-%m-%Y_%H:%M:%S")
    image_path = f"{save_directory}/image_{timestamp}.jpg"
    print('Capturing Image...')
    camera.capture(image_path)
    print(f"Image captured and saved to {image_path}")
    camera.resolution = (320, 240)
    camera.start_preview()

@app.route('/capture/image')
def captureImg():
    capture_image()
    return ''

# Defining function for continuous generation of video frames
def generate_frames():
    stream = io.BytesIO()
    for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
        stream.seek(0)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + stream.read() + b'\r\n')
        stream.seek(0)
        stream.truncate()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Setting flag for auto mode
auto_mode = False
# Defining a function for obstacle detection
def obstacle_detection():
    global auto_mode
    random_rotate_direction = [rotateLeft, rotateRight]

    while auto_mode:
        distance = us100.distance
        time.sleep(0.1)
        print(distance)
        if distance <= 35:
            rndir = random.choice(random_rotate_direction)
            stop()
            #capture_image()
            time.sleep(1)
            while True:
                distance = us100.distance
                time.sleep(0.1)
                rndir()
                time.sleep(0.1)
                if distance >= 35:
                    rndir()
                    time.sleep(0.1)
                    stop()
                    time.sleep(1)
                    break
        else:
            moveForward()
            time.sleep(0.1)

@app.route('/auto-mode')
def auto():
    global auto_mode
    auto_mode = not auto_mode
    if auto_mode:
        thread = threading.Thread(target=obstacle_detection)
        thread.start()
    return ''


if __name__ == '__main__':
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Error detected: {e}")
    finally:
        GPIO.cleanup()
        camera.stop_preview()
        camera.close()
