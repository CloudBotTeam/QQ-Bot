import os

import docker

env_dict = {
    "CQHTTP_SERVE_DATA_FILES": "yes",
    "CQHTTP_SERVE_DATA_FILES":"yes",
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
        post_url: str = os.environ.get("CQHTTP_POST_URL")
        # 跑到的 account
        coolq_account: str = os.environ.get("COOLQ_ACCOUNT")
        # 事件接收的端口
        event_recv_port: int = int(os.environ.get("EVENT_RECV_PORT", "5700"))
        expose_login_port: int = int(os.environ.get("EXPOSE_LOGIN_PORT", "9005"))
        pwd = os.getcwd()

        # build env dict
        env_dict[CQHTTP_POST_URL] = post_url
        env_dict[COOLQ_ACCOUNT] = coolq_account

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
                                     })
        print(resp)
    except Exception as e:
        raise e

