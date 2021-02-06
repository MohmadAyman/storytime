from flask import Flask
from flask import request

from transformers import AutoTokenizer, AutoModelWithLMHead

import json


print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion", use_fast=False)
model = AutoModelWithLMHead.from_pretrained("classifier")
print("model loaded!")

def get_emotion(text):

	input_ids = tokenizer.encode(text + '</s>', return_tensors='pt')

	output = model.generate(input_ids=input_ids, max_length=2)

	dec = [tokenizer.decode(ids) for ids in output]
	label = dec[0]
	return label[6:]

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello from Flask!'


@app.route('/analyze', methods=['POST'])
def test():
	print("inside func")
	data = request.form
	emot = get_emotion(data['text'])
	print("emotion is:", emot)
	result = {"emotion": emot}

	# return json.dumps(result)
	return emot

if __name__ == "__main__":
	app.run(debug=True)
