import os
import pickle
from os import getcwd
from PIL import Image
import dlib
import cv2
import subprocess
import numpy as np


# Download face detector and recognition mode if necessary and load into variables
if not os.path.exists('shape_predictor_68_face_landmarks.dat'):
    subprocess.run(['wget', 'https://github.com/davisking/dlib-models/raw/master/shape_predictor_68_face_landmarks.dat.bz2', '-O', 'shape_predictor_68_face_landmarks.dat.bz2'])
    subprocess.run(['bzip2', '-d', 'shape_predictor_68_face_landmarks.dat.bz2'])
if not os.path.exists('dlib_face_recognition_resnet_model_v1.dat'):
    subprocess.run(['wget', 'https://github.com/davisking/dlib-models/raw/master/dlib_face_recognition_resnet_model_v1.dat.bz2', '-O', 'dlib_face_recognition_resnet_model_v1.dat.bz2'])
    subprocess.run(['bzip2', '-d', 'dlib_face_recognition_resnet_model_v1.dat.bz2'])

faceDetector = dlib.get_frontal_face_detector()
shapePredictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
faceRecognizer = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

# Download faces dataset if necessary
faceDatasetFolder = 'celeb_mini'

if not os.path.exists(faceDatasetFolder):
    subprocess.run(['wget', 'https://www.dropbox.com/s/lulw2jwsblz687g/celeb_mini.zip?dl=1', '-O', 'celeb_mini.zip'])
    subprocess.run(['unzip', 'celeb_mini.zip'])
if not os.path.exists('celeb_mapping.npy'):
    subprocess.run(['wget', 'https://www.dropbox.com/s/m7kjjoa1z1hsxw6/celeb_mapping.npy?dl=1', '-O', 'celeb_mapping.npy'])
if not os.path.exists('test-images'):
    subprocess.run(['wget', 'https://www.dropbox.com/s/3yi89blp4lhiw6y/test-images.zip?dl=1', '-O', 'test-images.zip'])
    subprocess.run(['unzip', 'test-images.zip'])

# Label -> Name Mapping file
labelMap = np.load("celeb_mapping.npy", allow_pickle=True).item()


def face2vec(image):
    # detect faces in image
    faces = faceDetector(image)
    vecs = []

    # Now process each face we found
    for k, face in enumerate(faces):
        # Find facial landmarks for each detected face
        shape = shapePredictor(image, face)

        # Compute face descriptor using neural network defined in Dlib.
        # It is a 128D vector that describes the face in img identified by shape.
        faceDescriptor = faceRecognizer.compute_face_descriptor(image, shape)

        # Convert face descriptor from Dlib's format to list, then a NumPy array
        faceDescriptorList = [x for x in faceDescriptor]
        faceDescriptorNdarray = np.asarray(faceDescriptorList, dtype=np.float64)
        faceDescriptorNdarray = faceDescriptorNdarray[np.newaxis, :]

        vecs.append(faceDescriptorNdarray)

    return vecs


# If necessary, compute face descriptors for faces dataset and link them to a celebrity. Later used to compare uploaded
# image against
descriptors_file = 'faceDescriptors.npy'
index_file = 'index.pkl'
if not os.path.exists(descriptors_file) or not os.path.exists(index_file):
    faceDescriptors = None
    index = {}
    i = 0

    celeb_list = os.listdir(faceDatasetFolder)
    for celeb_nb, celeb in enumerate(celeb_list):
        celeb_path = os.path.join(faceDatasetFolder, celeb)

        print("processing celeb {}/{}".format(celeb_nb, len(celeb_list)), end='\r')

        for image_path in os.listdir(celeb_path):
                    # read image and convert it to RGB
            image_path = os.path.join(celeb_path, image_path)
            img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

            descriptors = face2vec(img)

            for faceDescriptorNdarray in descriptors:
                # Stack face descriptors (1x128) for each face in images, as rows
                if faceDescriptors is None:
                  faceDescriptors = faceDescriptorNdarray
                else:
                  faceDescriptors = np.concatenate((faceDescriptors, faceDescriptorNdarray), axis=0)

                # save the label for this face in index. We will use it later to identify
                # person name corresponding to face descriptors stored in NumPy Array
                index[i] = {'name': labelMap[celeb], 'image_path': image_path}
                i += 1
    print()

    np.save(descriptors_file, faceDescriptors, allow_pickle=True)
    with open(index_file, 'wb') as f:
        pickle.dump(index, f)
else:
    faceDescriptors = np.load(descriptors_file, allow_pickle=True)
    with open(index_file, 'rb') as f:
        index = pickle.load(f)


def supported_image_type(img):
    try:
        image = Image.open(img)
        return image.mode == 'RGB'
    except:
        return False


# Find most similar celebrity
def predict(image_file):
    try:
        im = cv2.imread(image_file)
        imDlib = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

        # Convert test image to embedding/vector
        faceDescriptorNdarray = face2vec(imDlib)[0]

        # Calculate Euclidean distances between face descriptor calculated on face detected
        # in current frame with all the face descriptors we calculated while enrolling faces
        distances = np.linalg.norm(faceDescriptors - faceDescriptorNdarray, axis=1)

        # Calculate minimum distance and index of this face
        argmin = np.argmin(distances)  # index
        minDistance = distances[argmin]  # minimum distance
        print('min distance:', minDistance)

        celeb_name = index[argmin]['name']

        return [celeb_name]
    except:
        print(f"Something went wrong with the model. May be image format is not supported")
        return []

#testing
def test():
    img = '/tmp/dog.jpg'
    cf = '/tmp/imagenet_class_index.json'

    p = predict(img, cf)
    print(f'Given image is: {p[1]}')

