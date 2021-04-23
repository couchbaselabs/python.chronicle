import time

from tests.basetestcase import BaseTestCase
from lib.util import Util

import unittest


class FailureTests(BaseTestCase):
    def setUp(self):
        super(FailureTests, self).setUp()
        self.primary_node = self.input["node"]
        self.util = Util(self.primary_node)

    def tearDown(self):
        super(FailureTests, self).tearDown()

    def test_reads_on_stopped_node(self):
        """
        Negative test to verify that reads fail on a stopped node
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        key = "key"
        value = "1"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                              key=key, value=value)
        self.util.stop_node("8081")
        try:
            _ = self.util.get_value(self.primary_node + ":8081", key=key)
        except Exception as e:
            self.log.info("Read on stopped node failed as expected: {0}".format(e))
        else:
            self.fail("Read on stopped node did not fail")

    def test_reads_on_revived_node(self):
        """
        Start a 3 node cluster. Stop the second node and immediately
        revive the node.
        Issue get and write from the revived node and verify
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        key = "key"
        value = "1"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                              key=key, value=value)
        self.util.stop_node("8081")
        self.util.start_node("8081")

        content = self.util.get_value(self.primary_node + ":8081", key=key)
        self.assertEqual(str(content), value)

        second_key = "key2"
        second_value = "2"
        bool_val, content, response = self.util.add_key_value(self.primary_node + ":8081",
                                                              key=second_key, value=second_value)
        content = self.util.get_value(self.primary_node + ":8081", key=second_key)
        self.assertEqual(str(content), second_value)

    def test_quorum_reads_cruds_before_after_reviving_random_node(self):
        """
        Start a 3 node cluster. Do:
        Add key/value pairs before stopping random node
        Add some more keys and update some values after stopping node
        Verify history(quorum reads) after reviving node, from revived node
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        for i in range(50):
            key = "key" + str(i)
            value = str(i)
            bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                                  key=key, value=value)
        self.util.stop_node("8081")
        for i in range(50):
            key = "key" + str(i)
            value = str(i + 1)
            bool_val, content, response = self.util.update_value(self.primary_node + ":8080",
                                                                 key=key, value=value)
        for i in range(50, 100):
            key = "key" + str(i)
            value = str(i + 1)
            bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                                  key=key, value=value)
        self.util.start_node("8081")
        for i in range(100):
            key = "key" + str(i)
            expected_value = str(i + 1)
            content = self.util.get_value(self.primary_node + ":8081", key=key, consistency_level="quorum")
            self.assertEqual(str(content), expected_value)

    def test_quorum_reads_cruds_before_after_reviving_leader_node(self):
        """
        Start a 3 node cluster. Do:
        Add key/value pairs before stopping leader node
        Add some more keys and update some values after stopping leader node
        Verify history(quorum reads) after reviving node, from revived node
        """
        bool_val, content, response = self.util.provision_node(self.primary_node + ":8080")

        nodes_to_add = '["chronicle_1@127.0.0.1", "chronicle_2@127.0.0.1"]'
        bool_val, content, response = self.util.add_node(self.primary_node + ":8080",
                                                         nodes_to_add=nodes_to_add)
        for i in range(50):
            key = "key" + str(i)
            value = str(i)
            bool_val, content, response = self.util.add_key_value(self.primary_node + ":8080",
                                                                  key=key, value=value)
        self.util.stop_node("8080")
        time.sleep(20)  # ToDo: Why does it not work without sleep? Time for Replicated log sync maybe?
        for i in range(50):
            key = "key" + str(i)
            value = str(i + 1)
            bool_val, content, response = self.util.update_value(self.primary_node + ":8081",
                                                                 key=key, value=value)
        for i in range(50, 100):
            key = "key" + str(i)
            value = str(i + 1)
            bool_val, content, response = self.util.add_key_value(self.primary_node + ":8081",
                                                                  key=key, value=value)
        self.util.start_node("8080")
        for i in range(100):
            key = "key" + str(i)
            expected_value = str(i + 1)
            content = self.util.get_value(self.primary_node + ":8080", key=key, consistency_level="quorum")
            self.assertEqual(str(content), expected_value)

