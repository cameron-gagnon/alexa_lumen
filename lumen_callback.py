#!/usr/bin/env python2.7
import logging
import requests

from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, request, session, version

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

PORT=80
URL="http://127.0.0.1:" + str(PORT) + "/signal/"

# used to translate the state from the skill to the opcode used in the program
lookup = {
    "maize and blue": "mandb",
    "rainbow": "gerald",
}


@ask.intent("ListStates")
def list_states():
    msg = render_template("listStates")
    return statement(msg)


@ask.intent("ControlLights")
def control_lights(state):
    logging.debug("Triggering state: ")
    logging.debug(state)
    opcode = lookup.get(state, state)
    if opcode is not None:
        requests.get(URL + opcode)
    else:
        logging.error("Unknown opcode")
        logging.error(opcode)
        return statement("That is not a valid setting, or something went wrong")

    return statement("")


while True:
    try:
        app.run(debug=True)
        while True:
            pass
    except Exception as e:
        logging.error("An error occurred: {}\n{}".format(e.errno, e.strerror))
