def writeLog(file, text):
    text = text.replace('\n', '')
    with open(file, 'w', encoding='utf-8') as log:
        log.write(text)

def readLogs(files):
    ret = ""
    for file in files:
        with open(file, 'r', encoding='utf-8') as log:
            ret = ret + "\n" + log.readline().strip()
    return ret