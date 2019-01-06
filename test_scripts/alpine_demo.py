import docker

if __name__ == '__main__':
    client: docker.client = docker.from_env()
    container = client.containers.run('alpine:3.8', detach=True)

    ipam_pool = docker.types.IPAMPool(
        subnet='192.168.23.0/24',
        gateway='192.168.23.1'
    )

    ipam_config = docker.types.IPAMConfig(
        pool_configs=[ipam_pool]
    )

    mynet = client.networks.create(
        "network_test",
        driver="bridge",
        ipam=ipam_config
    )

    ip = {"ipv4_address": "192.168.23.2"}
    mynet.connect(container, ip)
