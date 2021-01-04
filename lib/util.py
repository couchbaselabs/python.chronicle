from rest import Rest

import json
import requests
import logging


class Util(object):

    def __init__(self, primary_node):
        self.primary_node = primary_node
        self.rest = Rest()
        self.log = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        logging.getLogger("paramiko").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)

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
            self.log.error("adding nodes {0} failed", str(nodes_to_add))
        return bool_val, content, response

    def remove_node(self, primary_node, nodes_to_remove):
        self.log.info("removing nodes {0}".format(nodes_to_remove))
        api = "http://" + primary_node + "/config/removenode/"
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_post(api, headers=headers, params=nodes_to_remove,
                                                                      session=session)
        if not bool_val:
            self.log.error("removing nodes {0} failed", str(nodes_to_remove))
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

    def get_value(self, node, key, consistency_level="local"):
        """
        Return value associated with key depending on consistency_level
        """
        api = "http://" + node + "/kv/" + str(key) + "?consistency=" + consistency_level
        headers = {"Content-Type": "application/json"}
        with requests.Session() as session:
            bool_val, content, response = self.rest.http_session_get(api, headers=headers,
                                                                     session=session)
        if not bool_val:
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
        content = json.loads(content)
        return content['value']
