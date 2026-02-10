from sklearn.linear_model import LinearRegression


def execute(data, fit_intercept, tol, positive, helpers: any):
    X = helpers.get_features(data)
    y = helpers.get_target(data)

    model = LinearRegression(
        fit_intercept=fit_intercept,
        tol=tol,
        positive=positive,
    )

    model.fit(X, y)

    prediction = model.predict(X)

    helpers.set_target(data, prediction)

    return {"prediction": data}
