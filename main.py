import face_recognition
import cv2
import numpy as np

#Source https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py

def moveto(top, right, bottom, left, frame):
    tolerance = 40
    height,width,_  = frame.shape  # float `width`
    center_height = (top - (top - bottom)/2)
    center_width = (right - (right - left)/2)
    if (height/2) - tolerance > center_height: print("up")
    elif (height/2) + tolerance < center_height: print("down")
    if (width/2) - tolerance > center_width: print("right")
    elif (width/2) + tolerance < center_width: print("left")
    else: print("good")

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

#person identifier
known_image = face_recognition.load_image_file("Roy.jpg")
target_encoding = face_recognition.face_encodings(known_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    target_encoding,
]
known_face_names = [
    "target",
]


while True:
    face_locations = []
    face_encodings = []
    face_names = []
    # Grab a single frame of video
    ret, frame = video_capture.read()

    magnification_factor = 2
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=1/magnification_factor, fy=1/magnification_factor)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    # Display the results
    for top, right, bottom, left in face_locations:
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= magnification_factor
        right *= magnification_factor
        bottom *= magnification_factor
        left *= magnification_factor

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        if name == "target":
            moveto(top, right, bottom, left, frame)



    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()