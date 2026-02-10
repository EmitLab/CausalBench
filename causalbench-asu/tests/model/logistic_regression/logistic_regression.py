from sklearn.linear_model import LogisticRegression


def execute(
    data,
    penalty,
    C,
    l1_ratio,
    dual,
    tol,
    fit_intercept,
    intercept_scaling,
    class_weight,
    random_state,
    solver,
    max_iter,
    verbose,
    warm_start,
    helpers: any,
):
    X = helpers.get_features(data)
    y = helpers.get_target(data)

    model = LogisticRegression(
        penalty=penalty,
        C=C,
        l1_ratio=l1_ratio,
        dual=dual,
        tol=tol,
        fit_intercept=fit_intercept,
        intercept_scaling=intercept_scaling,
        class_weight=class_weight,
        random_state=random_state,
        solver=solver,
        max_iter=max_iter,
        verbose=verbose,
        warm_start=warm_start,
    )

    model.fit(X, y)

    prediction = model.predict(X)

    helpers.set_target(data, prediction)

    return {"prediction": data}
