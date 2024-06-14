from flask import *
import random
import time
import requests
import json
OPNSENSE_IP = "192.168.98.131" #firewall
API_KEY = "jrvyX2oH6Ofqp/7BHfC+3YyBq8YTU3PkcGSKKC6XabZGWKZ9OkDkzp8kUtdsxvKTZ60aw2OtcOXUEw5E"
API_SECRET = "bz92B/FFBOWs1CNrweoJ3iV8N4tkA8Rdf3KMfqzj9lTJ3zMOMbPbqOn9H+TMs2M8e7k2ae7vt4fbsc5x"

#Firmware URL
stats_url = f"http://{OPNSENSE_IP}/api/diagnostics/interface/getInterfaceStatistics"

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("dashboard.html")
@app.route("/get-interfaces")
def get_interfaces():
    packets_ps = requests.get(stats_url,auth=(API_KEY,API_SECRET))
    data = packets_ps.json()
    interfaces = []
    for interface in data['statistics']:
        if('Loopback' not in interface and ':' not in interface):
            interfaces.append(interface)
    return jsonify({'interfaces':interfaces})
@app.route('/firewalltraffic', methods=['GET'])
def get_traffic_value():
    try:
        response = requests.get(stats_url, auth=(API_KEY, API_SECRET))
        data = response.json()
        stats = data['statistics']
        traffic_data = {}
        for interface in stats:
            if 'Loopback' not in interface and ':' not in interface:
                traffic_data[interface] = stats[interface]['sent-bytes']  
        return jsonify(traffic_data)
    except Exception as e:
        return jsonify(f"Error: {e}")
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
