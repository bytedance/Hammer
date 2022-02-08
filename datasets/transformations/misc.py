# python3.7
"""Helper functions for data transformation."""

try:
    import nvidia.dali.fn as fn
    import nvidia.dali.types as types
except ImportError:
    fn = None

__all__ = ['switch_between', 'FunctionOp']


def switch_between(cond, cond_true, cond_false, use_dali=False):
    """Switches between two transformation nodes for data pre-processing.

    Args:
        cond: Condition to switch between two alternatives.
        cond_true: The returned value if the condition fulfills.
        cond_false: The returned value if the condition fails.
        use_dali: Whether the nodes are from DALI pre-processing pipeline.
            (default: False)

    Returns:
        One of `cond_true` and `cond_false`, depending on `cond`.
    """
    if use_dali and fn is None:
        raise NotImplementedError('DALI is not supported! '
                                  'Please install first.')

    if not use_dali:
        return cond_true if cond else cond_false

    # Record whether any input (cond_true/cond_false) is not a list. If that is
    # the case, the returned value will be a single node. Otherwise, the
    # returned value will also be a list of nodes.
    is_input_list = True
    if not isinstance(cond_true, (list, tuple)):
        is_input_list = False
        cond_true = [cond_true]
    if not isinstance(cond_false, (list, tuple)):
        is_input_list = False
        cond_false = [cond_false]
    assert len(cond_true) == len(cond_false)

    cond = fn.cast(cond, dtype=types.BOOL)
    outputs = []
    for sample_true, sample_false in zip(cond_true, cond_false):
        outputs.append(sample_true * cond + sample_false * (cond ^ True))
    return outputs if is_input_list else outputs[0]


class FunctionOp(object):
    """Contains the class to turn a function as an operator.

    DALI supports creating a data node, which is populated with data from an
    external source function. This function should be callable via accepting one
    positional argument. This class is particularly designed to turn a function,
    with default settings, into a DALI compatible operator. Please refer to
    `nvidia.dali.fn.external_source()` for more details.

    More concretely, a function `f(a, b)` with desired arguments `a=1, b=2` can
    be wrapped with

    ```
    op = FunctionOp(f, a=1, b=2)
    ```

    Then, it can be used with

    ```
    dali_node = fn.external_source(source=op,
                                   parallel=True,
                                   prefetch_queue_depth=32,
                                   batch=False)
    ```

    OR, it can be directly called with

    ```
    result = op()
    ```
    """

    def __init__(self, function, **kwargs):
        """Initializes with the function to wrap and the default arguments."""
        self.function = function
        self.kwargs = kwargs

    def __call__(self, _dali_arg=None):
        return self.function(**self.kwargs)
