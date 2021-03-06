import tensorflow as tf
import numpy as np
import os
import cPickle as pickle
from os.path import expanduser
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..","util")))
from tf_utils import fcLayer, createLSTMCell, applyActivation, predictionLayer
#from predContext import predContext, createHtDict

class model(object):
        
        # Model params
        # 0 -- shared;  1 -- context;  2 -- task
	fc_activation = "tanh"
	output_activation = "tanh"
	dropout = 0.0
	body_lstm_size = 128
	context_lstm_size = 128
	task_lstm_size = 128
	body_n_layer = 1
	context_n_layer = 1
	task_n_layer = 1
	context_branch_fc = 512
	task_branch_fc = 512

	# Data params
	batch_size = 128
	max_length = 52
	feature_length = 300
	context_dim = 300
	task_dim = 2

	# Hyper- params
	lr = 0.001
	context_lr = lr
	n_epoch = 500
	topN = 4
	keep_prob_val = 1.0

	def buildModel(self, x, y_context, y_task, is_train, dropout, scope="multiTask"):
     
    	    # Assume the input shape is (batch_size, max_length, feature_length) 

    	    #TASK = primary task, CONTEXT = secondary task
    
    	    # Create lstm cell for the shared layer 
            body_lstm_cell, _ = createLSTMCell(self.batch_size, self.body_lstm_size, self.body_n_layer, forget_bias=0.0)
            # Create lstm cell for branch 1 
            context_lstm_cell, _ = createLSTMCell(self.batch_size, self.context_lstm_size, self.context_n_layer, forget_bias=0.0)
            # Create lstm cells for branch 2
	    task_lstm_cell, _ = createLSTMCell(self.batch_size, self.task_lstm_size, self.task_n_layer, forget_bias=0.0)

    	    context_cost = tf.constant(0)
    	    task_cost = tf.constant(0)

    	    with tf.variable_scope("shared_lstm"):
        	body_cell_output, last_body_state = tf.nn.dynamic_rnn(cell = body_lstm_cell, dtype=tf.float32, sequence_length=self.length(x), inputs=x)
        
    	    with tf.variable_scope("context_branch"):
        	context_cell_output, last_context_state = tf.nn.dynamic_rnn(cell = context_lstm_cell, dtype=tf.float32, sequence_length=self.length(body_cell_output), inputs=body_cell_output)

    	    # The output from LSTMs will be (batch_size, max_length, out_size)
    	    with tf.variable_scope("context_fc"):
        	# Select the last output that is not generated by zero vectors
        	last_context_output = self.last_relevant(context_cell_output, self.length(context_cell_output))
        	# feed the last output to the fc layer and make prediction
        	context_fc_out = fcLayer(x=last_context_output, in_shape=self.context_lstm_size, out_shape=self.context_branch_fc, activation=self.fc_activation, dropout=self.dropout, is_train=is_train, scope="fc1")
        	context_cost, context_output = predictionLayer(x=context_fc_out, y=y_context, in_shape=self.context_branch_fc, out_shape=y_context.get_shape()[-1].value, activation=self.output_activation)

    	    with tf.variable_scope("task_branch"):
        	task_cell_output, last_task_state = tf.nn.dynamic_rnn(cell = task_lstm_cell, dtype=tf.float32, sequence_length=self.length(body_cell_output), inputs=body_cell_output)

    	    with tf.variable_scope("task_fc"):
        	# Select the last output that is not generated by zero vectors
        	last_task_output = self.last_relevant(task_cell_output, self.length(task_cell_output))
        	# feed the last output to the fc layer and make prediction
        	task_fc_out = fcLayer(x=last_task_output, in_shape=self.task_lstm_size, out_shape=self.task_branch_fc, activation=self.fc_activation, dropout=self.dropout, is_train=is_train, scope="fc2")
        	task_cost, task_output = predictionLayer(x=task_fc_out, y=y_task, in_shape=self.context_branch_fc, out_shape=y_task.get_shape()[-1].value, activation=self.output_activation)

    	    return context_cost, task_cost, task_output, context_output

	# Flatten the output tensor to shape features in all examples x output size
	# construct an index into that by creating a tensor with the start indices for each example tf.range(0, batch_size) x max_length
	# and add the individual sequence lengths to it
	# tf.gather() then performs the acutal indexing.
	def last_relevant(self, output, length):
    	    index = tf.range(0, self.batch_size) * self.max_length + (length - 1)
            out_size = int(output.get_shape()[2])
    	    flat = tf.reshape(output, [-1, out_size])
   	    relevant = tf.gather(flat, index)
    	    return relevant

# Assume that the sequences are padded with 0 vectors to have shape (batch_size, max_length, feature_length)

        def length(self, sequence):
            used = tf.sign(tf.reduce_max(tf.abs(sequence), reduction_indices=2))
            length = tf.reduce_sum(used, reduction_indices=1)
            length = tf.cast(length, tf.int32)
            print length.get_shape()
            return length





