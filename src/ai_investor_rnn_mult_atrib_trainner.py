# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 16:14:47 2023

@author: ccgov
"""

from __future__ import print_function

import math ##For basic mathematical operations

from IPython import display ## Plot setup for Ipython
from matplotlib import cm ##  Colormap reference
from matplotlib import gridspec ##plot setups
from matplotlib import pyplot as plt ##plot setups
import numpy as np 
import pandas as pd
from sklearn import metrics
import tensorflow as tf
from tensorflow.python.data import Dataset

import constants
from tensorflow.keras import optimizers
import logging
import datetime
from functools import partial

logging.getLogger("tensorflow").setLevel(logging.ERROR)

#tf.logging.set_verbosity(tf.logging.ERROR)
pd.options.display.max_rows = 10
#pd.options.display.max_cols = 1000
pd.options.display.float_format = '{:.1f}'.format
ativo="WIN@N"


def read_data(plot=True):
    data = pd.read_csv(constants.DATA_PATH_STOCKS+ativo+'-ind.csv', sep=';')
    
    data['date'] = pd.to_datetime(data['data'], format='%Y%m%d')
    
    data = data.loc[(data['data'] > 20210101) & (data['data']<20220101)]
    #data = data.loc[(data['date'] > datetime(2021,1,1)) & (data['date']<datetime(2022,1,1))]
    return data

dataframe = read_data() #pd.read_csv(constants.DATA_PATH_STOCKS+ativo+'-ind.csv', sep=';')
dataframe.info()
dataframe = dataframe.dropna()
print(dataframe[["BBP-50", "BBP-200", "SO-20", "SO-50", "SO-200"]].head(1))

#dataframe["height"] = dataframe["height"]*-1
dataframe = dataframe.reindex(
    np.random.permutation(dataframe.index))
dataframe.head()


def preprocess_features(dataframe):
  
  selected_features = dataframe[
    [
      "open", "high", "low"
         , "SMA-LREG-20", "BBH-LREG-20", "BBL-LREG-20"
      
    ]]

     
  
  selected_features[["open", "high", "low"]] = selected_features[["open", "high", "low"]] #/10000.0
  processed_features = selected_features.copy()
  return processed_features

def preprocess_targets(dataframe):

  output_targets = pd.DataFrame()
  # Scale the target to be in units of thousands of dollars.
  output_targets["close"] = (
    dataframe["close"] #/ 10000.0
    )
  return output_targets





training_examples = preprocess_features(dataframe.head(12000*2))
training_targets = preprocess_targets(dataframe.head(12000*2))

validation_examples = preprocess_features(dataframe.tail(5000))
validation_targets = preprocess_targets(dataframe.tail(5000))


print("Training examples summary:")
display.display(training_examples.describe())
print("Validation examples summary:")
display.display(validation_examples.describe())

print("Training targets summary:")
display.display(training_targets.describe())
print("Validation targets summary:")
display.display(validation_targets.describe())




def construct_feature_columns(input_features):
  return set([tf.feature_column.numeric_column(my_feature)
              for my_feature in input_features])

def my_input_fn(features, targets, batch_size=1, shuffle=True, num_epochs=None):

    
    # Convert pandas data into a dict of np arrays.
    features = {key:np.array(value) for key,value in dict(features).items()}                                           
    
    # Construct a dataset, and configure batching/repeating.
    ds = Dataset.from_tensor_slices((features,targets)) # warning: 2GB limit
    ds = ds.batch(batch_size).repeat(num_epochs)

    # Shuffle the data, if specified.
    if shuffle:
      ds = ds.shuffle(10000)
    
    # Return the next batch of data.
    features, labels = ds.make_one_shot_iterator().get_next()
    return features, labels


def train_model(
    learning_rate,
    steps,
    batch_size,
    training_examples,
    training_targets,
    validation_examples,
    validation_targets):


  periods = 10
  steps_per_period = steps / periods

  # Create a linear regressor object.
  #my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
  #my_optimizer = tf.optimizers.SGD(learning_rate=learning_rate, clipnorm=5.0)
  my_optimizer = optimizers.SGD(learning_rate=learning_rate, clipnorm=5.0)
###  my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)
  #my_optimizer = partial(optimizers.SGD, learning_rate=learning_rate, momentum=0.9, clipnorm=5.0)
  my_optimizer = partial(optimizers.SGD, learning_rate=learning_rate, clipnorm=5.0)
  linear_regressor = tf.estimator.LinearRegressor(
      feature_columns=construct_feature_columns(training_examples)
      ,      optimizer=my_optimizer
  )
    
  # Create input functions.
  training_input_fn = lambda: my_input_fn(training_examples, 
                                          training_targets["close"], 
                                          batch_size=batch_size)
  predict_training_input_fn = lambda: my_input_fn(training_examples, 
                                                  training_targets["close"], 
                                                  num_epochs=1, 
                                                  shuffle=False)
  predict_validation_input_fn = lambda: my_input_fn(validation_examples, 
                                                    validation_targets["close"], 
                                                    num_epochs=1, 
                                                    shuffle=False)

  # Train the model
  print("Training model...")
  print("RMSE (on training data):")
  training_rmse = []
  validation_rmse = []
  for period in range (0, periods):
    # Train the model
    linear_regressor.train(
        input_fn=training_input_fn,
        steps=steps_per_period,
    )
    
    training_predictions = linear_regressor.predict(input_fn=predict_training_input_fn)
    training_predictions = np.array([item['predictions'][0] for item in training_predictions])
    
    validation_predictions = linear_regressor.predict(input_fn=predict_validation_input_fn)
    validation_predictions = np.array([item['predictions'][0] for item in validation_predictions])
    
   
    training_root_mean_squared_error = math.sqrt(
        metrics.mean_squared_error(training_predictions, training_targets))
    validation_root_mean_squared_error = math.sqrt(
        metrics.mean_squared_error(validation_predictions, validation_targets))
   
    print("  period %02d : %0.2f" % (period, training_root_mean_squared_error))
   
    training_rmse.append(training_root_mean_squared_error)
    validation_rmse.append(validation_root_mean_squared_error)
  print("Model training finished.")

  
  # Output a graph of loss metrics over periods.
  plt.ylabel("RMSE")
  plt.xlabel("Periods")
  plt.title("Root Mean Squared Error vs. Periods")
  plt.tight_layout()
  plt.plot(training_rmse, label="training")
  plt.plot(validation_rmse, label="validation")
  plt.legend()

  return linear_regressor


minimal_features = ["open", "high","low"
         , "SMA-LREG-20", "BBH-LREG-20", "BBL-LREG-20"
                    
                    ] # ["BBP-50", "BBP-200", "SO-20", "SO-50", "SO-200"]

assert minimal_features, "You must select at least one feature!"

minimal_training_examples = training_examples[minimal_features]
minimal_validation_examples = validation_examples[minimal_features]


train_model(
    learning_rate=0.001,
    steps=500,
    batch_size=5,
    training_examples=minimal_training_examples,
    training_targets=training_targets,
    validation_examples=minimal_validation_examples,
    validation_targets=validation_targets)

