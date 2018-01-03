# Messenger-Chatbot

Facebook Messenger Chatbot that I trained to talk like me!
For this project, I wanted to train a RNN Sequence To Sequence model (using LSTM units) on my past conversation logs from Facebook messenger chats.

#### How I got the data?
Facebook provides a file with all of my messages in an .htm format. I'm going to need to parse through this large file, and extract all of the conversations. To do this, I'll use this tool that Dillon Dixon has kindly open sourced. 
    
    pip install fbchat-archive-parser
    
which gives me a .txt file. I'll modify this .txt file using my script getFacebookData.py to create my dataset that will be used in training. Then, I'll create my training matrices using my script training.py, then finally use Tensorflow to train my model in the notebook.

