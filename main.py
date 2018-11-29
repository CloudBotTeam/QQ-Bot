import docker

if __name__ == '__main__':
    client = docker.from_env()
    resp = client.containers.run("alpine:3.8", "echo hello world")
    print(resp)
    print(client.images.list())
