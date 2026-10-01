# Classical ML Basics Notes

## Learning types
Supervised learning uses labeled examples. Unsupervised learning finds structure without labels. Reinforcement learning optimizes behavior from rewards and environment interaction.

## Generalization
Underfitting means the model is too simple for the pattern; overfitting means it models training-specific noise. Bias-variance thinking helps reason about this trade-off. Use appropriate train/validation/test splits and avoid leakage.

## Models
Linear regression predicts continuous values. Logistic regression models classification probabilities. Trees partition feature space; ensembles such as random forests and gradient boosting improve robustness. XGBoost is a widely used gradient-boosting implementation. SVMs maximize a margin. K-means clusters by distance to centroids. PCA projects data into lower-dimensional directions of variance.

## Neural networks
Backpropagation computes gradients through the network so optimization can update parameters. CNNs exploit spatial locality; RNN/LSTM architectures model sequences and maintain state, although transformer architectures dominate many modern language workloads.

## Evaluation
Classification metrics include precision, recall, F1, ROC-AUC, and PR-AUC. Select metrics based on the cost of false positives and false negatives.

## MLOps
Track model versions, datasets, features, experiments, deployment metadata, drift, and performance. A model is a production component, not just a training artifact.

## Practice
Train baseline linear/logistic/tree models, compare metrics, demonstrate overfitting, perform PCA, cluster a dataset, and design a model registry/drift-monitoring workflow.