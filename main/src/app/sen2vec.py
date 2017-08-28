from gensim.models import word2vec
import logging
import os.path
import numpy as np
from sys import stdin
from scipy import spatial
import json

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def get_model(model_file, training_file):
    """Return a word2vec model"""
    # Return the existing model if it exists
    logging.info("Seeking model from {}".format(model_file))
    model = None
    if os.path.isfile(model_file):
        logging.info("Model file found, retrieving")
        model = word2vec.Word2Vec.load(model_file)
        return model

    # Create and save the new model
    logging.info(
        "No model file found, training with {}".format(training_file))
    sentences = word2vec.Text8Corpus(training_file)
    model = word2vec.Word2Vec(sentences, size=200)
    model.save(model_file)

    # Return the model
    return model


def get_sentence_vector(model, sentence):
    """Get a simple average of the word vectors in the sentence"""
    logging.debug("The sentence is: {}".format(sentence))
    words = sentence.lower().split()
    logging.debug("The words are: {}".format(words))
    vector_list = [model.wv[word] for word in words if word in model.wv]
    logging.debug("The word vectors are: {}".format(vector_list))
    sentence_vector = np.mean(np.array(vector_list), axis=0)
    logging.debug("The sentence_vector is: {}".format(sentence_vector))
    return sentence_vector


def get_score(model, question):
    """Rank the results"""
    target = question["target"]
    answer = {
        "target": target,
        "candidates": []
    }
    target_vec = get_sentence_vector(model, target)
    for candidate in question["unscored_candidates"]:
        can_vec = get_sentence_vector(model, candidate)
        # Subtracting from 1.0 to provide cosine similarity from cosine distance
        similarity = round(
            (1 - spatial.distance.cosine(target_vec, can_vec)), 4)
        answer["candidates"].append(
            {"text": candidate, "score": similarity})
    sorted_candidates = sorted(
        answer["candidates"], key=lambda k: -1 * k["score"])
    answer["candidates"] = sorted_candidates
    return answer


def demonstrate(model):
    """Offer a command line interface for demonstration purposes"""
    target_sentence = ""
    while target_sentence != "quit":
        logging.info("Enter a question or type quit to exit: ")
        target_sentence = stdin.readline().rstrip()
        if target_sentence == "quit":
            continue
        question = {
            "target": target_sentence,
            "unscored_candidates": [
                # "What is the weather in Sunnyvale?",
                "Can I cancel my VIP membership?",
                "Can I track my order?",
                "Hello",
                "I would like to order socks",
                "Can I return this dress?",
                "Can I buy some shoes?"
            ]
        }
        answer = get_score(model, question)
        answer_json = json.dumps(
            answer, sort_keys=True, indent=4, separators=(",", ":"))
        logging.info("answer:\n{}".format(answer_json))


if __name__ == "__main__":
    logging.info("Starting simulation.")
    model = get_model("main/data/my_model", "main/data/training/text8")
    demonstrate(model)
