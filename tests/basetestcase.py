import time
import unittest
import logging
import spec.test_input as t
import paramiko
import datetime


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        print("\n")
        self.log = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
        # For detailed line numbers, file name logging uncomment the below
        # logging.basicConfig(format='[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        #                     datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

        logging.getLogger("paramiko").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.input = t.test_input
        self.path_to_compiled_chronicle = self.input["install_dir"]
        self.username = self.input["username"]
        self.password = self.input["password"]
        now = datetime.datetime.now()
        self.path_to_log = "/" + str(now.second) + str(now.microsecond) + "chr"
        self.log.info("starting test: {0}".format(self._testMethodName))
        self.start_cluster()
        self.log.info("BaseTestCase setup finished")

    def install_libraries(self, node):
        """
        Install any commands/libraries on the node that are
        used in the code
        eg: lsof command
        """
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(node, username=self.username, password=self.password)
        cmd = "yum install -y lsof"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        exit_status = ssh_stdout.channel.recv_exit_status()
        if not (exit_status == 0):
            self.fail("lsof command failed")

    def copy_chronicle(self, node):
        """
        Copy compiled chronicle repo to a different place per test
        to make logs. Use this on a per test basis and later zip this
        """
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(node, username=self.username, password=self.password)
        cmd = "mkdir " + self.path_to_log
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        exit_status = ssh_stdout.channel.recv_exit_status()
        if not (exit_status == 0):
            self.fail("mkdir command failed")

        cmd = "cp -a " + self.path_to_compiled_chronicle + "/ . " + self.path_to_log + "/"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        self.log.info("copied a copy of compiled chronicle to logs folder: {0}".
                      format(self.path_to_log))
        exit_status = ssh_stdout.channel.recv_exit_status()
        if not (exit_status == 0):
            self.fail("cp command failed")

    def setup_cluster(self, node, num_nodes):
        """
        Setup cluster of num_nodes with node being the primary node
        """
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(node, username=self.username, password=self.password)
        transport = ssh.get_transport()
        channel = transport.open_session()
        cmd = self.path_to_log + \
              "/compiled_chronicle/chronicle/start_cluster --app chronicled --num-nodes 5 " \
              "--hostname 127.0.0.1 > /dev/null 2>&1 &"
        channel.exec_command(cmd)
        time.sleep(15)
        self.log.info("Started cluster finally")

    def start_cluster(self):
        """
        Start a cluster of 5 nodes
        """
        self.install_libraries(self.input["node"])
        self.copy_chronicle(self.input["node"])
        self.setup_cluster(self.input["node"], 5)

    def tearDown(self):
        # Kill processes
        self.log.info("tearing down")
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.input["node"], username=self.username, password=self.password)
        cmd = "pkill -9 -f start_cluster"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
        cmd = "pkill -9 -f erlang"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
