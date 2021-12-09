"""
python functionsplatform.py COMMAND [--OPTIONS|-O]

COMMANDs:
  create
  list
  delete
  trigger
  logs
  list-instances
  lookup-instance

OPTIONs:
  --help        global help
  --verbose
  --version
  --show-help   per-command help

Example:
  functionsplatform create --http-verb=GET --http-path=/api/cats  --code-file handler.py --name some_name
  functionsplatform list [--filter=glob_patter]
  functionsplatform logs some_instance_id
"""

import argparse
import requests
import sys
import pprint
import os

import uuid

import fnmatch

__version__ = "0.1.0"


def create_function(platform_uri, args_string):
    parser = argparse.ArgumentParser(usage="%(prog)s create [options]")
    parser.add_argument("--name", type=str)
    parser.add_argument("-P", "--http-path", type=str)
    parser.add_argument("-X", "--http-verb", type=str)
    parser.add_argument("-f", "--code-file", type=str)
    parser.add_argument("--show-help", action="store_true")
    args = parser.parse_args(args_string)
    if args.show_help:
        parser.pprint.pprint_help()
        sys.exit()
    
    event_type = f"http|{args.http_verb.upper()}|{args.http_path}"

    payload = {
        "event_type": event_type,
        "function_code": open(args.code_file).read(),
        "function_name": args.name
    }

    response = requests.post(os.path.join(platform_uri, "functions"), json=payload)
    pprint.pprint(response.json())


def delete_function(platform_uri, args_string):
    parser = argparse.ArgumentParser(usage="%(prog)s delete [options]")
    parser.add_argument("name", type=str)
    parser.add_argument("--show-help", action="store_true")
    args = parser.parse_args(args_string)
    if args.show_help:
        parser.pprint.pprint_help()
        sys.exit()
    
    response = requests.delete(os.path.join(platform_uri, f"functions/{args.name}"))
    pprint.pprint(response.json())


def list_functions(platform_uri, args_string):
    parser = argparse.ArgumentParser(usage="%(prog)s list [options]")
    parser.add_argument("--show-help", action="store_true")
    parser.add_argument("--filter", type=str)
    args = parser.parse_args(args_string)
    if args.show_help:
        parser.pprint.pprint_help()
        sys.exit()

    response = requests.get(os.path.join(platform_uri, "functions"))
    if not args.filter:
        pprint.pprint(response.json())
    else:
        body = response.json()
        matching_keys = fnmatch.filter(body.keys(), args.filter)
        pprint.pprint({key: body[key] for key in matching_keys})


def trigger_function(platform_uri, args_string):
    parser = argparse.ArgumentParser(usage="%(prog)s trigger [options]")
    parser.add_argument("-P", "--http-path", type=str)
    parser.add_argument("-X", "--http-verb", type=str)
    parser.add_argument("-d", "--http-body", default="{}", type=str)
    parser.add_argument("-H", "--http-headers", type=str)
    parser.add_argument("--show-help", action="store_true")
    args = parser.parse_args(args_string)
    if args.show_help:
        parser.pprint.pprint_help()
        sys.exit()

    payload = {
        "http_header": f"{args.http_headers}\nX-Correlation-Id: test-{uuid.uuid4()}",
        "http_body": args.http_body,
        "http_path": args.http_path,
        "http_verb": args.http_verb.upper()
    }

    response = requests.post(os.path.join(platform_uri, "functions/trigger"), json=payload)
    pprint.pprint(response.json())


def list_instances(platform_uri, args_string):
    parser = argparse.ArgumentParser(usage="%(prog)s list-instances [options]")
    parser.add_argument("--show-help", action="store_true")
    args = parser.parse_args(args_string)
    if args.show_help:
        parser.pprint.pprint_help()
        sys.exit()
    
    response = requests.get(os.path.join(platform_uri, f"functions/instances"))
    pprint.pprint(response.json())


def lookup_instance(platform_uri, args_string):
    parser = argparse.ArgumentParser(usage="%(prog)s lookup-instance [options]")
    parser.add_argument("instance_id", metavar="instance-id", type=str)
    parser.add_argument("--show-help", action="store_true")
    args = parser.parse_args(args_string)
    if args.show_help:
        parser.pprint.pprint_help()
        sys.exit()
    
    response = requests.get(os.path.join(platform_uri, f"functions/instances/{args.instance_id}"))
    pprint.pprint(response.json())


def show_function_logs(platform_uri, args_string):
    parser = argparse.ArgumentParser(usage="%(prog)s logs [options]")
    parser.add_argument("instance_id", metavar="instance-id", type=str)
    parser.add_argument("--show-help", action="store_true")
    args = parser.parse_args(args_string)
    if args.show_help:
        parser.pprint.pprint_help()
        sys.exit()

    response = requests.get(os.path.join(platform_uri, f"functions/instances/{args.instance_id}/logs"))
    pprint.pprint(response.json())




DISPATCH = {
    "create": create_function,
    "list": list_functions,
    "delete": delete_function,
    "trigger": trigger_function,
    "logs": show_function_logs,
    "list-instances": list_instances,
    "lookup-instance": lookup_instance
}


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["create", "list", "delete", "trigger", "logs", "lookup-instance", "list-instances"], nargs="?")
    parser.add_argument("--platform-uri", default="http://localhost:8000", help="URI should also contain the schema, for example 'http://'")
    parser.add_argument('-v',
                       '--verbose',
                       action='store_true',
                       help='increase verbosity')
    parser.add_argument("--version", action="store_true")
    args, unkown = parser.parse_known_args()

    if args.version:
        pprint.pprint(__version__)
        sys.exit()

    if args.command:
        DISPATCH[args.command](args.platform_uri, unkown)




if __name__ == "__main__":
    main(sys.argv)