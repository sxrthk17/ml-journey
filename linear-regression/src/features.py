from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

#----------------------------------------------

def one_hot_encode(X_train, X_test, columns=[]):
    if not columns:
        raise ValueError("No column to OneHotEncode")

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore", drop='first')

    encoded_array = encoder.fit_transform(X_train[columns])
    encoded_df = pd.DataFrame(encoded_array, columns= encoder.get_feature_names_out(columns), index=X_train.index)

    X_train = X_train.drop(columns=columns).join(encoded_df)

    encoded_array = encoder.transform(X_test[columns])
    encoded_df = pd.DataFrame(encoded_array, columns=encoder.get_feature_names_out(columns), index=X_test.index)

    X_test = X_test.drop(columns=columns).join(encoded_df)

    X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

    return X_train, X_test

#----------------------------------------------

def split_sets_tr_val(X_train, y_train, feature_cols):

    split_idx = int(len(X_train) * 0.8)
    X_tr = X_train.iloc[:split_idx][feature_cols]
    y_tr = y_train.iloc[:split_idx]

    X_val = X_train.iloc[split_idx:][feature_cols]
    y_val = y_train.iloc[split_idx:]

    return X_tr, y_tr, X_val, y_val

#----------------------------------------------

def clean_and_preprocess_data(df, target_cols=['cnt'], feature_cols=None, cat_cols=None):
    '''
    The dataset comes uncleaned, raw and full of skewked distribution,
    my goal here is to design a helper function, that takes in,
    the raw features and target values, transform them on the basis of
    planned transformations and give them back to the user,
    here we will split the data into train test and train into train and validation set
    apply transformation on X and y train val sets, and hald them back to users!
    assuming X has features and not target variables, but still confirming.
    '''
    if isinstance(target_cols, str):
            target_cols = [target_cols]

    if feature_cols is None:
        feature_cols = [
            "holiday", "yr", "season", "weathersit",
            "hr", "atemp", "hum", "windspeed"
        ]

    X = df.drop(columns=target_cols).copy()
    
    y = df[target_cols].copy()


    if 'weathersit' in X.columns:
        X['weathersit'] = X['weathersit'].replace(4, 3)

    ## splitting the data !! 
    X_train, X_test , y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    split_idx = int(len(X_train) * 0.8)
    X_tr = X_train.iloc[:split_idx].copy()
    X_val = X_train.iloc[split_idx:].copy()
    y_tr = y_train.iloc[ :split_idx ].copy()
    y_val = y_train.iloc[split_idx: ].copy()

    features = feature_cols

    X_tr = X_tr[features]
    X_val = X_val[features]


    cat_cols = cat_cols if cat_cols is not None else ['season', 'weathersit', 'hr']
    X_tr, X_val = one_hot_encode(X_tr, X_val, columns=cat_cols)

    y_tr_log, y_val_log = target_logger(y_tr, y_val)

    return X_tr, y_tr_log, X_val, y_val_log


#----------------------------------------------

def target_logger(y_train, y_test):
    y_train = np.log1p(y_train)
    y_test = np.log1p(y_test)

    return y_train, y_test


#----------------------------------------------
def compute_vif(X):
    scaler = StandardScaler()
    Z = scaler.fit_transform(X)
    n = X.shape[0]
    
    #correlation matrix R
    # R = (1/n-1) * Z.T @ Z fell into a classic python operator precedence trap !!
    R = (1/(n-1)) * Z.T @ Z
    #invert r to get c
    C = np.linalg.pinv(R)

    VIF_score = np.diag(C)
    return pd.DataFrame(VIF_score, index=X.columns).rename(columns={0: "VIF"})
#----------------------------------------------










