from src.data.data_processing import load_dataset, preprocess_data
from src.model.logistic_regression import LogisticRegression
from src.utils.helper_functions import plot_learning_curve

def train_model(X_train, y_train, learning_rate=0.01, num_iterations=2000):
    model = LogisticRegression()
    model.fit(X_train, y_train, num_iterations=num_iterations, learning_rate=learning_rate)
    return model

if __name__ == "__main__":
    # Load and preprocess data
    X_train, y_train = load_dataset(train=True)
    X_train = preprocess_data(X_train)

    # Train model
    model = train_model(X_train, y_train)

    # Save model
    model.save("trained_model.pkl")

    # Plot learning curve
    plot_learning_curve(model.costs)