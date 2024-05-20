"""
The module provids functionality related to different plots used 
in the repository.
"""

import pandas as pd
import numpy as np
import shap
import seaborn as sns 
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

from sklearn.metrics import (
    confusion_matrix,
    precision_recall_fscore_support,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score,
    roc_auc_score
)
from sklearn.model_selection import learning_curve
from sklearn.preprocessing import label_binarize
from mlxtend.plotting import plot_confusion_matrix
from typing import Union, List, Any


def plot_confusion_matrix_plt(
    true_labels: Union[pd.Series, np.ndarray, list],
    pred_labels: Union[pd.Series, np.ndarray, list],
    problem: str = 'binary',
    class_names: Union[None, np.ndarray, list] = None,
    figsize: tuple = (4,4), # TODO: may be create a seprate parameter for it (4,4)?
    sns_style: str = 'darkgrid',
    return_figure: bool = True
) -> Union[None, Figure]:
    """
    Plot confusion matrix for both bianry and multiclassification problems
    using predicted class labels (not probabilities!).

    Parameters
    ----------
    true_labels: 
        Known labels.
    pred_labels:
        Predicted labels.
    problem: str
        Binary or multiclass.
    class_names: np.ndarray
        Class names (usually used from sklearn.LabelEncoder).
    figsize: tuple
        Plot figure size.
    sns_style: str
        Seaborn plot style.
    return_figure: bool
        If the plot should be returned.
    
    Returns
    -------
    None or Figure
        Confusion matrix plot.
    """
    _confusion_matrix = confusion_matrix(true_labels, pred_labels)
    sns.set_style(sns_style)


    if problem == 'binary':
        cm_plot, figure = plot_confusion_matrix(
            _confusion_matrix,
            show_normed=True,
            figure=plt.figure(figsize=figsize)
        )

    elif problem == 'multiclass':
        cm_plot, figure = plot_confusion_matrix(
            _confusion_matrix,
            show_normed=True,
            figure=plt.figure(figsize=figsize),
            class_names=class_names
        )

    else:
        raise ValueError('Problem can be either "binary" or "multiclass"!')

    if return_figure:
        return cm_plot


def plot_class_proba_distribution(
    X: Union[pd.DataFrame, np.ndarray],
    y: Union[pd.Series, np.ndarray],
    model: Any,
    problem: str = 'binary',
    figsize: tuple = (12,6),
    sns_style: str = 'darkgrid',
    title: str = "Score Distribution",
    return_figure: bool = True
) -> Union[None, Figure]:
    """
    Plot predicted probability distribution per class.

    Parameters
    ----------
    X: pd.DataFrame
        Matrix of features (train or test).
    y: pd.Series or np.ndarray
        Labels (train or test).
    model: Any
        Fitted ML model.
    problem: str
        Problem type (either binary or multiclass).
    figsize: tuple
        Figure size.
    sns_style: str
        Seaborn plot style.
    title: str
        Plot title.
    return_figure: bool
        If a plot should be returned as figure (for saving the figure).

    Returns
    -------
    None or Figure
        Plot score distribution plot for class 0 and 1.
    """
    if problem == 'binary':
        class_samples = {
            class_label: X[y == class_label]
            for class_label in set(y)
        }
        class_predicted_proba = {
            class_label: [x[1] for x in model.predict_proba(class_sample)]
            for class_label, class_sample in class_samples.items()
        }
    elif problem == 'multiclass':
        pass
        # TODO: define multiclass logic
        # may be define logic for n_classes overlap (no more than 3)
    
    else:
        raise ValueError('Problem can be either "binary" or "multiclass"!')
        
    plt.figure(figsize=figsize)
    sns.set_style(sns_style)
    for class_label, class_proba in class_predicted_proba.items():
        fig = sns.distplot(class_proba, label=class_label)
    plt.legend(loc="best")
    fig.set(xlabel="Scores")
    fig.set_title(title)

    if return_figure:
        return fig.get_figure()


