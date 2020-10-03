import speech_recognition as sr


r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    while True:
        print("listening")
        audio = r.listen(source)

        try:
            print("Davey thinks you said" + " " + r.recognize_sphinx(audio))
        except:
            print("I couldnt quite catch that!!")

        if str(r.recognize_sphinx(audio)) == "Alpha":
            print ("a")

        elif str(r.recognize_sphinx(audio)) == "Bravo":
            print ("b")

        elif str(r.recognize_sphinx(audio)) == "Charlie":
            print ("c")

        elif str(r.recognize_sphinx(audio)) == "Delta":
            print ("d")

        elif str(r.recognize_sphinx(audio)) == "Echo":
            print ("e")

        elif str(r.recognize_sphinx(audio)) == "Foxtrot":
            print ("f")

        elif str(r.recognize_sphinx(audio)) == "Golf":
            print ("g")

        elif str(r.recognize_sphinx(audio)) == "Hotel":
            print ("h")

        elif str(r.recognize_sphinx(audio)) == "India":
            print ("i")

        elif str(r.recognize_sphinx(audio)) == "Juliet":
            print ("j")

        elif str(r.recognize_sphinx(audio)) == "Kilo":
            print ("k")

        elif str(r.recognize_sphinx(audio)) == "Lima":
            print ("l")

        elif str(r.recognize_sphinx(audio)) == "Mike":
            print ("m")

        elif str(r.recognize_sphinx(audio)) == "November":
            print ("n")

        elif str(r.recognize_sphinx(audio)) == "Oscar":
            print ("o")

        elif str(r.recognize_sphinx(audio)) == "Papa":
            print ("p")

        elif str(r.recognize_sphinx(audio)) == "Quebec":
            print ("q")

        elif str(r.recognize_sphinx(audio)) == "Romeo":
            print ("r")

        elif str(r.recognize_sphinx(audio)) == "Sierra":
            print ("s")

        elif str(r.recognize_sphinx(audio)) == "Tango":
            print ("t")

        elif str(r.recognize_sphinx(audio)) == "Uniform":
            print ("u")

        elif str(r.recognize_sphinx(audio)) == "Victor":
            print ("v")

        elif str(r.recognize_sphinx(audio)) == "Whiskey":
            print ("w")

        elif str(r.recognize_sphinx(audio)) == "X-ray":
            print ("x")

        elif str(r.recognize_sphinx(audio)) == "Yankee":
            print ("y")

        elif str(r.recognize_sphinx(audio)) == "Zulu":
            print ("z")

        elif str(r.recognize_sphinx(audio)) == "space":
            print ("spacebar")

        elif str(r.recognize_sphinx(audio)) == "back":
            print ("backspace")




                # comments if needed:

                # lastWord = r.recognize_sphinx(audio)
                # print("Davey thinks you said" + " " + lastWord)
                # if lastWord = "alpha"
                    # print ("a")

                # switcher = {
                #             0: Alpha,
                #             1: Bravo,
                #             2: Charlie,
                #             3: Delta,
                #             4: Echo
                #         }
