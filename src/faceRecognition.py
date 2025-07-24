import face_recognition
import cv2
import numpy as np

def recognize_face_and_get_name() -> str:
    frameCounter = 0
    checkRate = 30 #used to say how often we run the facial recognition so as not to slow down computer
    #Get a reference to webcam #0
    foundName = ""

    video_capture = cv2.VideoCapture(0)

    #Load sample pictures
    #NOTE: REPLACE THESE WITH YOUR OWN PICTURES
    jack_image = face_recognition.load_image_file("private/IMG_2840.JPG")
    jack_face_recognition = face_recognition.face_encodings(jack_image)[0]


    # Create arrays of known face encodings and their names
    known_face_encodings = [
        jack_face_recognition
    ]

    known_face_names = [
        "Jack"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True and foundName == "":
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frameCounter = frameCounter + 1

        # Only process every other frame of video to save time
        if (frameCounter%checkRate == 0) or frameCounter < 2:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            #Fix compute_face_desciptor crash
            rgb_small_frame = cv2.cvtColor(rgb_small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)

            face_names = []

            for found_face in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings,found_face)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    if(foundName != ""):
                        foundName += " and " + name
                    else:
                        foundName = name



                # Or instead, use the known face with the smallest distance to the new face
                #face_distances = face_recognition.face_distance(known_face_encodings, found_face)
                #best_match_index = np.argmin(face_distances)
                #if matches[best_match_index]:
                #    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left - 30, top - 30), (right + 30, bottom + 30), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left - 30, bottom - 5), (right + 30, bottom + 30), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 36, bottom + 20), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    return foundName

#base Function
def recognize_face():
    frameCounter = 0
    checkRate = 30 #used to say how often we run the facial recognition so as not to slow down computer
    #Get a reference to webcam #0

    video_capture = cv2.VideoCapture(0)

    #Load sample pictures
    #NOTE: REPLACE THESE WITH YOUR OWN PICTURES
    jack_image = face_recognition.load_image_file("private/IMG_2840.JPG")
    jack_face_recognition = face_recognition.face_encodings(jack_image)[0]


    # Create arrays of known face encodings and their names
    known_face_encodings = [
        jack_face_recognition
    ]

    known_face_names = [
        "Dana",
        "Jack"
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        frameCounter = frameCounter + 1

        # Only process every other frame of video to save time
        if (frameCounter%checkRate == 0) or frameCounter < 2:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            #Fix compute_face_desciptor crash
            rgb_small_frame = cv2.cvtColor(rgb_small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)

            face_names = []

            for found_face in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings,found_face)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]


                # Or instead, use the known face with the smallest distance to the new face
                #face_distances = face_recognition.face_distance(known_face_encodings, found_face)
                #best_match_index = np.argmin(face_distances)
                #if matches[best_match_index]:
                #    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left - 30, top - 30), (right + 30, bottom + 30), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left - 30, bottom - 5), (right + 30, bottom + 30), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 36, bottom + 20), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

