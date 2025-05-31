import os
import sys

DEFAULT_IGNORE = {'node_modules', '.git', '__pycache__', '.venv', 'venv', 'env'}

def print_tree(start_path, prefix="", ignore_dirs=DEFAULT_IGNORE, max_level=None, current_level=0):
    try:
        items = sorted(os.listdir(start_path))
    except PermissionError:
        print(prefix + "└── [Permission denied]")
        return

    # Filter out ignored directories
    items = [item for item in items if item not in ignore_dirs]
    
    pointers = ['├── '] * (len(items) - 1) + ['└── ']

    for pointer, item in zip(pointers, items):
        path = os.path.join(start_path, item)
        print(prefix + pointer + item)
        if os.path.isdir(path) and (max_level is None or current_level < max_level):
            extension = '│   ' if pointer == '├── ' else '    '
            print_tree(path, prefix + extension, ignore_dirs, max_level, current_level + 1)

def usage():
    print("""maptree - Directory tree visualizer

Usage:
  maptree [<path>] [options]

Options:
  -h, --help      Show this help message
  -l, --level N   Maximum depth to display (default: unlimited)
  -a, --all       Show all directories (ignore nothing)
  
Default ignored directories: """ + ', '.join(DEFAULT_IGNORE))

def main():
    path = '.'  # default to current directory
    max_level = None
    ignore_dirs = DEFAULT_IGNORE

    # Simple argument parsing
    args = sys.argv[1:]
    if '-h' in args or '--help' in args:
        usage()
        sys.exit(0)
    
    if '-a' in args or '--all' in args:
        ignore_dirs = set()
        args.remove('-a' if '-a' in args else '--all')
    
    if '-l' in args or '--level' in args:
        flag = '-l' if '-l' in args else '--level'
        try:
            index = args.index(flag)
            max_level = int(args[index + 1])
            args.pop(index)
            args.pop(index)
        except (ValueError, IndexError):
            print("Error: --level requires an integer argument")
            sys.exit(1)
    
    if len(args) > 0:
        path = args[0]

    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid directory.")
        sys.exit(1)
    
    print(os.path.abspath(path))
    print_tree(path, ignore_dirs=ignore_dirs, max_level=max_level)

if __name__ == "__main__":
    main()