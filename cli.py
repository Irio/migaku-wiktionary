import argparse

import commands

COMMANDS = {
    "download": commands.download,
    "convert": commands.convert,
}

parser = argparse.ArgumentParser(
    description="Parse Wiktionary dump into a Migaku Dictionary."
)
parser.add_argument(
    "command",
    metavar="command",
    choices=list(COMMANDS.keys()),
    help=f"Choose from {', '.join(COMMANDS.keys())}",
)
parser.add_argument(
    "--lang",
    nargs="?",
    help="ISO 639-1 language code of the dump to download e.g., de",
)
parser.add_argument(
    "--xml",
    nargs="?",
    help="Path for the XML to be parsed e.g., /tmp/dewiktionary-latest-pages-meta-current.xml",
)
parser.add_argument(
    "--destination",
    default="/tmp",
    help=f"Folder where the output will be saved (default: %(default)s)",
)

args = parser.parse_args()

selected_command = COMMANDS[args.command]
if args.command == "download":
    selected_command(args.lang, args.destination)
elif args.command == "convert":
    selected_command(args.xml, args.destination)
