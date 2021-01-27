from transformers import AutoTokenizer, AutoModelWithLMHead
import nltk

model_path = "classifier"

# Downloads and saves the models
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion", use_fast=False)
model = AutoModelWithLMHead.from_pretrained(model_path)

nltk.download('punkt')
from nltk.tokenize import sent_tokenize 


# Takes a string and returns one of the six emotions as a string
# Examples:
# get_emotion("i feel as if i havent blogged in ages are at least truly blogged i am doing an update cute") # Output: 'joy'
# get_emotion("i have a feeling i kinda lost my best friend") # Output: 'sadness'

def get_emotion(text):
  input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

  output = model.generate(input_ids=input_ids,
               max_length=2)

  dec = [tokenizer.decode(ids) for ids in output]
  label = dec[0]
  # print(dec)
  return label[6:]


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



def set_the_scene(story_file, story_partitions=3):
    with open(story_file, 'r') as f:
        story = f.readlines()

    story = [line for line in story if not line == "\n"]
    story = "".join(story) # The whole story in one string

    sentences = sent_tokenize(story)

    sub_stories = partition(sentences, story_partitions)
    blocks = [" ".join(sub_story) for sub_story in sub_stories]

    emotions = [get_emotion(block) for block in blocks]
