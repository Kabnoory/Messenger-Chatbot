import tensorflow as tf 
import numpy as np 
import sys
from random import randint
import datetime
from sklearn.utils import shuffle
import pickle
import os

def create_matrix(filename, wordlist, maxlength):
	messages_dict= np.load(filename).item()
	num_examples = len(messages_dict)
	xTrain = np.zeros((num_examples, maxlength), dtype='int32')
	yTrain = np.zeros((num_examples, maxlength), dtype='int32')
	for index,(key,value) in enumerate(messages_dict.iteritems()):
		# Will store integerized representation of strings here (initialized as padding)
		encoder_msg = np.full((maxlength), wordlist.index('<pad>'), dtype='int32')
		decoder_msg = np.full((maxlength), wordlist.index('<pad>'), dtype='int32')
		# Getting all the individual words in the strings
		key_split = key.split()
		value_split = value.split()
		key_count = len(key_split)
		value_count = len(value_split)
		# Throw out sequences that are too long
		if (key_count > (maxlength - 1) or value_count > (maxlength - 1)):
			continue
		# Integerize the encoder string
		for key_index, word in enumerate(key_split):
			try:
				encoder_msg[key_index] = wordlist.index(word)
			except ValueError:
				encoder_msg[key_index] = 0
		encoder_msg[key_index + 1] = wordlist.index('<EOS>')
		# Integerize the decoder string
		for value_index, word in enumerate(value_split):
			try:
				decoder_msg[value_index] = wordlist.index(word)
			except ValueError:
				decoder_msg[value_index] = 0
		decoder_msg[value_index + 1] = wordlist.index('<EOS>')
		xTrain[index] = encoder_msg
		yTrain[index] = decoder_msg
	# Remove rows with all zeros
	yTrain = yTrain[~np.all(yTrain == 0, axis=1)]
	xTrain = xTrain[~np.all(xTrain == 0, axis=1)]
	num_examples = xTrain.shape[0]
	return num_examples, xTrain, yTrain

def get_batch(local_XTrain, local_YTrain, local_batch_size, wordlist, maxlength):
	num = randint(0,num_training_examples - local_batch_size - 1)
	arr = local_XTrain[num:num + local_batch_size]
	labels = local_YTrain[num:num + local_batch_size]
	# Reversing the order of encoder string
	reversed_list = list(arr)
	for index,example in enumerate(reversed_list):
		reversed_list[index] = list(reversed(example))

	# Lagged labels are for the training input into the decoder
	lagged_labels = []
	EOS_token_index = wordlist.index('<EOS>')
	pad_token_index = wordlist.index('<pad>')
	for example in labels:
		eos_found = np.argwhere(example==EOS_token_index)[0]
		shifted_example = np.roll(example,1)
		shifted_example[0] = EOS_token_index
		# The EOS token was already at the end, so no need for pad
		if (eos_found != (maxlength - 1)):
			shifted_example[eos_found+1] = pad_token_index
		lagged_labels.append(shifted_example)

	# Need to transpose these 
	reversed_list = np.asarray(reversed_list).T.tolist()
	labels = labels.T.tolist()
	lagged_labels = np.asarray(lagged_labels).T.tolist()
	return reversed_list, labels, lagged_labels

def get_test_input(input_msg, wordlist, maxlength):
	encoder_msg = np.full((maxlength), wordlist.index('<pad>'), dtype='int32')
	input_split = input_msg.lower().split()
	for index,word in enumerate(input_split):
		try:
			encoder_msg[index] = wordlist.index(word)
		except ValueError:
			continue
	encoder_msg[index + 1] = wordlist.index('<EOS>')
	encoder_msg = encoder_msg[::-1]
	encoder_msg_list=[]
	for num in encoder_msg:
		encoder_msg_list.append([num])
	return encoder_msg_list

def nums_to_sentence(nums, wordlist):
    EOS_token_index = wordlist.index('<EOS>')
    pad_token_index = wordlist.index('<pad>')
    msg_str = ""
    response=[]
    for num in nums:
        if (num[0] == EOS_token_index or num[0] == pad_token_index):
            response.append(msg_str)
            msg_str = ""
        else:
            msg_str = msg_str + wordlist[num[0]] + " "
    if msg_str:
        response.append(msg_str)
    response = [i for i in response if i]
    return response
