from tests.basetestcase import BaseTestCase
from lib.util import Util
import threading

import unittest


class Volume(BaseTestCase):
    def setUp(self):
        super(Volume, self).setUp()
        self.primary_node = self.input["node"]
        self.util = Util(self.primary_node)
        self.data_load_flag = False
        self.number_of_cycles = 100  # ToDO: scale it up later
        self.number_of_kv_pairs = 100000  # ToDO: scale it up later

    def tearDown(self):
        super(Volume, self).tearDown()

    def assert_rebalance(self, bool):
        self.assertTrue(bool, "Rebalance failed")

    def wipe_removed_nodes(self, removed_nodes):
        """
        Wipes the removed nodes
        :param removed_nodes: eg:'["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1"]'
        """
        removed_nodes_list = removed_nodes.strip('][').split(', ')
        for removed_node in removed_nodes_list:
            number = removed_node[11]
            port = 8080 + int(number)
            bool_val, content, response = self.util.wipe_node(self.primary_node + ":" + str(port))
            self.assertTrue(bool_val, "could not wipe node")

    def infinite_data_load(self):
        """
        Add million key value pairs
        Update million key value pairs
        Read million key value pairs
        Delete million key value pairs
        repeat
        """
        self.log.info("Starting infinite data load")
        while self.data_load_flag:
            self.log.info("Adding keys")
            for i in range(1, self.number_of_kv_pairs):
                key = "key" + str(i)
                value = str(i)
                bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                                      key=key, value=value)
            self.log.info("Updating keys")
            for i in range(1, self.number_of_kv_pairs):
                key = "key" + str(i)
                value = str(i + 1)
                bool_val, content, response = self.util.update_value(self.primary_node + ":8080",
                                                                     key=key, value=value)
            self.log.info("Reading keys")
            for i in range(1, self.number_of_kv_pairs):
                key = "key" + str(i)
                content = self.util.get_value(self.primary_node + ":8080", key=key)
                expected_value = str(i + 1)
                self.assertEqual(str(content), expected_value)

            self.log.info("Removing keys")
            for i in range(1, self.number_of_kv_pairs):
                key = "key" + str(i)
                bool_val, content, response = self.util.delete_key(self.primary_node + ":8080",
                                                                   key=key)

    def test_volume(self):
        """
        Step 0: create a 1 node cluster
        Step 0.1: Start infinite data load
        Repeat for 100 cycles below steps:
        Step 1: Add one node
        Step 2: Remove one node
        Step 3: Add multiple nodes
        Step 4: Remove multiple nodes (all except init nodes)
        """

        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        self.data_load_flag = True
        data_load_thread = threading.Thread(target=self.infinite_data_load)
        data_load_thread.start()

        for cycle in range(self.number_of_cycles):
            self.log.info("starting cycle: {0}".format(cycle))

            print("#############################################################################")
            self.log.info("Step 1: Adding a single node")
            nodes_to_add = '"chronicle_1@127.0.0.1"'
            bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                             nodes_to_add=nodes_to_add)
            self.assert_rebalance(bool_val)
            bool_val, content, response = self.util.get_config(self.primary_node + ":8080")
            self.log.info("config of the cluster: {0} {1} {2}".format(bool_val, content, response))

            print("#############################################################################")
            self.log.info("Step 2: Removing a single node")
            nodes_to_remove = '["chronicle_1@127.0.0.1"]'
            bool_val, content, response = self.util.remove_node(self.primary_node + ":8080",
                                                                nodes_to_remove=nodes_to_remove)
            self.assert_rebalance(bool_val)
            bool_val, content, response = self.util.get_config(self.primary_node + ":8080")
            self.log.info("config of the cluster: {0} {1} {2}".format(bool_val, content, response))
            self.wipe_removed_nodes(nodes_to_remove)
            self.log.info("config of the cluster: {0} {1} {2}".format(bool_val, content, response))

            print("#############################################################################")
            self.log.info("Step 3: Adding multiple nodes")
            nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", "chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
            bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                             nodes_to_add=nodes_to_add)
            self.assert_rebalance(bool_val)
            bool_val, content, response = self.util.get_config(self.primary_node + ":8080")
            self.log.info("config of the cluster: {0} {1} {2}".format(bool_val, content, response))

            print("#############################################################################")
            self.log.info("Step 4: Removing multiple nodes")
            nodes_to_remove = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", "chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
            bool_val, content, response = self.util.remove_node(self.primary_node + ":8080",
                                                                nodes_to_remove=nodes_to_remove)
            self.assert_rebalance(bool_val)
            bool_val, content, response = self.util.get_config(self.primary_node + ":8080")
            self.log.info("config of the cluster: {0} {1} {2}".format(bool_val, content, response))
            self.wipe_removed_nodes(nodes_to_remove)

        self.data_load_flag = False
        data_load_thread.join()
