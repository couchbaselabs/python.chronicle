from tests.simple_tests import SimpleTests

import getopt
import sys
import unittest
import paramiko
import spec.test_input as t


def main(argv):
    test_input = t.test_input
    try:
        opts, args = getopt.getopt(argv, "ht:in:u:p:")
    except getopt.GetoptError:
        print('python runner.py -t module -i source_dir_chronicle -n node')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python runner.py -t module -i source_dir_chronicle -n node -u username -p password')
            sys.exit()
        elif opt in "-t":
            module = arg
        elif opt in "-i":
            test_input["install_dir"] = arg
        elif opt in "-n":
            test_input["node"] = arg
        elif opt in "-u":
            test_input["username"] = arg
        elif opt in "-p":
            test_input["password"] = arg
    cleanup()

    unittest.TestLoader.sortTestMethodsUsing = None
    suite = unittest.TestLoader().loadTestsFromTestCase(eval(module))
    unittest.TextTestRunner().run(suite)


def cleanup():
    """
    Cleanups logs folders before running tests
    """
    test_input = t.test_input
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(test_input["node"], username=test_input["username"], password=test_input["password"])
    cmd = "rm -rf /*chr"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(test_input["node"], username=test_input["username"], password=test_input["password"])
    cmd = "pkill -9 -f start_cluster"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    cmd = "pkill -9 -f erlang"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit("ERROR command-line parameter must be supplied for these tests")
    argv = sys.argv[1:]
    main(argv=argv)
