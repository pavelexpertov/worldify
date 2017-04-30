import numpy as np
from collections import Counter
import time
import sys
import os
import pickle


class SentimentNetwork:
    def __init__(
        self, reviews,
        labels, hidden_nodes=10, polarity=0.05,
        min_count=10, learning_rate=0.1
    ):
        self.reviews = reviews
        self.labels = labels
        np.random.seed(1)
        print('Pre prcoessing about to start')
        self.pre_process_data(self.reviews, polarity, min_count)
        print('Pre processing has just finished')
        self.init_network(
            len(self.review_vocab), hidden_nodes, 1, learning_rate)

    def pre_process_data(self, reviews, polarity, min_count):

        positive_counts = Counter()
        negative_counts = Counter()
        total_counts = Counter()

        for i in range(len(reviews)):
            if(self.labels[i] == 'POSITIVE'):
                for word in reviews[i].split(" "):
                    positive_counts[word] += 1
                    total_counts[word] += 1
            else:
                for word in reviews[i].split(" "):
                    negative_counts[word] += 1
                    total_counts[word] += 1

        print('Get total count of words')

        pos_neg_ratios = Counter()

        for term, cnt in list(total_counts.most_common()):
            if(cnt > 100):
                pos_neg_ratio = positive_counts[term] / float(
                    negative_counts[term]+1)
                pos_neg_ratios[term] = pos_neg_ratio

        print('Get ratio of words')

        for word, ratio in pos_neg_ratios.most_common():
            if(ratio > 1):
                pos_neg_ratios[word] = np.log(ratio)
            else:
                pos_neg_ratios[word] = -np.log((1 / (ratio+0.01)))

        print('Get total log ratio of words')

        if not (os.path.isfile('./review_vocab.pkl')):
            review_vocab = set()
            for review in reviews:
                for word in review.split(" "):
                    if(total_counts[word] > min_count):
                        if(word in pos_neg_ratios.keys()):
                            if(pos_neg_ratios[word] >= polarity or pos_neg_ratios[word] <= -polarity):
                                review_vocab.add(word)
                        else:
                            review_vocab.add(word)

            pkl_file = open('./review_vocab.pkl', 'wb')
            pickle.dump(review_vocab, pkl_file)
        else:
            pkl_file = open('./review_vocab.pkl', 'rb')
            review_vocab = pickle.load(pkl_file)

        pkl_file.close()
        self.review_vocab = list(review_vocab)

        print('Get only the words with high polarity')

        label_vocab = set()
        for label in self.labels:
            label_vocab.add(label)

        self.label_vocab = list(label_vocab)
        self.review_vocab_size = len(self.review_vocab)
        self.label_vocab_size = len(self.label_vocab)
        self.word2index = {}
        for i, word in enumerate(self.review_vocab):
            self.word2index[word] = i
        self.label2index = {}
        for i, label in enumerate(self.label_vocab):
            self.label2index[label] = i

        print('Pre prcoessing of method has finished')

    def init_network(
        self, input_nodes, hidden_nodes, output_nodes, learning_rate
    ):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        self.weights_0_1 = np.zeros((self.input_nodes, self.hidden_nodes))

        self.weights_1_2 = np.random.normal(
            0.0, self.output_nodes**-0.5,
            (self.hidden_nodes, self.output_nodes)
        )
        self.learning_rate = learning_rate
        self.layer_0 = np.zeros((1, input_nodes))
        self.layer_1 = np.zeros((1, hidden_nodes))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_output_2_derivative(self, output):
        return output * (1 - output)

    def update_input_layer(self, review):
        self.layer_0 *= 0
        for word in review.split(" "):
            self.layer_0[0][self.word2index[word]] = 1

    def get_target_for_label(self, label):
        if(label == 'POSITIVE'):
            return 1
        else:
            return 0

    def train(self, training_reviews_raw, training_labels):
        training_reviews = list()
        print('Training has started', len(training_reviews_raw))
        for i in range(len(training_reviews_raw)):
            print('First for', i)
            indices = set()
            for word in training_reviews_raw[i].split(" "):
                if(word in self.word2index.keys()):
                    indices.add(self.word2index[word])
            print('Second for')
            training_reviews.append(list(indices))
            print('Done {} \n'.format(i))
        assert(len(training_reviews) == len(training_labels))
        correct_so_far = 0
        start = time.time()
        for i in range(len(training_reviews)):
            review = training_reviews[i]
            label = training_labels[i]

            # Input Layer

            # Hidden layer
#             layer_1 = self.layer_0.dot(self.weights_0_1)
            self.layer_1 *= 0
            for index in review:
                self.layer_1 += self.weights_0_1[index]
            # Output layer
            layer_2 = self.sigmoid(self.layer_1.dot(self.weights_1_2))

            # Output error
            layer_2_error = layer_2 - self.get_target_for_label(label)
            layer_2_delta = layer_2_error * self.sigmoid_output_2_derivative(
                layer_2
            )

            # Backpropagated error
            layer_1_error = layer_2_delta.dot(self.weights_1_2.T)
            layer_1_delta = layer_1_error

            self.weights_1_2 -= self.layer_1.T.dot(
                layer_2_delta) * self.learning_rate
            for index in review:
                self.weights_0_1[index] -= layer_1_delta[0] * self.learning_rate

            if(np.abs(layer_2_error) < 0.5):
                correct_so_far += 1
            reviews_per_second = i / float(time.time() - start)
            sys.stdout.write("\rProgress:" + str(100 * i/float(
                len(training_reviews)))[:4] + "% Speed(reviews/sec):" + str(
                    reviews_per_second)[0:5] + " #Correct:" + str(
                    correct_so_far) + " #Trained:" + str(i+1)
                    + " Training Accuracy:" + str(correct_so_far * 100 / float(
                        i+1))[:4] + "%")

        return self.weights_0_1, self.weights_1_2

    def test(self, weight_0_1, weight_0_2, testing_reviews):
        get_results = []
        for i in range(len(testing_reviews)):
            pred, prob = self.run(weight_0_1, weight_0_2, testing_reviews[i])
            get_results.append((pred, prob))
        return get_results

    def run(self, weight_0_1, weight_0_2, review):
        self.layer_1 *= 0
        unique_indices = set()
        for word in review.lower().split(" "):
            if word in self.word2index.keys():
                unique_indices.add(self.word2index[word])
        for index in unique_indices:
            self.layer_1 += weight_0_1[index]
        layer_2 = self.sigmoid(self.layer_1.dot(weight_0_2))
        if(layer_2[0] > 0.5):
            return "POSITIVE", layer_2
        else:
            return "NEGATIVE", layer_2
