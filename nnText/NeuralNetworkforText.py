#Adopted from https://pythonprogramming.net/train-test-tensorflow-deep-learning-tutorial/
from preProcessingText import create_feature_sets_and_labels
import tensorflow as tf
import pickle
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
train_x,train_y,test_x,test_y = create_feature_sets_and_labels('data/pos.txt','data/neg.txt')

n_nodes_hl1 = 1500
n_nodes_hl2 = 1500
n_nodes_hl3 = 1500
n_nodes_hl4 = 1500

n_classes = 2
batch_size = 100
hm_epochs = 8

x = tf.placeholder('float')
y = tf.placeholder('float')
#Construct the NN by creating individual layers. The first hidden layer is the input layer.
hidden_1_layer = {'f_fum':n_nodes_hl1,
                  'weight':tf.Variable(tf.random_normal([len(train_x[0]), n_nodes_hl1])),
                  'bias':tf.Variable(tf.random_normal([n_nodes_hl1]))}

hidden_2_layer = {'f_fum':n_nodes_hl2,
                  'weight':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
                  'bias':tf.Variable(tf.random_normal([n_nodes_hl2]))}

hidden_3_layer = {'f_fum':n_nodes_hl3,
                  'weight':tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
                  'bias':tf.Variable(tf.random_normal([n_nodes_hl3]))}

# hidden_4_layer = {'f_fum':n_nodes_hl4,
#                   'weight':tf.Variable(tf.random_normal([n_nodes_hl3, n_nodes_hl4])),
#                   'bias':tf.Variable(tf.random_normal([n_nodes_hl4]))}

output_layer = {'f_fum':None,
                'weight':tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
                'bias':tf.Variable(tf.random_normal([n_classes])),}


# Construct the model by summing the previous inputs and passing it through a nonlinear activation function
def neural_network_model(data):

    l1 = tf.add(tf.matmul(data,hidden_1_layer['weight']), hidden_1_layer['bias'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1,hidden_2_layer['weight']), hidden_2_layer['bias'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2,hidden_3_layer['weight']), hidden_3_layer['bias'])
    l3 = tf.nn.relu(l3)

    # l4 = tf.add(tf.matmul(l3,hidden_4_layer['weight']), hidden_4_layer['bias'])
    # l4 = tf.nn.relu(l4)

    output = tf.matmul(l3,output_layer['weight']) + output_layer['bias']

    return output

#Train the network by calculating the error and adjusting the weights hm_epochs number of times.
def train_neural_network(x):
	prediction = neural_network_model(x)
	cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits_v2(logits=prediction, labels=y) )
	optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(cost)

	with tf.Session() as sess:
		#sess.run(tf.initialize_all_variables())
		sess.run(tf.global_variables_initializer())
		for epoch in range(hm_epochs):
			epoch_loss = 0
			i=0
			while i < len(train_x):
				start = i
				end = i+batch_size
				batch_x = np.array(train_x[start:end])
				batch_y = np.array(train_y[start:end])

				_, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
				                                              y: batch_y})
				epoch_loss += c
				i+=batch_size
				
			print('Epoch', epoch+1, 'completed out of',hm_epochs,'loss:',epoch_loss)
		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))

		print('Accuracy:',accuracy.eval({x:test_x, y:test_y}))
train_neural_network(x)
	    

