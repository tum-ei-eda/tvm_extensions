import sys

from tvm.driver.tvmc.main import _main, register_parser
from tvm.driver.tvmc.compiler import drive_compile, add_compile_arguments

from disable_legalize import OptionallyDisableLegalize
import uma_loader


def drive_tumeda_compile(args):
    with OptionallyDisableLegalize(args.disable_legalize):
        drive_compile(args)
    return 0


@register_parser
def add_tumeda_compile_parser(subparsers, parser, json_params):
    """Include parser for 'tumeda_compile' subcommand"""
    parser = subparsers.add_parser("tumeda_compile", help="compile a model with tumeda extensions.")
    parser.set_defaults(func=drive_tumeda_compile)
    group = parser.add_argument_group("tumeda extension options")
    group.add_argument(
        "--disable-legalize", action="store_true", help="apply a custom transformation to disable legalization passes."
    )
    group.add_argument(
        "--uma-backends", action="append", default=[], help="add directory to search for UMA backends."
    )

    # Need to manually parse UMA targets so that their target options can be generated automatically.
    for i, arg in enumerate(sys.argv):
        if arg == "--uma-backends" and i + 1 < len(sys.argv):
            umadir = sys.argv[i + 1]
            sys.path.insert(0, umadir)
            sys.path.insert(0, umadir + "/uma_backends")
    uma_loader.init()

    add_compile_arguments(parser, json_params)



def main():
    args = [arg.replace("compile", "tumeda_compile") for arg in sys.argv[1:]]
    sys.exit(_main(args))


if __name__ == "__main__":
    main()
