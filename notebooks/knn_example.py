#!/usr/bin/env python3
"""
Anomaly Detection using K-Nearest Neighbors (KNN)

This script demonstrates anomaly detection using KNN.
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt


def main():
    # Create a sample dataframe for demonstration
    data = {
        "total_day_charge": np.random.rand(100) * 100,
        "total_eve_charge": np.random.rand(100) * 50,
        "churn": np.random.randint(0, 2, 100),
    }
    churn_df = pd.DataFrame(data)

    print("Sample data:")
    print(churn_df.head())

    # Prepare features and target
    x = churn_df[["total_day_charge", "total_eve_charge"]].values
    y = churn_df["churn"].values
    print(f"Features shape: {x.shape}, Target shape: {y.shape}")

    # Define and train the KNN model
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(x, y)

    # Create a mesh to plot the decision boundary
    h = 0.02  # step size in the mesh
    x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
    y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Predict on the meshgrid
    Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    # Plot the decision boundary
    plt.figure(figsize=(8, 6))
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot the training points
    plt.scatter(x[:, 0], x[:, 1], c=y, cmap=plt.cm.coolwarm)
    plt.xlabel("Total Day Charge")
    plt.ylabel("Total Eve Charge")
    plt.title("KNN Decision Boundary")
    plt.show()


if __name__ == "__main__":
    main()
