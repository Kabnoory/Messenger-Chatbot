# Messenger-Chatbot

Facebook Messenger Chatbot that I trained to talk like me!
For this project, I wanted to train a RNN Sequence To Sequence model (using LSTM units) on my past conversation logs from Facebook messenger chats. I'll be using Tensorflow for this project!

Training the model took much more than I expected so I had to use AWS cloud computing platform, to be able to use a powerful NVIDIA gpu and install CUDA. I trained my model for 100,000 iterations which took about 10 hours.

#### How I got the data?
Facebook provides a file with all of my messages in an .htm format. I'm going to need to parse through this large file, and extract all of the conversations. To do this, I'll use this tool that Dillon Dixon has kindly open sourced. 
    
    pip install fbchat-archive-parser
    
which gives me a .txt file. I'll modify this .txt file using my script getFacebookData.py to create my dataset that will be used in training. Then, I'll create my training matrices using my script training.py, then finally use Tensorflow to train my model in the notebook.


#### Future Improvements:
- Increase number of iterations, since I currently don't have enough computation power or resources to run more iterations fast.
- Adding more data from other social media applications like Whatsapp.


#### Notes:
English is not my first language, so some of the bot responses are not in English and won't be understood by people who speak different languages than I do.
