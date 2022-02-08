# python3.7
"""Implements an identity transformation, which can be used as a placeholder."""

from .base_transformation import BaseTransformation

__all__ = ['Identity']


class Identity(BaseTransformation):
    """Applies no transformation by directly returning the input."""

    def __init__(self):
        super().__init__(support_dali=True)

    def _CPU_forward(self, data):
        return data

    def _DALI_forward(self, data):
        return data
