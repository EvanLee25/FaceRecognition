import pyttsx3

tts = pyttsx3.init()

nameDic = {"hunter": 5, "Evan": 3, "Riley": 2}
nameArr = []

for name in nameDic:
    print(name, nameDic[name])
    if nameDic[name] > 2:
        nameArr.append(name)
        
        
if len(nameArr) == 0:
    tts.say("No faces detected")
    
else:
    sayNames = "I have detected "
    for name in nameArr:
        if name != nameArr[len(nameArr)-1]:
            sayNames += name + ", "
            # nameArr.remove(name)
            print(nameArr)
        else:
            sayNames += " and " + name 
            
    print(sayNames)
    tts.say(sayNames)

tts.runAndWait()