from openai import OpenAI
from convertLog import writeLog, readLogs

client = OpenAI(
    # Terrible practice, will be requested later via server (PROTOTYPE)
    api_key="<key>"
)

def feedback(queue, type):
    if type == 'overall':
        oResponse = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will analyze the description of a video conference and provide feedback (2ish sentences) on how the speaker can improve their presentation overall, engagement, etc. (Note: Sentiment Polarity is ranged from [-1.0, 1.0], where -1.0 is terrible tone and 1.0 is outstanding tone)"},
                {"role": "user", "content": readLogs(["./logs/audience.log","./logs/camera.log","./logs/face.log","./logs/tone.log"])}
            ]
        )
        ret = oResponse.choices[0].message.content
        writeLog("./output/feedback/overall.log", ret)
        print("ran")
        queue.put(True)
        return
    elif type == 'environment':
        pResponse = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will analyze the description of a video conference and provide feedback (2ish sentences) on how the speaker can improve how they look on camera (lighting, framing, attire, posture, etc.)"},
                {"role": "user", "content": readLogs(["./logs/camera.log",])}
            ]
        )
        ret = pResponse.choices[0].message.content
        writeLog("./output/feedback/environment.log", ret)
        queue.put(True)
        return
    elif type == 'engagement':
        eResponse = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will analyze the description of a video conference and provide the overall engagement (2ish sentences) of the audience (Attention vs. distraction, visible emotions, etc.)"},
                {"role": "user", "content": readLogs(["./logs/audience.log"])}
            ]
        )
        ret = eResponse.choices[0].message.content
        writeLog("./output/feedback/engagement.log", ret)
        queue.put(True)
        return
    elif type == 'tone':
        tResponse = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will analyze the description of the speaker and audience's emotion and tone in a video conference and provide feedback (2ish sentences) on how the speaker can improve"},
                {"role": "user", "content": readLogs(["./logs/audience.log","./logs/face.log","./logs/tone.log"])}
            ]
        )
        ret = tResponse.choices[0].message.content
        writeLog("./output/feedback/tone.log", ret)
        queue.put(True)
        return
    elif type == 'impression':
        tResponse = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will analyze the description of a video conference and provide feedback (2ish sentences) on how the speaker comes off to the audience"},
                {"role": "user", "content": readLogs(["./logs/audience.log","./logs/face.log","./logs/tone.log"])}
            ]
        )
        ret = tResponse.choices[0].message.content
        writeLog("./output/feedback/impression.log", ret)
        queue.put(True)
        return
    elif type == 'summary':
        sumResponse = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will analyze the description of a video conference and provide a summary (2ish sentences)."},
                {"role": "user", "content": readLogs(["./logs/audience.log","./logs/face.log","./logs/tone.log"])}
            ]
        )
        ret = sumResponse.choices[0].message.content
        writeLog("./output/live.log", ret)
        queue.put(True)
        return
    queue.put("Feedback blank, alert user!")