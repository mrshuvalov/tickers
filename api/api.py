from flask import Flask,jsonify
from flask_sse import sse
import logging
import json
import redis
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://redis"
app.register_blueprint(sse, url_prefix='/events')
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)
r = redis.Redis(host='redis', port=6379)


def publish_sse(p):
    with app.app_context():
        message = p.get_message()
        if message:
            sse.publish(message.get('data').decode("utf-8"))

sched = BackgroundScheduler(daemon=True)
sched.start()


@app.route('/start/<name>')
def start_sse(name: str):
    p = r.pubsub()
    p.subscribe(name)
    sched.add_job(lambda: publish_sse(p),'interval',seconds=10, id=name)
    return jsonify([])

@app.route('/stop/<name>')
def stop_sse(name: str):
    sched.remove_job(name)
    return jsonify([])



if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000)
