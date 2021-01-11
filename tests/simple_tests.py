from tests.basetestcase import BaseTestCase
from lib.util import Util

import unittest


class SimpleTests(BaseTestCase):
    def setUp(self):
        super(SimpleTests, self).setUp()
        self.primary_node = self.input["node"]
        self.util = Util(self.primary_node)

    def tearDown(self):
        super(SimpleTests, self).tearDown()

    def test_single_node_cluster(self):
        """
        test provision a single node cluster
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        self.log.info("{0} {1} {2}".format(bool_val, content, response))
        assert bool_val

    def test_multi_node_cluster(self):
        """
        Test adding a 5 node cluster
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", ' \
                       '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        self.log.info("{0} {1} {2}".format(bool_val, content, response))
        assert bool_val

    def test_remove_node(self):
        """
        Test remove single node
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", ' \
                       '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)

        nodes_to_remove = '"chronicle_4@127.0.0.1"'
        bool_val, content, response = self.util.remove_node(self.primary_node + ":8080",
                                                            nodes_to_remove=nodes_to_remove)
        self.log.info("{0} {1} {2}".format(bool_val, content, response))
        assert bool_val

    def test_remove_nodes(self):
        """
        Test remove multiple nodes
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", ' \
                       '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)

        nodes_to_remove = '["chronicle_2@127.0.0.1", ' \
                          '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.remove_node(self.primary_node + ":8080",
                                                            nodes_to_remove=nodes_to_remove)
        self.log.info("{0} {1} {2}".format(bool_val, content, response))
        assert bool_val

    def test_add_key_value_pair(self):
        """
        Create a single node cluster. Add a key,value pair. Add a node.
        Verify the new node returns the value for the key that was added
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        key = "key"
        value = "1"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                              key=key, value=value)
        self.log.info("{0} {1} {2}".format(bool_val, content, response))
        nodes_to_add = '["chronicle_1@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        content = self.util.get_value(self.primary_node + ":8081", key=key)
        self.log.info(content)
        self.assertEqual(str(content), value)

    def test_update_value_single_node(self):
        """
        Create a single node. Add a key-value pair. Update the value for the key.
        Verify the value returned is the updated-value
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        key = "key"
        value = "1"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                              key=key, value=value)
        updated_value = "3"
        bool_val, content, response = self.util.update_value(self.primary_node + ":8080",
                                                             key=key, value=updated_value)

        content = self.util.get_value(self.primary_node + ":8080", key=key)
        self.log.info(content)
        self.assertEqual(str(content), updated_value)

    def test_update_value_two_node(self):
        """
        Create a single node. Add a key-value pair. Add a new node. Update the value
        for the key. Verify that the new node returns the updated-value
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        key = "key"
        value = "1"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                              key=key, value=value)
        nodes_to_add = '["chronicle_1@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        updated_value = "3"
        bool_val, content, response = self.util.update_value(self.primary_node + ":8080",
                                                             key=key, value=updated_value)
        self.log.info("{0} {1} {2}".format(bool_val, content, response))

        content = self.util.get_value(self.primary_node + ":8081", key=key)
        self.log.info(content)
        self.assertEqual(str(content), updated_value)

    def test_delete_key_one_node(self):
        """
        Create a single node. Add a key-value pair. Delete the key.
        Verify reading the key throws exception
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        key = "key"
        value = "1"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                              key=key, value=value)
        bool_val, content, response = self.util.delete_key(self.primary_node + ":8080",
                                                           key=key)
        try:
            content = self.util.get_value(self.primary_node + ":8081", key=key)
        except Exception as e:
            self.log.info(str(e) + "as expected")
        else:
            self.fail("Get value of a deleted key worked")

    def test_delete_key_multiple_nodes(self):
        """
        Create a 5 node cluster
        Delete a key on one node and verify it is deleted on all other nodes
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", ' \
                       '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        key = "key"
        value = "1"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8084",
                                                              key=key, value=value)
        bool_val, content, response = self.util.delete_key(self.primary_node + ":8084",
                                                           key=key)
        for port in [":8080", ":8081", ":8082", ":8083"]:
            try:
                content = self.util.get_value(self.primary_node + port, key=key, consistency_level="quorum")
            except Exception as e:
                self.log.info(str(e) + " as expected")
            else:
                self.fail("Get value of a deleted key worked on node {0}"
                          .format(self.primary_node + port))

    def test_local_reads_after_removing_leader(self):
        """
        Create a 3 node cluster. Add a series of key value pairs.
        Remove the primary node. Verify local reads against those keys.
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", ' \
                       '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        base_key = "key"
        base_val = ""
        values_added = list()
        for i in range(5):
            key = base_key + str(i)
            value = base_val + str(i)
            key = str(key)
            value = str(value)
            bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                                  key=key, value=value)
            values_added.append(value)

        nodes_to_remove = '"chronicle_0@127.0.0.1"'
        bool_val, content, response = self.util.remove_node(self.primary_node + ":8080",
                                                            nodes_to_remove=nodes_to_remove)
        values = list()
        for i in range(5):
            key = base_key + str(i)
            content = self.util.get_value(self.primary_node + ":8081", key=key)
            values.append(str(content))
        self.log.info(values)
        self.assertEqual(values_added, values)

    def test_quorum_reads_after_removing_leader(self):
        """
        Create a 3 node cluster. Add a series of key value pairs.
        Remove the primary node. Verify quorum reads against those keys.
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", ' \
                       '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        base_key = "key"
        base_val = ""
        values_added = list()
        for i in range(5):
            key = base_key + str(i)
            value = base_val + str(i)
            key = str(key)
            value = str(value)
            bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                                  key=key, value=value)
            values_added.append(value)

        nodes_to_remove = '"chronicle_0@127.0.0.1"'
        bool_val, content, response = self.util.remove_node(self.primary_node + ":8080",
                                                            nodes_to_remove=nodes_to_remove)
        values = list()
        for i in range(5):
            key = base_key + str(i)
            content = self.util.get_value(self.primary_node + ":8081", key=key, consistency_level="quorum")
            values.append(str(content))
        self.log.info(values)
        self.assertEqual(values_added, values)

    def test_leader_reads_after_removing_leader(self):
        """
        Create a 3 node cluster. Add a series of key value pairs.
        Remove the primary node. Verify leader reads against those keys.
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")
        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1", ' \
                       '"chronicle_3@127.0.0.1", "chronicle_4@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        base_key = "key"
        base_val = ""
        values_added = list()
        for i in range(5):
            key = base_key + str(i)
            value = base_val + str(i)
            key = str(key)
            value = str(value)
            bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                                  key=key, value=value)
            values_added.append(value)

        nodes_to_remove = '"chronicle_0@127.0.0.1"'
        bool_val, content, response = self.util.remove_node(self.primary_node + ":8080",
                                                            nodes_to_remove=nodes_to_remove)
        values = list()
        for i in range(5):
            key = base_key + str(i)
            content = self.util.get_value(self.primary_node + ":8081", key=key, consistency_level="leader")
            values.append(str(content))
        self.log.info(values)
        self.assertEqual(values_added, values)
