#!/usr/bin/env python3

import argparse
import connexion
# import datetime
import logging
# import random

# from ..app.sen2vec import get_score2
from ..app.sen2vec import get_model, get_score

# from collections import deque
# from connexion import NoContent


# our memory-only recording storage
RECORDINGS = {}

# our word2vec model
word2vec_model = get_model("main/data/my_model", "main/data/training/text8")


def get_sen2vec_score(question):
    """This simple function re-directs the query to the app layer."""
    return get_score(word2vec_model, question)

logging.basicConfig(level=logging.INFO)
app = connexion.App(__name__)
app.add_api('swagger.yaml')
# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "port_number", type=int, default=80, help="port number for service")
    args = parser.parse_args()
    # run our standalone gevent server
    app.run(port=args.port_number, server='gevent')
