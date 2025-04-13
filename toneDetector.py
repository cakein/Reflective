import speech_recognition as sr
from textblob import TextBlob
import time

class toneHandler:
    def __init__(self):
        self.stopper = False
        self.tone = ['Not Detected',]
        self.sentiment = [0,] 
    
    def updateTone(self, string, score):
        self.tone.append(string)
        if len(self.tone) > 5:
            self.tone.pop(0)
        self.sentiment.append(score)
        if len(self.sentiment) > 5:
            self.sentiment.pop(0)

    def getTone(self):
        return self.tone

    def getSentiment(self):
        return self.sentiment
    
    def stop(self):
        self.stopper = True
    
    def isRunning(self):
        return False if self.stopper is True else True

def detect_tone(toneHandler):
    notExecuted = False
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        time.sleep(1)

    try:
        text = r.recognize_google(audio)
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity

        if sentiment_score > 0:
            tone = "Positive"
        elif sentiment_score < 0:
            tone = "Negative"
        else:
            tone = "Not Detected"
            notExecuted = True
        if notExecuted == False:
            toneHandler.updateTone(tone, sentiment_score)
        notExecuted = False
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(e)
    if toneHandler.isRunning():
        detect_tone(toneHandler)
    else:
        print('Stopped ToneDetector')
    