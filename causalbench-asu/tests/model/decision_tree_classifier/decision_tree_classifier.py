from sklearn.tree import DecisionTreeClassifier


def execute(
    data,
    criterion,
    splitter,
    max_depth,
    min_samples_split,
    min_samples_leaf,
    min_weight_fraction_leaf,
    max_features,
    random_state,
    max_leaf_nodes,
    min_impurity_decrease,
    class_weight,
    ccp_alpha,
    helpers: any,
):
    X = helpers.get_features(data)
    y = helpers.get_target(data)

    model = DecisionTreeClassifier(
        criterion=criterion,
        splitter=splitter,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        min_weight_fraction_leaf=min_weight_fraction_leaf,
        max_features=max_features,
        random_state=random_state,
        max_leaf_nodes=max_leaf_nodes,
        min_impurity_decrease=min_impurity_decrease,
        class_weight=class_weight,
        ccp_alpha=ccp_alpha,
    )

    model.fit(X, y)

    prediction = model.predict(X)

    helpers.set_target(data, prediction)

    return {"prediction": data}
