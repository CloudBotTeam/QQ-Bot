import os
import configparser
import random

import docker

env_dict = {
    "CQHTTP_SERVE_DATA_FILES": "yes",
    "CQHTTP_SERVE_DATA_FILES": "yes",
    # 尚未实现
    "CQHTTP_USE_WS": "no",
    "CQHTTP_USE_HTTP": "yes",
    "CQHTTP_POST_MESSAGE_FORMAT": "array"
}

CQHTTP_POST_URL: str = "CQHTTP_POST_URL"
COOLQ_ACCOUNT: str = "COOLQ_ACCOUNT"


if __name__ == '__main__':
    try:
        # 获得环境变量的 上报地址
        random_port = random.randint(9005, 20000)
        post_url: str = os.environ.get(CQHTTP_POST_URL, "http://10.0.0.229:8101")
        # 跑到的 account
        coolq_account: str = os.environ.get(COOLQ_ACCOUNT, "3187545268")
        # 事件接收的端口
        event_recv_port: int = int(os.environ.get("EVENT_RECV_PORT", "5700"))
        expose_login_port: int = int(os.environ.get("EXPOSE_LOGIN_PORT", "9005"))
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

        if coolq_account:
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
            with open("coolq/app/io.github.richardchien.coolqhttpapi/config/{}.ini".format(coolq_account),
                      encoding='utf-8',
                      mode='w') as f:
                config.write(f)

        client = docker.from_env()
        # 这是一个阻塞调用
        resp = client.containers.run("richardchien/cqhttp:latest",
                                     ports={
                                         "9000/tcp": expose_login_port,
                                         "5700/tcp": event_recv_port,
                                     }, environment=env_dict,
                                     volumes={
                                        os.path.join(pwd, "coolq"): {
                                            "bind": "/home/user/coolq",
                                            "mode": "rw",
                                        },
                                     }, detach=True)
        # client.networks.get('staticnet').connect(resp, ipv4_address="192.168.50.100")
        try:
            for line in resp.logs(stream=True):
                line = line.strip()
                if line:
                    print(line.decode('utf-8'))
        except KeyboardInterrupt as e:
            resp.stop()
            raise e
    except Exception as e:
        raise e

