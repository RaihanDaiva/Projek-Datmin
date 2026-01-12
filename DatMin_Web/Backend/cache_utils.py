import os
import pickle

def save_cache(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_cache(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'rb') as f:
        return pickle.load(f)
