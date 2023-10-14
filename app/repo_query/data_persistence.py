""" Module for loading and saving data to and from pickle files. """
import logging
import os
import pickle


def load_pickle(filename, pickle_docs_dir):
    """Load pickled data from a file."""
    try:
        with open(os.path.join(pickle_docs_dir, filename), "rb") as file:
            logging.debug("Loading pickled embeddings from %s", filename)
            return pickle.load(file)
    except FileNotFoundError:
        logging.error("File not found: %s", filename)
        raise


def save_pickle(obj, filename, pickle_docs_dir):
    """Save data to a pickle file."""
    with open(os.path.join(pickle_docs_dir, filename), "wb") as file:
        logging.debug("Saving pickled embeddings to %s", filename)
        pickle.dump(obj, file)
