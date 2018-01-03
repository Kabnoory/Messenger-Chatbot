import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
from collections import Counter

def read_data(path,facebook_name):
	facebook_dict = dict()
	fb_messages = open(path, 'r') 
	messages_lines = fb_messages.readlines()
	my_message, others_message, current_speaker = "","",""
	for index,lines in enumerate(messages_lines):
	    right_bracket = lines.find(']') + 2
	    just_message = lines[right_bracket:]
	    colon = just_message.find(':')
	    # Find messages that I sent
	    if (just_message[:colon] == facebook_name):
	        if not my_message:
	            # Want to find the first message that I send (if I send multiple in a row)
	            start_message_index = index - 1
	        my_message += just_message[colon+2:]
	        
	    elif my_message:
	        # Now go and see what message the other person sent by looking at previous messages
	        for counter in range(start_message_index, 0, -1):
	            current_msg = messages_lines[counter]
	            right_bracket = current_msg.find(']') + 2
	            just_message = current_msg[right_bracket:]
	            colon = just_message.find(':')
	            if not current_speaker:
	                # The first speaker not named me
	                current_speaker = just_message[:colon]
	            elif (current_speaker != just_message[:colon] and others_message):
	                # A different person started speaking, so now I know that the first person's message is done
	                others_message = clean_message(others_message)
	                my_message = clean_message(my_message)
	                facebook_dict[others_message] = my_message
	                break
	            others_message = just_message[colon+2:] + others_message
	        my_message, others_message, current_speaker = "","",""    
	return facebook_dict


def clean_message(message):
	# Remove new lines within message
	cleaned_message = message.replace('\n',' ').lower()
	# Deal with some weird tokens
	cleaned_message = cleaned_message.replace("\xc2\xa0", "")
	# Remove punctuation
	cleaned_message = re.sub('([.,!?])','', cleaned_message)
	# Remove multiple spaces in message
	cleaned_message = re.sub(' +',' ', cleaned_message)
	return cleaned_message

def process_data(filename):
	messages = open(filename, 'r')
	message_lines = messages.readlines()
	msg_str = ""
	for line in message_lines:
	    msg_str += line
	final_dict = Counter(msg_str.split())
	return msg_str, final_dict