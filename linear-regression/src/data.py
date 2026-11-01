## loading and cleaning logic
import pandas as pd
import random

def load_csv(path):
    df = pd.read_csv(path)
    df = df.drop(columns=['instant', 'casual', 'registered'])
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df


def split_data(data, prob):
    results = [], []

    for row in data:
        results[0 if random.random() < prob else 1].append(row)
    return results


def train_test_split(x, y, test_size: float):
    # Ensure inputs have the same length
    assert len(x) == len(y), "Inputs x and y must have the same length"
    
    # 1. Combine and shuffle the data to prevent ordering bias
    data = list(zip(x, y))
    random.shuffle(data)
    
    # 2. Calculate the split index
    split_idx = int(len(data) * (1 - test_size))
    
    # 3. Split the combined data
    train_data = data[:split_idx]
    test_data = data[split_idx:]
    
    # 4. Unpack carefully into lists to avoid empty list crashes
    x_train = [item[0] for item in train_data]
    y_train = [item[1] for item in train_data]
    x_test = [item[0] for item in test_data]
    y_test = [item[1] for item in test_data]
    
    return x_train, y_train, x_test, y_test
