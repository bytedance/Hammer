# python3.7
"""Dumps available arguments of all commands (configurations).

This file parses the arguments of all commands provided in `configs/` and dump
the results as a json file. Each parsed argument includes the name, argument
type, default value, and the help message (description). The dumped file looks
like

{
    "command_1": {
        "type": "object",
        "properties": {
            "arg_group_1": {
                "type": "object",
                "properties": {
                    "arg_1": {
                        "type":  # int / float / bool / str / json-string /
                                 # index-string
                        "is_recommended":  # true / false
                        "default":
                        "description":
                    },
                    "arg_2": {
                        "type":
                        "is_recommended":
                        "default":
                        "description":
                    }
                }
            },
            "arg_group_2": {
                "type": "object",
                "properties": {
                    "arg_3": {
                        "type":
                        "is_recommended":
                        "default":
                        "description":
                    },
                    "arg_4": {
                        "type":
                        "is_recommended":
                        "default":
                        "description":
                    }
                }
            }
        }
    },
    "command_2": {
        "type": "object",
        "properties: {
            "arg_group_1": {
                "type": "object",
                "properties": {
                    "arg_1": {
                        "type":
                        "is_recommended":
                        "default":
                        "description":
                    }
                }
            }
        }
    }
}
"""

import sys
import json

from configs import CONFIG_POOL

PARAM_TYPE_TO_VALUE_TYPE = {
    'IntegerParamType': 'int',
    'FloatParamType': 'float',
    'BooleanParamType': 'bool',
    'StringParamType': 'str',
    'IndexParamType': 'index-string',
    'JsonParamType': 'json-string'
}


def parse_args_from_config(config):
    """Parses available arguments from a configuration class.

    Args:
        config: The configuration class to parse arguments from, which is
            defined in `configs/`. This class is supposed to derive from
            `BaseConfig` defined in `configs/base_config.py`.
    """
    def _dummy_func():
        """A dummy function used to parse decorator."""

    args = dict()
    func = config.add_options_to_command(config.get_options())(_dummy_func)
    recommended_opts = config.get_recommended_options()
    for opt in reversed(func.__click_params__):
        if opt.group.title not in args:
            args[opt.group.title] = dict(type='object', properties=dict())
        args[opt.group.title]['properties'][opt.name] = dict(
            type=PARAM_TYPE_TO_VALUE_TYPE[opt.type.__class__.__name__],
            default=opt.default,
            is_recommended=opt.name in recommended_opts,
            description=opt.help
        )
    return args


def dump(configs, save_path):
    """Dumps available arguments from given configurations to target file.

    Args:
        configs: A list of configurations, each of which should be a
            class derived from `BaseConfig` defined in `configs/base_config.py`.
        save_path: The path to save the dumped results.
    """
    args = dict()
    for config in configs:
        args[config.name] = dict(type='object',
                                 properties=parse_args_from_config(config))
    with open(save_path, 'w') as f:
        json.dump(args, f, indent=4)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(f'Usage: python {sys.argv[0]} SAVE_PATH')
    dump(CONFIG_POOL, sys.argv[1])
