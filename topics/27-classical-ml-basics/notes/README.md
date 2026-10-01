# Classical ML Basics Notes

## Learning types
Supervised learning uses labeled examples. Unsupervised learning finds structure without labels. Reinforcement learning optimizes behavior from rewards and environment interaction.

## Generalization
Underfitting means the model is too simple; overfitting means it models training-specific noise. Use appropriate train/validation/test splits and avoid leakage.

## Models
Linear regression predicts continuous values. Logistic regression models classification probabilities. Trees partition feature space; random forests and gradient boosting combine trees. XGBoost is a gradient-boosting implementation. SVMs maximize a margin. K-means clusters by distance to centroids. PCA projects data into lower-dimensional directions of variance.

## Neural networks
Backpropagation computes gradients for parameter updates. CNNs exploit spatial locality; RNN/LSTM architectures model sequences, while transformers dominate many modern language workloads.

## Evaluation
Use precision, recall, F1, ROC-AUC, and PR-AUC according to the business cost of false positives and negatives.

## MLOps
Track model versions, datasets, experiments, deployment metadata, drift, and production performance.

## Practice
Train baseline linear/logistic/tree models, demonstrate overfitting, perform PCA, cluster a dataset, and design registry/drift monitoring.