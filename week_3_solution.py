"""
makes FileReader class, which takes path to file on disk drive,
with method read returns content of the file as string and handles
an exception IOError
"""


class FileReader:
    def __init__(self, path):
        self.path = path
        print(self.path)


    def read(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                content = f.read()
        except IOError:
            print("IOError, file  not found")
            content = ""
        finally:
            return content


def main(path):
    reader = FileReader(path)
    print(reader.read())

if __name__ == "__main__":
    main("some text.txt")

