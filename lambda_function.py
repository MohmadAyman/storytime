# -*- coding: utf-8 -*-

import logging
from ask_sdk.standard import StandardSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream)

import random
# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
print('working')
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
#import tensorflow as tf

from ask_sdk_model import Response
from alexa import data, util


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


import requests

url = 'http://ec2-3-64-130-6.eu-central-1.compute.amazonaws.com:8080/analyze'


paragraph1 = "I’d named him Rufus. Cute right? Rufus wasn’t mine but then does a cat really belong to anybody? They’re free spirits. I believe they choose their people, and Rufus chose me.\
Rufus came at just the right time. Not long after mine and Tony’s arguments got too much. After the trouble happened, the sirens and after he got in the back of that car and left.\
Just as I was staring at the bottle of pills on the kitchen side and wondering how much longer I could go on for.\
If Tony couldn’t live with me then how could I live with myself?\
Meow."


paragraph2 = "She didn’t die on impact but we knew she was done for, Tony said she couldn’t be saved. That’s why we drove away. Better to preserve two lives than ruin three trying to save one.\
That’s what he said. I listened. I looked at her, gasping for air on the floor and I saw my own ruined life. I hate myself for it, I really do. But I didn’t see her for a second.\
That’s why we pushed her into the grassy embankment and left her there to die.\
The police found the body the next day, already being picked apart by animals at the roadside. I may have killed her but getting caught was Tony’s fault. He was the one that dropped his wallet.\
This was his fault!"



### Those should be joyful

paragraph3 = "In the spring, Nicholas picks flowers and chases butterflies, and in the summer, watches the frogs in the pond. In the autumn, he sees the animals preparing for the winter. When winter comes, Nicholas watches the snow falling from the sky, then curls up in his hollow tree and dreams about spring. In print for well over 50 years, this beautifully illustrated, gentle story has been a favorite Golden Book for generations."


paragraph4 = "One bright sunny day, a prince arrives at her palace, meets her and eventually, they fell in love. One night, the prince takes the princess to a shady grassland at the edge of the woods. He says if the princess truly loves him, she must pick a rare flower called the scarlet rose for him. She tries hard to find the flower as she wants to prove her love for the prince. Finally, she finds the scarlet rose. But as soon as the princess touches the flower, she falls asleep."


stories = [paragraph1, paragraph2, paragraph3, paragraph4]


# Takes a string and returns one of the six emotions as a string
# Examples:
# get_emotion("i feel as if i havent blogged in ages are at least truly blogged i am doing an update cute") # Output: 'joy'
# get_emotion("i have a feeling i kinda lost my best friend") # Output: 'sadness'

def get_emotion(text):
    myobj = {'text': text}
    print('before request')
    x = requests.post(url, data = myobj)
    print('request sent')
    print(x.text)
    # return "joy"
    return x.text


# Returns the most common element (mode) in a list
def most_common(lst):
    return max(set(lst), key=lst.count)

# Partitions a list into n chunks of equal size, except for the last chunk being at most n-1 larger due to the remainder.
def partition(list, n):
  k = len(list) // n
  rem = len(list) % n > 0 

  chunks = [list[x:x+k] for x in range(0, len(list), k)]
  
  if rem:
    last = chunks.pop()
    chunks[n-1] += last
    
  return chunks


# Returns the story and its corresponding sub-stories emotions
# def set_the_scene(story_file, story_partitions=3):
#     with open(story_file, 'r') as f:
#         story = f.readlines()

#     story = [line for line in story if not line == "\n"]
#     story = "".join(story) # The whole story in one string

#     sentences = sent_tokenize(story)

#     sub_stories = partition(sentences, story_partitions)
#     blocks = [" ".join(sub_story) for sub_story in sub_stories]

#     emotions = [get_emotion(block) for block in blocks]

#     return story, emotions


# Should fetch a story text file name
def fetch_random_story():
    # story_files = os.listdir()

    # return random.choice(story_files)
    return random.choice(stories)

# takes a list of emotions represented as strings, and plays the audio files in subsequent order corresponding to the emotions
def play_audio(emotions):
    pass

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        print('here')
        print(type(handler_input))
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # speak_output = "Welcome, you can say Hello or Help or Story or anything. Which would you like to try?"
        print('here 2')

        speak_output = "We will find a random story for you.\n\n"

        # story, emotions = set_the_scene(fetch_random_story())

        story = fetch_random_story()
        print(story)
        # story = ""
        emotion = get_emotion(story)
        print(emotion)
        speak_output += "###Play a \"{}\" track### \n\n".format(emotion)
        print('before last speak')
        speak_output += story
        speak_output += "\n"

        # play_audio(emotions) # Somehow run this in parallel to the audio of the story
        print('here 3')

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# class LaunchRequestHandler(AbstractRequestHandler):
#     """Handler for Skill Launch."""
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool

#         return ask_utils.is_request_type("LaunchRequest")(handler_input)

#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         speak_output = "Welcome, you can say Hello or Help or Story or anything. Which would you like to try?"

#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
