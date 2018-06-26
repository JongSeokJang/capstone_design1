import re
import os
import sys
import json
import numpy as np
import pandas as pd
import tensorflow as tf
import data_helper
import random
import time
from tensorflow.contrib import learn
from konlpy.tag import Mecab
from konlpy.utils import pprint
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def clean_str(s):
    """Clean sentence"""
    global counter_konlpy
    global total_dataset
    s = re.sub('[0-9]', '', s)
    mecab = Mecab()
    result = []
    result = mecab.nouns(s)
    if len(result) > 3000:
        result = result[0:3000]
    counter_konlpy += 1
    sys.stdout.write("\r Parsed: %d / %d" %(counter_konlpy, total_dataset))
    sys.stdout.flush()
    return ' '.join(result)

def get_x_test(contents):
    """Step 1: load data for prediction"""
    columns = ['section', 'class', 'subclass', 'abstract']
    selected = ['section', 'abstract']
    #test_list = test_list[0:10000]
    data = []
    #print("Listing all datas in testset.")
    start = time.time()
    for content in contents:
        #print(content)
        data.append(['', '', '', content])
    df = pd.DataFrame(data, columns=columns)
    global counter_konlpy
    global total_dataset
    start = time.time()
    counter_konlpy = 0
    total_dataset = len(contents)
    #x_raw = [example['abstract'] for example in test_examples]
    #x_test = [data_helper.clean_str(x) for x in x_raw]
    x_test = df[selected[1]].apply(lambda x: clean_str(x)).tolist()
    #print("\nExecution time = {0:.5f}".format(time.time() - start))



    return x_test

def get_classification_models():
    checkpoint_dir =  dir_path + '/trained_model/'
    models = []
    try:
        dirs = list(os.walk(checkpoint_dir))[0][1]
        models = dirs
    except:
        models = []

    return models

def get_category_name(model_name):
    checkpoint_dir =  dir_path + '/trained_model/' + str(model_name)
    category_name = ''
    try:
        f = open(checkpoint_dir + '/category.json')
        category_name = json.loads(''.join(f.readlines()))['name']
    except Exception as e:
        category_name = ''

    return category_name

def predict_unseen_data(x_test, model_name):
    """Step 0: load trained model and parameters"""
    params = json.loads(open(dir_path + '/parameters.json').read())
    checkpoint_dir =  dir_path + '/trained_model/' + str(model_name)
    print(checkpoint_dir)
    if not checkpoint_dir.endswith('/'):
        checkpoint_dir += '/'
    checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir + 'checkpoints')

    vocab_path = os.path.join(checkpoint_dir, "vocab.pickle")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_test)))

    
    """Step 2: compute the predictions"""
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(allow_soft_placement=True, log_device_placement=False, device_count = {'GPU': 0})
        sess = tf.Session(config=session_conf)

        with sess.as_default():
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            input_x = graph.get_operation_by_name("input_x").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            batches = data_helper.batch_iter(list(x_test), params['batch_size'], 1, shuffle=False)
            all_predictions = []
            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])

    all_predictions = list(map(lambda x: int(np.asscalar(x)), all_predictions))

    try:
        f = open(checkpoint_dir + 'labels.json')
        label_data = ''.join(f.readlines())
        labels = json.loads(label_data)
        all_predictions = list(map(lambda x: labels[x], all_predictions))
    except Exception as e:
        all_predictions = []
    return all_predictions
