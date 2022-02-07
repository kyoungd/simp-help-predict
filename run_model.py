# AI Class Project: CSUF Portal Bot
# Peter Bergeon, Brian Edwards, Ryan Romero

# ----- Libraries -----
import random
import json
import pickle
import numpy as np
import requests
import os
from tensorflow.keras.models import load_model

# ----- Setup -----

with open("intents.json") as file:
    data = json.load(file)

words = pickle.load(open("words.pkl", "rb"))
topics = pickle.load(open("topics.pkl", "rb"))
model = load_model("chatbot_Model.h5")

def bag_of_words(userString):
    # HTTP post request to the server
    hostUtil = os.environ.get(
        'HOST_UTIL', 'https://simp-help-util.herokuapp.com/bag_of_words')
    headers = {'Content-Type': 'application/json'}
    jdata = {'question': userString}
    r = requests.post(hostUtil, headers=headers, data=json.dumps(jdata))
    if (r.status_code == 200):
        return np.array(json.loads(r.json()['data']))
    return np.array([])

# chatBot:
#       Gives a user's string a percentage value for each topic in json file
#       we will check to see if percentage chance is greater then 75%
#       if so, we will assume the question is that of the json topic and respond
#       if below 75%, bot will print out a "I dont understand" message


def chatBot(userString):
    try:
        currentBag = bag_of_words(userString)
        result = model.predict(np.array([currentBag]))[0]
        # print("Result: ", result, "\n")

        # get the highest numerical value prediction
        result_index = np.argmax(result)
        # print("Highest Result Index: ", result_index, "\n")

        # get the topic associated to the highest numerical value prediction
        topic = topics[result_index]

        # IF: percentage is greater then 75%
        if result[result_index] > 0.80:
            # we grab the list of responds and choose one at random
            for tg in data["intents"]:
                if tg["tag"] == topic:
                    responses = tg['responses']
            return (random.choice(responses))

        # ELSE: we print out a confused bot response
        else:
            return ("Sorry, I didn' understand. Try asking again.")
    except Exception as e:
        outmsg = str(e)
        return (outmsg)

if __name__ == "__main__":
    # ----- Main -----
    while True:
        print("-------------------------------------------------------------------")
        userString = input("You: ")
        print(" ")
        chatBot(userString)
