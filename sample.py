from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

from datetime import datetime
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='save',
                        help='model directory to load stored checkpointed models from')
    parser.add_argument('-n', type=int, default=350,
                        help='number of words to sample')
    parser.add_argument('--prime', type=str, default=' ',
                        help='prime text')
    parser.add_argument('--pick', type=int, default=1,
                        help='1 = weighted pick, 2 = beam search pick')
    parser.add_argument('--width', type=int, default=4,
                        help='width of the beam search')
    parser.add_argument('--sample', type=int, default=1,
                        help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')
    parser.add_argument('--count', '-c', type=int, default=1,
                        help='number of samples to print')
    parser.add_argument('--quiet', '-q', default=False, action='store_true',
                        help='suppress printing the prime text (default false)')
    parser.add_argument('--save', '-s', type=str, default=' ',
                        help='should this run be saved in a json file or not (default False)')

    args = parser.parse_args()
    sample(args)


def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'words_vocab.pkl'), 'rb') as f:
        words, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            for _ in range(args.count):
                text = model.sample(sess, words, vocab, args.n, args.prime,
                                    args.sample, args.pick, args.width, args.quiet)
                text = ".".join(text.split(".")[1:-1])+"."
                text = text.lstrip().capitalize()
                if args.save:
                    date_time_now = str(datetime.now())
                    with open("bigfoot_sighting_output.json", "a") as f:
                        bigfoot_d = dict()
                        bigfoot_d[date_time_now] = text
                        with open("bigfoot_sighting_output.json") as f:
                            data = json.load(f)
                        data.update(bigfoot_d)
                        with open("bigfoot_sighting_output.json", 'w') as f:
                            json.dump(data, f, indent=4, sort_keys=False)
                        f.close()
                print(text)


if __name__ == '__main__':
    main()
