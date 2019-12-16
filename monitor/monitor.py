from k8spodmonitor1 import K8sPodMonitor

host = "https://35.202.51.4:443"
namespace = "default"
monitor = K8sPodMonitor(host, namespace)
monitor.start()

