"""
Utilities to be used along with the deep model
"""
from typing import Union

import torch
from torch import nn


def compute_accuracy(pred_sequences, labels: torch.Tensor) -> float:
    """Compute the accuracy given the prediction logits and the ground-truth labels

    Args:
        pred_sequences: token sequence to be evaluated
        labels: correct sequence
    Returns:
        accuracy: The accuracy of the predicted logits
                   (number of correct predictions / total number of examples)
    """
    batch_accuracy = 0.0
    ############################################################################
    # Student code begin
    ############################################################################
    correct = []
    for i in range(len(labels)):
        pred = eval(pred_sequences[i])
        label = eval(labels[i])
        if pred == label:
            correct.append(pred)
    batch_accuracy = len(correct) / len(labels)
    ############################################################################
    # Student code end
    ############################################################################

    return batch_accuracy


def compute_loss(
    model: nn.Module,
    model_output: torch.Tensor,
    target_labels: torch.Tensor,
    is_normalize: bool = True,
) -> torch.Tensor:
    """
    Computes the loss between the model output and the target labels

    Args:
    -   model: a model (which inherits from nn.Module)
    -   model_output: the raw scores output by the net
    -   target_labels: the ground truth class labels
    -   is_normalize: bool flag indicating that loss should be divided by the batch size
    Returns:
    -   the loss value
    """
    loss = None

    ############################################################################
    # Student code begin
    ############################################################################

    loss = model.loss_criterion(model_output, target_labels)
    if is_normalize:
        batch_size = list(target_labels.shape)[0]
        loss /= batch_size

    ############################################################################
    # Student code end
    ############################################################################

    return loss


def save_trained_model_weights(
    model: nn.Module, out_dir: str
) -> None:
    """Saves the weights of a trained model along with class name

    Args:
    -   model: The model to be saved
    -   out_dir: The path to the folder to store the save file in
    """
    class_name = model.__class__.__name__
    state_dict = model.state_dict()

    save_dict = {"class_name": class_name, "state_dict": state_dict}
    torch.save(save_dict, f"{out_dir}/trained_{class_name}_final.pt")
