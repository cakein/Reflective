from analysis import analyze_image, encode_image
from feedback import feedback
from toneDetector import detect_tone, toneHandler
from convertLog import writeLog
import queue, threading, time

toneListener = toneHandler()
run = True

if __name__ == "__main__":

    toneThread = threading.Thread(target=detect_tone, args=(toneListener,))
    toneThread.start()

    while run:
        print(" ")
        audienceQ = queue.Queue()
        audienceThread = threading.Thread(target=analyze_image, args=(audienceQ, "audience", encode_image("audience.png"),encode_image("speaker.png")))
        audienceThread.start()

        faceQ = queue.Queue()
        faceThread = threading.Thread(target=analyze_image, args=(faceQ, "face", encode_image("speaker.png")))
        faceThread.start()

        cameraQ = queue.Queue()
        cameraThread = threading.Thread(target=analyze_image, args=(cameraQ, "camera", encode_image("speaker.png")))
        cameraThread.start()

        writeLog("./logs/tone.log", "The last tones of the speaker were: " + str(toneListener.getTone()) + " and their corresponding polarity scores are: " + str(toneListener.getSentiment()))

        audienceThread.join()
        faceThread.join()
        cameraThread.join()

        overallQ = queue.Queue()
        overallThread = threading.Thread(target=feedback, args=(overallQ, 'overall'))
        overallThread.start()

        environmentQ = queue.Queue()
        environmentThread = threading.Thread(target=feedback, args=(environmentQ, 'environment'))
        environmentThread.start()

        engagementQ = queue.Queue()
        engagementThread = threading.Thread(target=feedback, args=(engagementQ, 'engagement'))
        engagementThread.start()

        toneQ = queue.Queue()
        toneThread = threading.Thread(target=feedback, args=(toneQ, 'tone'))
        toneThread.start()

        impressionQ = queue.Queue()
        impressionThread = threading.Thread(target=feedback, args=(impressionQ, 'impression'))
        impressionThread.start()

        summaryQ = queue.Queue()
        summaryThread = threading.Thread(target=feedback, args=(summaryQ, 'summary'))
        summaryThread.start()

        overallThread.join()
        environmentThread.join()
        engagementThread.join()
        toneThread.join()
        impressionThread.join()
        summaryThread.join()

        time.sleep(1)