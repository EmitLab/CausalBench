from sklearn.tree import DecisionTreeRegressor


def execute(
    data,
    criterion,
    splitter,
    max_depth,
    min_samples_split,
    min_samples_leaf,
    ccp_alpha,
    random_state,
    helpers: any
):
    X = helpers.get_features(data)
    y = helpers.get_target(data)

    model = DecisionTreeRegressor(
        criterion=criterion,
        splitter=splitter,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        ccp_alpha=ccp_alpha,
        random_state=random_state,
    )
    model.fit(X, y)

    prediction = model.predict(X)

    helpers.set_target(data, prediction)

    return {"prediction": data}
