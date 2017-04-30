import os
import numpy as np
from sentiment_network import SentimentNetwork


def run_sentiment_analysis(test_reviews):
    g = open('reviews.txt', 'r')
    reviews = list(map(lambda x: x[:-1], g.readlines()))
    g.close()

    g = open('labels.txt', 'r')
    labels = list(map(lambda x: x[:-1].upper(), g.readlines()))
    g.close()

    print('The data has been intialized')

    mlp = SentimentNetwork(
        reviews[:-1000], labels[:-1000],
        polarity=0.8, min_count=20, learning_rate=0.01
    )

    print('Sentiment network initialized')

    if not (os.path.isfile('./weights_layer_0_1.dat') and os.path.isfile('./weights_layer_0_2.dat')):
        weights_layer_1, weights_layer_2 = mlp.train(
           reviews[:-1000], labels[:-1000]
        )
        print('Training has finished')
        weights_layer_1.dump("./weights_layer_0_1.dat")
        weights_layer_2.dump("./weights_layer_0_2.dat")
        print('Hyper parameters have been saved')


    weights_0_1 = np.load("./weights_layer_0_1.dat")
    weights_0_2 = np.load("./weights_layer_0_2.dat")
    results = mlp.test(weights_0_1, weights_0_2, test_reviews)
    get_energy_value = np.mean([i[1] for i in results])
    return get_energy_value
