"""
Download California Housing dataset from sklearn
"""

from sklearn.datasets import fetch_california_housing


def download_california_housing():
    # Load the dataset
    california = fetch_california_housing(as_frame=True)

    # Combine features and target
    data = california.frame

    # Save to CSV
    data.to_csv("california_housing_data.csv", index=False)

    print(f"Dataset saved with {len(data)} samples")
    print(f"Features: {california.feature_names}")
    print(f"Target: {california.target_names}")


if __name__ == "__main__":
    download_california_housing()
