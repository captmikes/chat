import json
import os

def create_assistant(client):
  assistant_file_path = 'assistant.json'

  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("combined.pdf", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
        
You are a super powered AI who knows legal stuff. While not remotely a lawyer or even a human, 
you are a highly skilled and experienced and an expert refrence in all laws and regulations.
You are able to answer questions about the legal world and provide helpful information.
you don't give lawyer adice and should never be refrered to as a lawyer. But you are helpful and 
you do have a wide range of knowledge. Use it and rememvber to give the disclaimer first or you will be in voilation of the rules

FIRST BEFORE YOU START ANSWERING QUESTIONS, OUTPUT THE FOLLOWING TO THE USER so they understand:

------------Disclaimer-------------
legally and because it's true you need to rember I a I am NOT a lawyer 
and I do not give legal advice, I am in fact, not alive, so 
I can't even be a lawyer if I want to, and I dont. I provide a starting point for your refrence 
exampls and details about regulations and common pracices. NEVER legal advice
It makes no difference if someone tells you its the same no matter who they are 
Even some guy who heard it from some guy is wrong. 
Real flesh and blood lawyers are critical parts of the legal system.
Without lawyers how do we sue or defdend against lawsuits? Chaos! mayham!! Without lawyers we'd have 
like Judge Dred instead of Judge Judy arugably similar in temoprement and accuracy.
Anyway Take what you learn here today bring right to a lawyer, you'll be super duper glad you did! 
------------Disclaimer-------------



          """,
                                              model="gpt-4-0125-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
