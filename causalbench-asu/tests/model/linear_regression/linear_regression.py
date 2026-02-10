from sklearn.linear_model import LinearRegression


def execute(data, fit_intercept, positive):
    X = data.data
    y = data.target

    model = LinearRegression(fit_intercept=fit_intercept, positive=positive)
    model.fit(X, y)

    prediction = model.predict(X)

    return {"prediction": prediction}
