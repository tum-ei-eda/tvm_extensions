import sys

from tvm.driver.tvmc.main import _main, register_parser
from tvm.driver.tvmc.compiler import drive_compile, add_compile_arguments

from disable_legalize import OptionallyDisableLegalize


def drive_tumeda_compile(args):
    with OptionallyDisableLegalize(args.disable_legalize):
        drive_compile(args)
    return 0


@register_parser
def add_tumeda_compile_parser(subparsers, parser):
    """Include parser for 'tumeda_compile' subcommand"""
    parser = subparsers.add_parser("tumeda_compile", help="compile a model with tumeda extensions.")
    parser.set_defaults(func=drive_tumeda_compile)
    group = parser.add_argument_group("tumeda extension options")
    group.add_argument(
        "--disable-legalize", action="store_true", help="apply a custom transformation to disable legalization passes."
    )
    add_compile_arguments(parser)


def main():
    args = [arg.replace("compile", "tumeda_compile") for arg in sys.argv[1:]]
    sys.exit(_main(args))


if __name__ == "__main__":
    main()
