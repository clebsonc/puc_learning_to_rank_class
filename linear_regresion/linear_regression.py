import numpy as np
from matplotlib import pyplot as plt


class LinearRegression(object):
    def __init__(self, x, y):
        self.x = np.asarray(x)
        self.y = np.asarray(y)

        self.m = None
        self.b = None

    def draw(self):
        """ Draw the linear regression fit. """
        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(self.x, self.y, linestyle='', marker='s')
        line = list()
        if self.m is not None and self.b is not None:
            for i in self.x:
                line.append(self.m * i + self.b)
            ax.plot(self.x, line, color='red')
            plt.show()


class LinearRegressionLeastSquare(LinearRegression):
    def __init__(self, x, y):
        super().__init__(x=x, y=y)

    def solve_equation(self):
        """ This functions solves the linear regression equation:
            y = mx + b
                -> m is the slope
                -> b is the intercept
        """
        m_numerator = np.sum(np.dot(a=self.x - np.mean(self.x), b=self.y - np.mean(self.y)))
        m_denominator = np.sum((self.x - np.mean(self.x))**2)
        m = m_numerator / m_denominator

        b = np.mean(self.y) - m * np.mean(self.x)
        self.m = m
        self.b = b

    def predict(self, x):
        return self.m * x + self.b


class LinearRegressionGradient(LinearRegression):
    def __init__(self, x, y, steps=1000, learning_rate=1):
        super().__init__(x=x, y=y)
        self.steps = steps
        self.learning_rate = learning_rate
        self.m = 1
        self.b = 1

    def compute_gradient(self):
        errors = np.zeros(len(self.x))
        for idx in range(len(self.x)):
            guess = self.m * self.x[idx] + self.b
            errors[idx] = self.y[idx] - guess
            self.m += errors[idx] * self.x[idx] * self.learning_rate
            self.b += errors[idx] * self.learning_rate
        cost = np.sum(errors**2)
        return cost

    def train(self):
        cost_per_iteration = list()
        idx = 0
        while idx < self.steps:
            cost_per_iteration.append(self.compute_gradient())
            idx += 1
        return cost_per_iteration


if __name__ == "__main__":
    x = np.asarray([1, 1.5, 2, 3, 4, 4.5, 5, 6, 7, 8, 9, 10])
    y = np.asarray([1.5, 2, 3.5, 4, 3, 4.5, 3, 3.5, 6, 9, 5.5, 6])

    ln = LinearRegressionLeastSquare(x=x, y=y)
    ln.solve_equation()
    ln.draw()