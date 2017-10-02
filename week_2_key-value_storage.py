"""
takes key-value from parameters of command line and write or return
information from temporary storage
"""
import argparse, os, tempfile, json, sys


def get_parameters(args):
    """parse arguments from command line keys"""
    parser = argparse.ArgumentParser(description="Read and show or write key-values couples.")
    parser.add_argument("-k", "--key",
                        nargs='*',
                        help="key name")
    parser.add_argument("-v", "--val",
                        nargs='*',
                        help='Usage: %(prog)s --val 1234 2345 make '
                             '[\'1234\', \'2345\']',
                        required=False)
    return parser.parse_args(args)


def write_json(storage_path, args_key, args_val):
    """
    Add a new element in dictionary
    in json file, create file if it doesn't exist
    """
    d = dict.fromkeys(args_key, args_val)
    if not os.path.isfile(storage_path):
        with open(storage_path, 'w') as f:
            json.dump([d], f)
        return True
    with open(storage_path, 'r') as f:
        storage = json.load(f)
        print("readed: ", storage)
        storage[0][''.join(args_key)] = args_val
        print("append: ", storage)
    with open(storage_path, 'w') as f:
        json.dump(storage, f)
    return True


def read_json(storage_path, args_key):
    """
    Checking if entry exist in dictionary inside json file
    """
    #   print(args_key)
    if os.path.isfile(storage_path):
        with open(storage_path, 'r') as f:
            storage = json.load(f)
            print(storage)
            if args_key in storage[0]:
                return storage[0][args_key]
            else:
                return None
    else:
        print("File doesn't exist")
        return None


def main():
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    print("storage_path: ", storage_path)
    args = get_parameters(sys.argv[1:])
    #   print(args)
    if args.key and args.val:
        write_json(storage_path, args.key, args.val)
    elif args.key:
        #   print(args.key)
        answer = read_json(storage_path, ''.join(args.key))
        if answer:
            print(', '.join(answer))
        else:
            print(answer)


if __name__ == "__main__":
    main()
