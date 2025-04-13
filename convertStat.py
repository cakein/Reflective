from pathlib import Path
from convertLog import readLogs, writeLog
import queue, threading 
from openai import OpenAI

client = OpenAI(
    # Terrible practice, will be requested later via server (PROTOTYPE)
    api_key="<key>"
)

def generateStat(file, location):
    print(str(file) + " thread created!")
    feedback = readLogs([file,])
    stResponse = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will be provided with a filepath to a log file, its previously interpretted rating, the name of the log file corresponds with its contents, the contents (a sentence or two), provide feedback on a video conference. Provide an integer 0-100 on how it rates from 0 being highly negatively critized / negative tones etc. to 100 being positive feedback, positive tones etc. (YOUR ENTIRE OUTPUT NEEDS TO ALWAYS BE 3 OR LESS INTEGERS AS THIS WILL BE PARSED LATER!!!)"},
                {"role": "user", "content": feedback + " \n\nFILEPATH: " + str(file) + "\n\n\OLD RATING: " + readLogs([location,])}
            ]
        )
    ret = stResponse.choices[0].message.content
    if not ret.isdigit():
        ret = 50
    print(str(file) + ": " + ret)
    writeLog(location, str(ret))
    return

def convertStat():
    feedback = Path('./output/feedback')
    stats = Path('./output/stats')

    threads = []
    for i in feedback.iterdir():
        t = threading.Thread(target=generateStat, args=("./output/feedback/"+i.name,"./output/stats/"+i.name))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

    print("done!")

convertStat()