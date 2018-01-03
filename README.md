# Messenger-Chatbot

Facebook Messenger Chatbot that I trained to talk like me!

For this project, I wanted to train a Sequence To Sequence model on my past conversation logs from Facebook messenger chats. I won't be doing it in jupyter to keep my messages data secure

## Steps:
Get the Data: Facebook provides a file with all of my messages in an .htm format. I'm going to need to parse through this large file, and extract all of the conversations. To do this, I'll use this tool that Dillon Dixon has kindly open sourced. 
    
    pip install fbchat-archive-parser
    

Read Data: I'll read the Data using .py
