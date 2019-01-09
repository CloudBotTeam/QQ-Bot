from flask import Flask, jsonify, request

from build_docker import build_docker_wechat, build_docker_qq, client

app = Flask(__name__)

app_map = {}


@app.route('/containers', methods=['GET'])
def get_containers():
    # print(app_map.values())
    return jsonify(list(app_map.values()))


@app.route("/create")
def add_account():
    data_type = request.args['type']
    if data_type == 'qq':
        build_docker = build_docker_qq
    else:
        build_docker = build_docker_wechat
    ip, cid, name, expose_login_port, resp = build_docker('bot-manager', 8101)
    app_map[str(cid)] = (ip, cid, name, expose_login_port, resp)
    return jsonify({
        'ip': ip,
        'container_name': name,
        'container_id': cid,
        'expose_login_port': expose_login_port,
        'bot_type': data_type
    })


@app.route("/delete/<container_id>", methods=['DELETE'])
def destroy(container_id):
    ip, cid, name, expose_login_port, resp = app_map[str(container_id)]
    resp.stop()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
