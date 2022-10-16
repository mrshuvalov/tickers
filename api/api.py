from flask import Flask,jsonify
from flask_sse import sse
import logging
import json
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
import datetime
from helper import Ticker

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

tickers = {f"ticker{el if el > 9 else '0' + str(el)}": Ticker() for el in range(100)}

def server_sent_event(ticker_name):
    with app.app_context():
        sse.publish({**tickers[ticker_name].new_price, 'ticker': ticker_name})
        print("Event Scheduled at ",datetime.datetime.now())

def store_all_tickers():
    for ticker_inst in tickers.values():
        ticker_inst.new_price



sched = BackgroundScheduler(daemon=True)
sched.add_job(store_all_tickers,'interval',seconds=1, id='all_tickers')
sched.start()


@app.route('/start/<name>')
def start_sse(name):
    sched.add_job(lambda: server_sent_event(name),'interval',seconds=5, id=name)
    return jsonify(tickers[name].prices_history)

@app.route('/stop/<name>')
def stop_sse(name):
    sched.remove_job(name)
    return jsonify([])



if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0',port=5000)