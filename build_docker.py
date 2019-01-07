import os
import configparser
import random

import docker

env_dict = {
    "CQHTTP_SERVE_DATA_FILES": "yes",
    "CQHTTP_SERVE_DATA_FILES": "yes",
    # 尚未实现
    "CQHTTP_USE_WS": "yes",

    "CQHTTP_USE_HTTP": "yes",
    "CQHTTP_POST_MESSAGE_FORMAT": "array"
}

CQHTTP_POST_URL: str = "CQHTTP_POST_URL"
COOLQ_ACCOUNT: str = "COOLQ_ACCOUNT"

client = docker.from_env()


def build_docker(serv_addr: str, serv_port: int):
    http_serv_addr = f"http://{serv_addr}:{serv_port}"
    ws_serv_addr = "ws://" + serv_addr
    # 获得环境变量的 上报地址
    random_port = random.randint(9005, 20000)

    # 跑到的 account
    coolq_account: str = os.environ.get(COOLQ_ACCOUNT, "")
    # 事件接收的端口
    event_recv_port: int = int(os.environ.get("EVENT_RECV_PORT", "5700"))
    post_url: str = os.environ.get(CQHTTP_POST_URL, http_serv_addr)

    expose_login_port: int = random_port
    # 心跳 相关的事件
    enable_heart_beat = bool(os.environ.get("ENABLE_HEART_BEAT", "true"))
    heartbeat_interval = int(os.environ.get("HEARTBEAT_INTERVAL", "15000"))

    pwd = os.getcwd()

    # build env dict
    env_dict[CQHTTP_POST_URL] = post_url
    env_dict[COOLQ_ACCOUNT] = coolq_account

    if enable_heart_beat:
        env_dict["CQHTTP_ENABLE_HEART_BEAT"] = enable_heart_beat
        env_dict["CQHTTP_HEARTBEAT_INTERVAL"] = heartbeat_interval
        env_dict["CQHTTP_PORT"] = event_recv_port
        env_dict["CQHTTP_USE_HTTP"] = 'yes'
        env_dict["CQHTTP_ENABLE_HEART_BEAT"] = "true"
        env_dict["CQHTTP_POST_URL"] = post_url
        # env_dict["CQHTTP_USE_WS"] = "yes"

    if coolq_account is not None and coolq_account != "":
        # write config file
        config = configparser.ConfigParser()
        config[coolq_account] = {}
        config_ini = config[coolq_account]
        config_ini["port"] = '5700'
        config_ini["use_http"] = 'yes'
        config_ini["post_url"] = post_url
        config_ini["post_message_format"] = "array"
        config_ini["enable_heartbeat"] = "true"
        config_ini["heartbeat_interval"] = str(heartbeat_interval)
        # config_ini["use_ws"] = 'true'
        # config_ini['ws_reverse_url'] = "ws://10.0.0.229:8101/"
        # config_ini['ws_reverse_event_url'] = "ws://10.0.0.229:8101/event"
        # config_ini['ws_reverse_reconnect_on_code_1000'] = 'yes'
        # config_ini['use_ws_reverse'] = 'true'

        with open("coolq/app/io.github.richardchien.coolqhttpapi/config/{}.ini".format(coolq_account),
                  encoding='utf-8',
                  mode='w') as f:
            config.write(f)

    # client = docker.DockerClient(base_url='tcp://10.0.0.229:2375')
    # 这是一个阻塞调用

    # os.system("mkdir {new_dir} ; cp -a ./coolq {new_dir}".format(new_dir=random_port))
    resp = client.containers.run("richardchien/cqhttp:latest",
                                 ports={
                                     "9000/tcp": expose_login_port,
                                 }, environment=env_dict,
                                 detach=True, network='cloud-bot-network')
    docker_inspect = client.api.inspect_container(resp.id)
    docker_ip = docker_inspect['NetworkSettings']['IPAddress']
    if docker_ip is None or not docker_ip:
        # print(docker_inspect['NetworkSettings'])
        docker_ip = docker_inspect['NetworkSettings']['Networks']['cloud-bot-network']['IPAddress']
    # print(docker_inspect)
    docker_name = resp.name
    # docker name

    return docker_ip, resp.id, docker_name, random_port, resp


__all__ = ["build_docker", "client"]