from fd.settings import IMG_ROOT
import numpy as np
import cv2
import os


def saveData(details):

    print(cv2.__version__)

    # load pretrainted dataset from file
    faceDetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    dataset = os.path.join(IMG_ROOT)
    print("Dataset path : " + dataset)

    rollnumber = details['rollnumber']
    shift = details['shift']
    year = details['year']

    subdata = os.path.join(dataset, year, shift, rollnumber)
    print("subdata path : " + subdata)

    path = os.path.join(dataset, subdata)
    print(path)

    if not os.path.isdir(path):
        os.mkdir(path)

    # img sample size
    (width, height) = (130, 100)

    # camture images from the webcam and process and detect the face
    # takes video capture id, for webcam most of the time its 0.
    cam = cv2.VideoCapture(0)

    # Our identifier
    # We will put the id here and we will store the id with a face, so that later we can identify whose face it is
    # Our dataset naming counter
    sampleNum = 0
    # Capturing the faces one by one and detect the faces and showing it on the window
    while(True):
        # Capturing the image
        # cam.read will return the status variable and the captured colored image
        ret, img = cam.read()
        # the returned img is a colored image but for the classifier to work we need a greyscale image
        # to convert
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # To store the faces
        # This will detect all the images in the current frame, and it will return the coordinates of the faces
        # Takes in image and some other parameter for accurate result
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        # In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
        for(x, y, w, h) in faces:
            # Whenever the program captures the face, we will write that is a folder
            # Before capturing the face, we need to tell the script whose face it is
            # For that we will need an identifier, here we call it id
            # So now we captured a face, we need to write it in a file
            sampleNum = sampleNum+1
            # Saving the image dataset, but only the face part, cropping the rest
            img_name = path + str(sampleNum) + '.png'
            cv2.imwrite(img_name, gray[y:y+h, x:x+w])
            # @params the initial point of the rectangle will be x,y and
            # @params end point will be x+width and y+height
            # @params along with color of the rectangle
            # @params thickness of the rectangle
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Before continuing to the next loop, I want to give it a little pause
            # waitKey of 100 millisecond
            cv2.waitKey(250)

        # Showing the image in another window
        # Creates a window with window name "Face" and with the image img
        cv2.imshow("Face", img)
        # Before closing it we need to give a wait command, otherwise the open cv wont work
        # @params with the millisecond of delay 1
        cv2.waitKey(1)
        # To get out of the loop
        if(sampleNum > 20):
            break
    # releasing the cam
    cam.release()
    # destroying all the windows
    cv2.destroyAllWindows()

    return True


def takeAttendance():

    # Access details ( year, shift ) to access folder from base directory
    # use those details to append dir path to IMG_ROOT

    datasets = os.path.join(IMG_ROOT)
    # Creating a cascade image classifier
    faceDetect = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # Traverse through the dataset
    (images, lables, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(datasets, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                lable = id
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1
            print(path)
    # train model to recognize faces
    (images, lables) = [numpy.array(lis) for lis in [images, lables]]
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, lables)
    # camture images from the webcam and process and detect the face
    # takes video capture id, for webcam most of the time its 0.
    cam = cv2.VideoCapture(0)
    # Our identifier
    # We will put the id here and we will store the id with a face, so that later we can identify whose face it is
    # Our dataset naming counter
    sampleNum = 0
    # Capturing the faces one by one and detect the faces and showing it on the window
    while(True):
        # Capturing the image
        # cam.read will return the status variable and the captured colored image
        ret, img = cam.read()
        # the returned img is a colored image but for the classifier to work we need a greyscale image
        # to convert
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # To store the faces
        # This will detect all the images in the current frame, and it will return the coordinates of the faces
        # Takes in image and some other parameter for accurate result
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        # In above 'faces' variable there can be multiple faces so we have to get each and every face and draw a rectangle around it.
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (80, 130))
            # Recognizing face here
            prediction = model.predict(face_resize)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            if prediction[1] < 500:
                cv2.putText(img, '% s - %.0f' % (names[prediction[0]], prediction[1]),
                            (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            else:
                cv2.putText(img, 'not recognized', (x-10, y-10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        cv2.imshow('OpenCV', img)
        key = cv2.waitKey(10)
        if key == 27:
            break
    cv2.destroyAllWindows()
