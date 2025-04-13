import base64
from openai import OpenAI
from convertLog import writeLog

client = OpenAI(
    # Terrible practice, will be requested later via server (PROTOTYPE)
    api_key="<key>"
  )

def encode_image(image):
  with open(image, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_image(queue, type, speaker=False, audience=False):
  if type == 'camera':
    train = "Give a 1-10 rating on each of the following categories for the image: Lighting Quality, Camera Framing/Positioning, Background Professionalism, Facial Visibility, Image Quality"
  elif type == 'face':
    train = "Using the image, give a 1-10 rating for the person's Eye Contact, relay their detected emotion, body language, posture, and clothing"
  elif type == 'audience':
    train = "('audience' means excluding speaker, so don't include any info from speaker's image. Additionally, don't link any of the information to a person, just raw info) Give a line of all the emotions of the audience, a line of each of the audience's distracted (%) and attentive (%), and a line of each of their body language description (posture, pose)"
  if audience == False:
    sResponse = client.chat.completions.create(
      model="gpt-4-turbo-2024-04-09",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": train},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{speaker}"}},
          ]
        }
      ]
    )
    ret = sResponse.choices[0].message.content
    writeLog(f"./logs/{type}.log", ret)
    queue.put(True)
    return
  else:
    aResponse = client.chat.completions.create(
      model="gpt-4-turbo-2024-04-09",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": train},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{audience}"}},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{speaker}"}},
          ]
        }
      ]
    )
    ret = aResponse.choices[0].message.content
    writeLog(f"./logs/{type}.log", ret)
    queue.put(True)
    return