def plot_roc_graph(
    true_labels: Union[pd.Series, np.ndarray, list],
    pred_proba: np.ndarray,
    problem: str = 'binary',
    average_type: str = 'macro',
    class_names: Union[None, np.ndarray, list] = None,
    figsize: tuple = (12,6),
    sns_style: str = 'darkgrid',
    return_figure: bool = True
) -> Union[None, Figure]:
    """
    Plot ROC-AUC curve for both multiclass and binary problems.

    Parameters
    ----------
    true_labels: pd.Series
        Known labels.
    pred_proba: np.ndarray
        Predicted probabilities (for all classes).
    problem: str
        Binary or multiclass.
    average_type: str
        How resulting Precision and Recall will be calculated.
        Can be either 'macro', 'micro', 'weighted' or 'samples'.
    class_names: list
        Use class names instead of values.
    figsize: tuple
        Figure size.
    sns_style: str
        Seaborn plot style.
    return_figure: bool
        If a plot should be returned as figure (for saving the figure).

    Returns
    -------
    None or Figure
        Plot ROC-AUC plots, both averaged and per class.
    """
    if problem == 'multiclass':
        # binarize the labels 
        true_labels_bin = label_binarize(true_labels, classes=np.unique(true_labels))
        
        # Compute average ROC-AUC 
        roc_auc = roc_auc_score(true_labels_bin, pred_proba, average=average_type)

        # plot average ROC-AUC
        plt.figure(figsize=figsize)
        sns.set_style(sns_style)
        plt.subplot(1, 2, 1)
        fpr_mean, tpr_mean, _ = roc_curve(true_labels_bin.ravel(), pred_proba.ravel())
        roc_plot = plt.plot(fpr_mean, tpr_mean, label=f'{average_type}-average ROC (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], 'k--', linewidth=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'{average_type.capitalize()} ROC Curve')
        plt.legend(loc="lower right")

        # plot ROC-AUC per class
        plt.subplot(1, 2, 2)
        for i in range(len(np.unique(true_labels))):
            fpr, tpr, _ = roc_curve(true_labels_bin[:, i], pred_proba[:, i])
            roc_auc = auc(fpr, tpr)
            roc_plot = plt.plot(fpr, tpr, label=f'{class_names[i]} (AUC = {roc_auc:.2f})')

        plt.plot([0, 1], [0, 1], 'k--', linewidth=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve per Class')
        plt.legend(loc="lower right")
        plt.tight_layout()

    elif problem == 'binary':
        fpr, tpr, threshold = roc_curve(true_labels, pred_proba[:, 1])
        roc_auc = auc(fpr, tpr)
        plt.figure(figsize=figsize)
        sns.set_style(sns_style)
        roc_plot = plt.plot(
            fpr, tpr, color="darkorange", lw=2, label=f"ROC-AUC (area = {roc_auc:.2f})"
        )
        plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title('ROC Curve')
        plt.legend(loc="lower right")

    else:
        raise ValueError('Problem can be either "binary" or "multiclass"!')

    if return_figure:
        return roc_plot[0].get_figure()


def plot_precision_recall_curve(
    true_labels: Union[pd.Series, np.ndarray, list],
    pred_proba: np.ndarray,
    problem: str = 'binary',
    average_type: str = 'macro',
    class_names: Union[None, np.ndarray, list] = None,
    figsize: tuple = (12,6),
    sns_style='darkgrid',
    return_figure: bool = True,
) -> Union[None, Figure]:
    """
    Plot Precision-Recall Curve for both multiclass and binary problems.

    Parameters
    ----------
    true_labels: pd.Series
        Known labels.
    pred_proba: np.ndarray
        Predicted probabilities (for all classes).
    problem: str
        'binary' or 'multiclass'.
    average_type: str
        Either 'macro' or 'micro'.
    class_names: list
        Use class names instead of values.
    sns_style: str
        Seaborn plot style.
    figsize: tuple
        Figure size.
    return_figure: bool
        If a plot should be returned as figure (for saving the figure).

    Returns
    -------
    None or Figure
        Plot Precision-Recall curves plots, both averaged and per class.
    """
    if problem == 'multiclass':
        true_labels_bin = label_binarize(true_labels, classes=np.unique(true_labels))
        precision = dict()
        recall = dict()

        plt.figure(figsize=figsize)
        sns.set_style(sns_style)
        plt.subplot(1, 2, 1)
        for i in range(np.unique(true_labels).shape[0]):
            precision[i], recall[i], _ = precision_recall_curve(true_labels_bin[:, i], pred_proba[:, i])
            pr_auc = auc(recall[i], precision[i])
            pr_plot = plt.plot(recall[i], precision[i], lw=2, label=f'{class_names[i]} (PR-AUC = {pr_auc:.2f})')
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.title("Precision Recall Curve")
            plt.legend(loc="lower right")
            plt.grid(True)

        # micro/macro option
        if average_type == 'macro':
            precision["macro"], recall["macro"], _ = precision_recall_curve(true_labels_bin.ravel(), pred_proba.ravel())
            pr_auc = auc(recall["macro"], precision["macro"])
            plt.subplot(1, 2, 2)
            pr_plot = plt.plot(recall["macro"], precision["macro"], lw=2, label=f'PR-AUC = {pr_auc:.2f})')
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.title("Macro Precision Recall Curve")
            plt.legend(loc="lower right")
            plt.grid(True)

        # TODO: define logic for micro
 
    elif problem == 'binary':
        precision, recall, _ = precision_recall_curve(true_labels, pred_proba[:, 1])
        pr_auc = auc(recall, precision)

        plt.figure(figsize=figsize)
        pr_plot = plt.plot(
            recall, precision, color="b", lw=2, label=f"PR-AUC = {pr_auc:.2f}"
        )
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("Precision-Recall Curve")
        plt.legend(loc="lower right")
        plt.grid(True)

    else:
        raise ValueError('Problem can be either "binary" or "multiclass"!')

    if return_figure:
        return pr_plot[0].get_figure()


def plot_feature_correlation(
    corr_df: pd.DataFrame,
    figsize: tuple = (12,6),
    title: str = 'Features Correlation',
    return_figure: bool = True
) -> Union[None, Figure]:
    """
    Plot correlation matrix between the features.

    Parameters
    ----------
    corr_df: pd.DataFrame
        Correlation betweien the features.
    figsize: tuple
        Figure size.
    title: str
        Plot title.
    return_figure: bool
        If a plot should be returned as figure (for saving the figure).

    Returns 
    -------
    None or Figure
        Plot feature correlation plot as a heatmap.
    """
    plt.figure(figsize=figsize)
    correlation_plot = sns.heatmap(corr_df, annot=True, cmap="coolwarm", fmt=".3f")
    plt.title(title)
    if return_figure:
        return correlation_plot.get_figure()
    

def plot_with_std(n_samples: int, data, return_figure: bool = True, **kwargs):
    """Helper function for 'plot_learning_curve'"""
    mu, std = data.mean(1), data.std(1)
    lines = plt.plot(n_samples, mu, '-', **kwargs)
    plot = plt.fill_between(n_samples, mu - std, mu + std, edgecolor='none', facecolor=lines[0].get_color(), alpha=0.2)
    if return_figure:
        return plot.get_figure()


def plot_learning_curve(
    model: Any,
    X_train: Union[pd.DataFrame, np.ndarray],
    y_train: Union[pd.Series, np.ndarray],
    cv_type: Any,
    scorer: str = 'roc_auc',
    train_data_split: int = 20,
    figsize: tuple = (12,6),
    shuffle: bool = True,
    random_state: int = 23,
    n_jobs: int = -1,
    fit_params: Any = None,
    sns_style: str = 'darkgrid',
    return_figure: bool = True
) -> Union[None, Figure]:
    """
    Plot learning curves for both binary and multiclass problems.

    Parameters
    ----------
    model: Any
        Model to validate.
    X_train: pd.DataFrame
        Training data.
    y_train: pd.Series
        Training labels.
    cv_type: Any
        Cross-Validation type (e.g. 'sklearn.model_selection.StratifiedKFold').
    scorer: str
        Metric type. For multiclassification problems use respective metrics, otherwise none will be returned.
    train_data_split: int
        How many splits defien for the training data (e.g. 5, 10, 15, ...).
    figsize: tuple
        Figure size.
    shuffle: bool
        If shuffle should be applied in cross-validation.
    random_state: int
        Random state parameter.
    n_jobs: int
        How many CPU units to use for computing.
    fit_params:
        TODO: describe
    sns_style: str
        Seaborn plot style.
    return_figure: bool
        If a plot should be returned as Figure (for saving the figure).
    
    Returns 
    -------
    None or Figure
        Plot learning curves.
    """
    train_sizes = np.linspace(0.05, 1, train_data_split)
    n_train, train_curve, val_curve = learning_curve(
      estimator=model, X=X_train, y=y_train,
      cv=cv_type, scoring=scorer, train_sizes=train_sizes,
      n_jobs=n_jobs, shuffle=shuffle, random_state=random_state, fit_params=fit_params
    )
    sns.set_style(sns_style)
    plt.figure(figsize=figsize)
    plot = plot_with_std(n_train, train_curve, label='Training Scores', return_figure=return_figure)
    plot = plot_with_std(n_train, val_curve, label='Validation Scores', return_figure=return_figure)
    plt.xlabel('Training Set Size')
    plt.ylabel(scorer)
    plt.title('Learning Curves (Train)')
    plt.legend(loc="lower right")
    plt.grid(True)
    if return_figure:
        return plot.get_figure()


# SHAP
# TODO: currently not working properly
# bianry -> issue with colors and need to select class
# mutliclass -> cannot work with more than one dimention
# check if I can fix it
def plot_shap_beeswarm(
    shap_values: List[np.ndarray],
    feature_names: Union[None, np.ndarray, list] = None,
    class_names: Union[None, np.ndarray, list] = None,
    figsize: tuple = (12,6),
    show: bool = False,
    return_figure: bool = True
) -> Union[None, Figure]:
    """
    Plot SHAP beeswarm plot.

    Parameters
    ----------
    shap_values: 
        TODO: describe
    figsize: tuple
        Figure size.
    show: bool
        If we need to show the plot.
    return_plot: bool
        If we need to return the plot.

    Returns
    -------
    None or Figure
        Plot SHAP beeswarm plot.
    """
    plt.figure(figsize=figsize)
    beeswarm_plot, ax = plt.gcf(), plt.gca()
    shap.summary_plot(
        shap_values, plot_type='dot', plot_size=(10,4),
        show=False, feature_names=feature_names, class_names=class_names
    )
    ax.set_title('SHAP Importance (Beeswarm plot)', fontsize=12)
    if return_figure:
        return beeswarm_plot


def plot_shap_bar(
    shap_values: List[np.ndarray],
    feature_names: Union[None, np.ndarray, list] = None,
    class_names: Union[None, np.ndarray, list] = None,
    figsize: tuple = (12,6),
    show: bool = False,
    return_figure: bool = True
) -> Union[None, Figure]:
    """
    Plot SHAP bar plot.

    Parameters
    ----------
    shap_values: 
        TODO: describe
    figsize: tuple
        Figure size.
    feature_names: np.ndarray
        Feature names. 
    class_names: np.ndarray
        Class names (usually used from sklearn.LabelEncoder).
    show: bool
        If we need to show the plot.
    return_figure: bool
        If we need to return the plot.

    Returns
    -------
    None or Figure
        Plot SHAP beeswarm plot.
    """
    plt.figure(figsize=figsize)
    bar_plot, ax = plt.gcf(), plt.gca()
    shap.summary_plot(
        shap_values, plot_type='bar', plot_size=(10,4),
        show=False, feature_names=feature_names, class_names=class_names
    )
    ax.set_title('SHAP Importance (Bar Plot)', fontsize=12)
    if return_figure:
        return bar_plot
