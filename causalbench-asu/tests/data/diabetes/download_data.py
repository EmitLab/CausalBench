"""
Download Diabetes dataset from sklearn
"""

from sklearn.datasets import load_diabetes


def download_diabetes():
    # Load the dataset
    diabetes = load_diabetes(as_frame=True)

    # Combine features and target
    data = diabetes.frame

    # Save to CSV
    data.to_csv("diabetes_data.csv", index=False)

    print(f"Dataset saved with {len(data)} samples")
    print(f"Features: {diabetes.feature_names}")
    print("Target: target (diabetes progression)")


if __name__ == "__main__":
    download_diabetes()
