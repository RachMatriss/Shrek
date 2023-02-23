import openai
import sys

# Set up the OpenAI API client
openai.api_key = "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"

# Set up the model and prompt
model_engine = "text-davinci-003"

print("[+] i'm Shrek boot, i use AI to reaply your Qs ...")
print("[+] To close the program, input [close] or [Q] \n")
while (1):
    prompt = input("Please ask me >>>: ")
    if prompt:
        if prompt=="close" or prompt=="Q" or prompt=="q":
            print("\n [+] Thank you for your time /\/ bye ...")
            sys.exit()
        # Generate a response
        completion = openai.Completion.create(
   	        engine=model_engine,
	    	prompt=prompt,
    		max_tokens=1024,
	    	n=1,
	    	stop=None,
	    	temperature=0.5,
	    	)

        response = completion.choices[0].text
        print("\n ",response)
        print("\n#...\n#...\n#...\n ================================ \n")
    
