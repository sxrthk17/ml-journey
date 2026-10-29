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