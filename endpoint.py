from parser import parse_lines
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from time import sleep
import subprocess

class CustomCollector(object):

    def collect(self):
        raw_data = subprocess.run(["/usr/local/sbin/apcaccess"], capture_output=True).stdout.decode("ascii")
        metrics = parse_lines(raw_data.split("\n"))
        for name, value in metrics.items():
            if name == "status":
                status = GaugeMetricFamily("status", "-- n/a --", labels=["flag"])
                for flag_name, flag_value in value.items():
                    status.add_metric([flag_name], int(flag_value))
                yield status

            else:
                yield GaugeMetricFamily(name, "-- n/a --", value=value)

REGISTRY.register(CustomCollector())
start_http_server(9150)

while True:
    sleep(100)
