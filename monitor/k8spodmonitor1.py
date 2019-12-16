import kubernetes
from kubernetes import client
from multiprocessing import Process
import os
import sys
import yaml
import time
from spark_rest import *


def get_application_status(pod_name, pod_ip):
    while(True):
        url_base = get_api_url_base(pod_ip) 
        applications = get_all_application(url_base)
        if applications:
            #print (applications)
            app_id = applications[0].get('id')
            jobs = get_all_jobs_application(url_base, app_id)
            #print (jobs)
        time.sleep(10)

class K8sPodMonitor(object):
    """
    This class has methods to monitor Pod on K8 cluster.
    """

    def __init__(self, k8host, namespace):
        self.k8host= k8host
        self.namespace = namespace
        #kubernetes.config.load_kube_config(config_file='/opt/monitor/config')
        configuration = client.Configuration()
        configuration.api_key["authorization"] = "token-goes-here"
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.ssl_ca_cert = 'path-to-certificate'
        configuration.host = self.k8host
        configuration.watch = True
        configuration.debug = True
        self.api_instance = client.CoreV1Api(client.ApiClient(configuration))
        self.watch = None


    def start(self):
        self.monitor_process = Process(target=self.kube_monitor_pod_status())
        self.monitor_process.daemon = True
        self.monitor_process.start()


    def stop(self):
        if self.monitor_process:
            self.monitor_process.terminate()
    

    def kube_monitor_pod_status(self):
        INTERESTED_EVENTS = ["MODIFIED", "DELETED"]
        pods = []
        try:
            allpods = self.api_instance.list_namespaced_pod(self.namespace,
                                                pretty=True,
                                                timeout_seconds=60)
        except kubernetes.client.rest.ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
            return False

        for pod in allpods.items:
            print (pod)

        ''' Watch begins! '''
        w = kubernetes.watch.Watch()
        print ("Starting a watch")
        stream = w.stream(self.api_instance.list_namespaced_pod, self.namespace)
        for event in stream:
            print (pods)
            name = event['object'].metadata.name
            print ("Event type %s:" %(event['type']))
            status = event['object'].status
            pod_ip = status.pod_ip
            print ("Pod (%s) IP (%s) status is (%s)" %(name, pod_ip, status.phase))
            if "driver" in name:
                if status.phase == "Running":
                    #create a DS to hold info. about all the processes that we are spawning
                    application_Status_proc = Process(target=get_application_status(name, pod_ip)) 
                #if phase is stopped or completed or failed
                    #stop the process from the DS
        return (True)


    '''
    def kube_delete_pod(self):
        deleteoptions = client.V1DeleteOptions()
        try:
            pods = api_instance.list_namespaced_pod(self.namespace,
                                                include_uninitialized=False,
                                                pretty=True,
                                                timeout_seconds=60)
        except kubernetes.client.rest.ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)
            return False
        
        for pod in pods.items:
            print (pod)
            if self.name in pod.metadata.name:
                try:
                    api_response = api_pods.delete_namespaced_pod(podname, self.namespace, body=deleteoptions)
                    print (api_response)
                except kubernetes.client.rest.ApiException as e:
                    print ("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

        return True
    '''
