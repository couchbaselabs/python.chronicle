import paramiko

from lib.rest import Rest

import json
import requests
import logging
import spec.test_input as t


class Util(object):

    def __init__(self, primary_node):
        self.primary_node = primary_node
        self.rest = Rest()
        self.log = logging.getLogger(__name__)
        self.input = t.test_input
        self.username = self.input["username"]
        self.password = self.input["password"]

        logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(primary_node, username=self.username, password=self.password)

    def provision_node(self, provision_node):
        """
        Provisons a node
        :param provision_node: 10.112.200.101:8080 for eg
        :return: bool, content, response
        """
        self.log.info("provisioning node {0}...".format(provision_node))
        api = "http://" + provision_node + "/config/provision/"
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_get(api, headers=headers, session=session)
        if not bool_val:
            self.log.error("provisioning node {0} failed".format(provision_node))
        return bool_val, content, response

    def get_config(self, node):
        self.log.info("getting config for node {0}...".format(node))
        api = "http://" + node + "/config/info"
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_get(api, headers=headers, session=session)
        if not bool_val:
            self.log.error("Getting config for node {0} failed".format(node))
        return bool_val, content, response

    def add_node(self, primary_node, nodes_to_add):
        self.log.info("Adding nodes {0}".format(nodes_to_add))
        api = "http://" + primary_node + "/config/addnode/"
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_post(api, headers=headers, params=nodes_to_add,
                                                                      session=session)
        if not bool_val:
            self.log.error("adding nodes {0} failed".format(nodes_to_add))
        return bool_val, content, response

    def remove_node(self, primary_node, nodes_to_remove):
        self.log.info("removing nodes {0}".format(nodes_to_remove))
        api = "http://" + primary_node + "/config/removenode/"
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_post(api, headers=headers, params=nodes_to_remove,
                                                                      session=session)
        if not bool_val:
            self.log.error("removing nodes {0} failed".format(nodes_to_remove))
        return bool_val, content, response

    def wipe_node(self, node_to_wipe):
        self.log.info("wiping node: {0}".format(node_to_wipe))
        api = "http://" + node_to_wipe + "/node/wipe/"
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_post(api, headers=headers, params=node_to_wipe,
                                                                      session=session)
        if not bool_val:
            self.log.error("wiping node {0} failed".format(node_to_wipe))
        return bool_val, content, response

    def add_key_value(self, node, key, value):
        api = "http://" + node + "/kv/" + str(key)
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_put(api, headers=headers, params=str(value),
                                                                     session=session)
        if not bool_val:
            self.log.error("adding key:value {0}:{1} to node {2} failed".format(key, value, node))
        return bool_val, content, response

    def get_value(self, node, key, consistency_level="local", raise_exception=True):
        """
        Return value associated with key depending on consistency_level
        Raises exception if key not found and raise_exception=True
        """
        api = "http://" + node + "/kv/" + str(key) + "?consistency=" + consistency_level
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_get(api, headers=headers,
                                                                     session=session)
        if not bool_val and raise_exception:
            raise Exception("getting value of key: {0} from node: {1} failed: {2}".format(key, node, content))
        content = json.loads(content)
        return content['value']

    def update_value(self, node, key, value):
        api = "http://" + node + "/kv/" + str(key)
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_post(api, headers=headers, params=str(value),
                                                                      session=session)
        if not bool_val:
            self.log.error("updating key:value {0}:{1} to node {2} failed".format(key, value, node))
        return bool_val, content, response

    def delete_key(self, node, key):
        api = "http://" + node + "/kv/" + str(key)
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_delete(api, headers=headers,
                                                                        session=session)
        if not bool_val:
            self.log.error("deleting key {0} from node {1} failed".format(key, node))
        return bool_val, content, response

    def stop_node(self, port):
        """
        SIGSTOP chronicle on node referenced by port
        :param port: 8080 for first node, 8081 for second node etc.
        """
        self.log.info("Stopping node on port {0}".format(port))
        cmd = "lsof -t -i:" + port + " | xargs kill -19"
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        exit_status = ssh_stdout.channel.recv_exit_status()
        if not (exit_status == 0):
            self.log.error("Failed to stop node")

    def start_node(self, port):
        """
        SIGSTCONT chronicle on node referenced by port
        :param port: 8080 for first node, 8081 for second node etc.
        """
        self.log.info("Starting node on port {0}".format(port))
        cmd = "lsof -t -i:" + port + " | xargs kill -18"
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        exit_status = ssh_stdout.channel.recv_exit_status()
        if not (exit_status == 0):
            self.log.error("failed to start node")

    def kill_node(self, port):
        """
        SIGSTKILL chronicle on node referenced by port
        :param port: 8080 for first node, 8081 for second node etc.
        """
        self.log.info("Killing node on port {0}".format(port))
        cmd = "lsof -t -i:" + port + " | xargs kill -9"
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        exit_status = ssh_stdout.channel.recv_exit_status()
        if not (exit_status == 0):
            self.log.error("failed to kill node")
