# CausalBench

The up-to-date documentation regarding usage and features of CausalBench can be found at [docs.causalbench.org](docs.causalbench.org).

## Overview

CausalBench is a flexible, fair, and easy-to-use evaluation platform designed to advance research in causal learning. It facilitates scientific collaboration by providing a suite of tools for novel algorithms, datasets, and metrics. Our mission is to promote scientific objectivity, reproducibility, fairness, and awareness of bias in causal learning research. CausalBench serves as a comprehensive benchmarking resource, impacting a broad range of scientific and engineering disciplines.

## Features

-   **Transparent and Fair Evaluation**: Ensures unbiased and transparent benchmarking processes.
-   **Facilitation of Scientific Collaboration**: Encourages the sharing and development of novel algorithms, datasets, and metrics.
-   **Scientific Objectivity**: Promotes objective assessment and comparison of causal learning methods.
-   **Reproducibility**: Supports the reproducibility of research results, a cornerstone of scientific integrity.
-   **Awareness of Bias**: Highlights and addresses biases in causal learning research.

## Services Provided

1.  **Benchmarking Data**: A repository of diverse datasets specifically curated for evaluating causal learning algorithms.
2.  **Algorithm Evaluation**: Tools and frameworks for testing and comparing the performance of causal learning algorithms.
3.  **Model Benchmarking**: Standards and protocols for assessing the efficacy of different causal models.
4.  **Metric Evaluation**: A collection of metrics tailored for comprehensive evaluation of causal learning techniques.

## Impact

CausalBench meets the needs of various scientific and engineering disciplines by providing essential resources and standards for evaluating causal learning methods. This platform helps researchers to:

-   Collaborate and share advancements in causal learning.
-   Ensure their work meets high standards of scientific rigor and fairness.
-   Access a centralized repository of resources for benchmarking and evaluation.

## Getting Started

To start using CausalBench, follow these steps:

1.  **Installation**: Instructions for installing CausalBench can be found [here](#).
2.  **Documentation**: Comprehensive documentation for CausalBench, including API references and tutorials, is available [here](#).
3.  **Contributing**: Information on how to contribute to the CausalBench project can be found [here](#).

## Contributing

CausalBench is an open-source project and welcomes contributions from the community. Whether you are interested in developing new features, fixing bugs, or improving documentation, your input is valuable. Please refer to our [contribution guidelines](#) for more details.

## License

CausalBench is licensed under the MIT License. See the [LICENSE](#) file for more information.

## Contact

For questions, feedback, or further information, please contact us at support@causalbench.org.

## Acknowledgments
This work is supported by NSF grant 2311716, "CausalBench: A Cyberinfrastructure
for Causal-Learning Benchmarking for Efficacy, Reproducibility, and Scientific
Collaboration".



## Support Benchmark Context
CausalBench is structured to support different machine learning tasks and dataset types. With user contribution, the supported context will be expanded, currently, these models and tasks are provided.    

| Dataset               | File                 |
|-----------------------|----------------------|
| Abalone               | data, static graph   |
| Adult                 | data, static graph   |
| Time series simulated | data, temporal graph |

| Model      | Task     |
|------------|----------|
| PC         | Static   |
| GES        | Static   |
| VAR-LiNGAM | Temporal |
| PCMCI      | Temporal |


| Metric    | Task     |
|-----------|----------|
| Accuracy  | Static   |
| F1        | Static   |
| Precision | Static   |
| Recall    | Static   |
| SHD       | Static   |
| Accuracy  | Temporal |
| F1        | Temporal |
| Precision | Temporal |
| Recall    | Temporal |
| SHD       | Temporal |
