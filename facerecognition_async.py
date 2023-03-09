# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

#screenshot command in bash
#fswebcam -r 1280x720 --no-banner filename.jpg

import face_recognition
import picamera
import numpy as np
import cv2
import asyncio

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
#camera = picamera.PiCamera()
#camera.resolution = (320, 240)
#output = np.empty((240, 320, 3), dtype=np.uint8)

cam = cv2.VideoCapture(0) 
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
# width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
# output = np.empty((width,height,3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
evan_image = face_recognition.load_image_file("evan1.jpg")
evan_face_encoding = face_recognition.face_encodings(evan_image)[0]

hunter_image = face_recognition.load_image_file("hunter1.jpg")
hunter_face_encoding = face_recognition.face_encodings(hunter_image)[0]

riley_image = face_recognition.load_image_file("riley1.jpg")
riley_face_encoding = face_recognition.face_encodings(riley_image)[0]

# Initialize some variables
face_locations = []
face_encodings = []

async def find_faces(face_locations, face_encodings):
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces([evan_face_encoding, hunter_face_encoding, riley_face_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Evan Lee"
        if match[1]:
            name = "Hunter Egeland"
        if match[2]:
            name = "Riley Monwai"

        print("I see someone named {}!".format(name))


async def getFaceLocation(img):
    
    return face_recognition.face_locations(img)


async def getFaceEncoding(img, location):
    return face_recognition.face_encodings(img, location)


async def getFacesFromCam(face_locations, face_encodings):
    # Grab a single frame of video from the RPi camera as a numpy array
    #camera.capture(output, format="rgb")
    ret, image = cam.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image',gray)
    
    # Find all the faces and face encodings in the current frame of video
    face_locations = await getFaceLocation(image)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = await getFaceEncoding(image, face_locations)

    await find_faces(face_locations, face_encodings)

print("Capturing image.")

while True:

    asyncio.run(getFacesFromCam(face_locations, face_encodings))

    # # Grab a single frame of video from the RPi camera as a numpy array
    # #camera.capture(output, format="rgb")
    # ret, image = cam.read()
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('image',gray)
    
    # # Find all the faces and face encodings in the current frame of video
    # face_locations = face_recognition.face_locations(image)
    # print("Found {} faces in image.".format(len(face_locations)))
    # face_encodings = face_recognition.face_encodings(image, face_locations)

    
    # Loop over each face found in the frame to see if it's someone we know.
    # for face_encoding in face_encodings:
    #     # See if the face is a match for the known face(s)
    #     match = face_recognition.compare_faces([evan_face_encoding, hunter_face_encoding, riley_face_encoding], face_encoding)
    #     name = "<Unknown Person>"

    #     if match[0]:
    #         name = "Evan Lee"
    #     if match[1]:
    #         name = "Hunter Egeland"
    #     if match[2]:
    #         name = "Riley Monwai"

    #     print("I see someone named {}!".format(name))

    k = cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
print("Done.")
       
