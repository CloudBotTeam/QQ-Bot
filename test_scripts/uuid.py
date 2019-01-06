import uuid

if __name__ == '__main__':

    prefix = uuid.uuid4().__str__()
    print(prefix)