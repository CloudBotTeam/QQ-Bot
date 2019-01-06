import docker

if __name__ == '__main__':
    client = docker.from_env()
    print(client.api.inspect_container("84cbe8067edf")['NetworkSettings']['IPAddress'])