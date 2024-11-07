class ArgumentsParser:
    """
    Class for parsing command-line arguments.

    The `ArgumentsParser` class provides a method to parse command-line arguments
    and convert them into a dictionary of options, supporting both options with
    single values and repeated options (like `--path`).
    """

    def parse(self, args) -> dict:
        """
        Parses the provided command-line arguments into a dictionary of options.

        This method iterates through the list of arguments, identifies options prefixed
        by `--`, and captures their corresponding values. If an option can have multiple
        values (e.g., `--path`), it stores them in a list.

        Args:
            args (list): A list of command-line arguments to be parsed.

        Returns:
            dict: A dictionary where keys are option names (without `--`) and values are
                  option values or lists of values for options that appear multiple times.
        """
        options = {}
        i = 0

        while i < len(args):
            arg = args[i]
            if arg.startswith("--"):
                option_name = arg[2:]
                option_value = None

                if i + 1 < len(args) and not args[i + 1].startswith("--"):
                    option_value = args[i + 1]
                    i += 1
                if option_name == 'path':
                    if option_name not in options:
                        options[option_name] = [option_value]
                    else:
                        options[option_name].append(option_value)
                else:
                    options[option_name] = option_value
            i += 1
        return options
