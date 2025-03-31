"""
Submission for
Exercise task 11
of UTU course TKO_8964_3006
Textual Data Analysis
by Botond Ortutay

---

Instructions:

Building a basic chatbot

In this exercise, you will build a minimal chatbot using the transformers 
library and a pretrained model.

First, if you haven't done so already, study the Using [LLMs with transformers 
notebook](https://github.com/TurkuNLP/textual-data-analysis-course/blob/main/llms_using_transformers_library.ipynb). 
That should give you all the necessary prerequisites for completing this 
exercise.

Using what you learned from that notebook, write a python script that takes 
input from a user, passes that to an LLM, and prints out the LLM response, 
repeating until the user requests to exit while <u>keeping track of the 
message history</u>. You can use this template as a starting point

```python
[YOUR CODE HERE: load model]

messages = []
while True:
    user_input = input('Say something ("exit" to quit): ')
    if user_input == 'exit':
        break
    messages.append({'role': 'user', 'content': user_input})
    [YOUR CODE HERE:  call model, print its output, and add it to messages]
```

(You may want to tweak generation parameters and add additional features like 
having the text "reset" reset the message queue to make testing easier.)

You can use e.g. one of the following models:

 - HuggingFaceTB/SmolLM2-135M-Instruct
 - HuggingFaceTB/SmolLM2-360M-Instruct
 - HuggingFaceTB/SmolLM2-1.7B-Instruct

(For best results, use the largest model with GPU acceleration. If you're 
running on a GPU with more memory, you can of course use even larger models, 
just pick an appropriate one from https://huggingface.co/models.)

Test your chatbot with the following and provide logs of your discussions:

 1. At least 5 questions about basic facts about the world (e.g. the capital 
    of a country)
 2. At least 5 arithmetic questions ranging from trivial ("what is 1+1?") to 
    more complex
 3. Inform the system of a secret word (e.g. "zebra"), then after a few other 
    questions ask it what the secret word is. Make sure you understand where 
    the memory of that secret word is.

In very brief, what did you think about the capabilities of the chatbot you 
created? Of the factors impacting LLM performance that we discussed on the 
lecture, which one (or ones) do you think are primarily limiting its 
performance?
"""

### IMPORTING LIBRARIES ###
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

### DEFINING FUNCTIONS ###
def printHelp(SAVEFILE):
	print("This software supports the following commands:")
	print("\"exit\":\t\tQuit the software")
	print("\"help\":\t\tPrint this message")
	print("\"logs\":\t\tSave logs to " + SAVEFILE)
	print("\"reset\":\tErase message history")
	print("")
	print("All other messages will be treated as input for the chatbot")
	print("")

"""
Function for saving message logs into separate file
In:
SAVEFILE	str						name of the file we save into (will create new file if suitable file doesn't exist)
messages	list of dict: {"role": str, "content": str}
"role"		"user" or "system"
Out:
---
Note:
We output a .tex file that should be used as an \input{} in another file for 
reporting. The tex file output uses the xcolor LaTeX package.
"""
def saveLogs(SAVEFILE, messages):
	print("Saving message logs in: " + SAVEFILE)
	f = open(SAVEFILE, "w")
	for message in messages:
		if (message["role"] == "user"):
			f.write("\\textcolor{blue}{\\textbf{" + message["content"] + "}}")
		else:
			f.write(message["content"])
		f.write("\\\\")
	f.close()

### GLOBAL VARIABLES AND CONSTANTS ###
device = "cuda"	# Use GPU by default
MODEL = "HuggingFaceTB/SmolLM2-360M-Instruct"
SAVEFILE = "ext_11_logs.tex"

### WELCOME MESSAGE ###
print("")
print("Welcome to my beautiful chatbot!")
if (torch.cuda.is_available()):
	print("Running on GPU with CUDA support!")
else:
	print("WARNING: GPU with CUDA support NOT FOUND. Falling back to CPU")
	device = "cpu"
print("")
printHelp(SAVEFILE)

### LOADING MODEL ###
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL).to(device)
print ("Loaded model: " + MODEL)
print("")

### EXERCISE TEMPLATE BELOW ###
messages = []
while True:
	user_input = input("$ ")
	if user_input == 'exit':
		break
	elif user_input == "help":
		printHelp(SAVEFILE)
	elif user_input == "logs":
		saveLogs(SAVEFILE, messages)
	elif user_input == "reset":
		messages = []
	else:
		messages.append({'role': 'user', 'content': user_input})

		### CALL MODEL, PRINT ITS OUTPUT AND ADD IT TO MESSAGES ###
		# tokenizing chat so that it can be used as an input for the LLM
		tokenized_chat = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(device)
		# using model to generate text
		outputs = model.generate(tokenized_chat, max_new_tokens=128)
		# decoding (tokens -> text) output
		textOut = tokenizer.decode(outputs[0])
		# removing all previous context from textOut
		textOut = textOut[textOut.rfind("<|im_start|>assistant")+len("<|im_start|>assistant"):textOut.rfind("<|im_end|>")]
		print(textOut)
		print("")

		messages.append({'role': 'system', 'content': textOut})
