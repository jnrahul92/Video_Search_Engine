# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 20:37:44 2022

@author: jnrah
"""
import cv2
import numpy as np
import os
import io
import nltk
import pickle
import speech_recognition as sr 
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from google.cloud import vision
from google.cloud.vision_v1 import types
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')

#Credentials for google vision api
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "your_google_vision_credentials.json"

#Directories for storing data
data_dir = r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\Data/"
ocr_dir = r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\OCR Data\\"
thumbnail_dir = r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\Thumbnails\\"
transcription_dir = r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\Transcription\\"
sound_dir = r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\SoundData\\"
transcription_dir = r"D:\M Tech DSE Bits\Semester 3\Information Retrieval\Assignments\Assignment 2\Transcription\\"

#Initiate Google Vision Image Annotation API
client = vision.ImageAnnotatorClient()

def detect_text(path):
    """
    Detect text using Google vision API
    """
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content = content)
    response = client.text_detection(image = image)
    texts = response.text_annotations
    string = ""
    for text in texts:
        string += " "+text.description
    return string

def ocr_data():
    """
    OCR Video files using Google Vision and OpenCV. 
    Open CV captures frames by frames from videos and then using google vision API
    OCR the image.
    """
    for fname in os.listdir(data_dir):
        result = ""
        cap = cv2.VideoCapture("Data/" + fname)
        i = 0
        while True:
            try:
                ret, frame = cap.read()
                file = "live.png"
                cv2.imwrite(file, frame)
                "Get thumbnail image from the video"
                if i == 20:
                    cv2.imwrite(thumbnail_dir+fname[:-3]+"png", frame)
                "Only OCR image after every 20 frames"
                if i%20 == 0:
                    temp = detect_text(file)
                    result += temp
                i += 1
            except:
                break
        with open(ocr_dir+fname+".txt",'w',encoding='utf-8') as file:
            file.write(result,)
            file.close()
        cv2.destroyAllWindows()
    return

def transcription():
    """Creates transcription from video files after converting them to sound files"""
    for f in os.listdir(data_dir):
        clip = mp.VideoFileClip(f)
        clip.audio.write_audiofile(sound_dir+f[:-3]+"wav")
        r = sr.Recognizer()
        audio = sr.AudioFile(sound_dir+f[:-3]+"wav")
        with audio as source:
            audio_file = r.record(source)
            result = r.recognize_google(audio_file)
        with open(transcription_dir+f[:-3]+"txt","w") as file:
            file.write(result)
            file.close()

def indexing():
    """Create indexing out of OCR'ed data and transcription derived from the videos"""
    stopwords = nltk.corpus.stopwords.words("english")
    tokenizer = RegexpTokenizer(r'\w+')
    vocab_dict = {}
    for file in os.listdir(ocr_dir):
        with open(ocr_dir + file, encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
        with open(transcription_dir + file, encoding="utf-8") as f:
            lines2 = f.readlines()
            lines.extend(lines2)
            f.close()
    lines = " ".join(lines)
    tokens = tokenizer.tokenize(lines)
    tokens = [w for w in tokens if w not in stopwords]
    tokens = list(set(tokens))
    for t in tokens:
        try:
            vocab_dict[t.lower()].extend([file])
        except:
            vocab_dict[t.lower()] = [file]
    with open("index.pkl", "wb") as f:
        pickle.dump(vocab_dict, f)
    
if __name__ == "__main__":
    ocr_data()
    transcription()
    indexing()
    print("Video indexing done.")