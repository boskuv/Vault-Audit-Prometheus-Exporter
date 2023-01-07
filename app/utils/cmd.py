from operator import contains
import optparse
import sys


parser = optparse.OptionParser(usage="Usage: %prog [options]")

parser.add_option("-c", "--config", type=str, help="path to configuration file") # TODO: default value

possible_args = [option.dest for option in parser._get_all_options()[1:]]
passed_args = [arg.lstrip("-") for arg in sys.argv]


def resolve_cmd_args():
    if len(sys.argv) == 1 or len(set(possible_args).intersection(passed_args)) == 0:
        parser.print_help()
        sys.exit()

    options, _ = parser.parse_args()
    return options


__all__ = ["resolve_cmd_args"]