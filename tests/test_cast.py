import unittest
from random import randint

from cast.app import app, create_parser


class CastShRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_home_status_code(self):
        result = self.app.get("/")
        self.assertEqual(result.status_code, 200)

    def test_download_404_code(self):
        result = self.app.get("/download/")
        self.assertEqual(result.status_code, 404)
        result = self.app.get("/download/{}".format(randint(1, 100000)))
        self.assertEqual(result.status_code, 404)


class CastShCLIOptionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parser = create_parser()
        cls.parser = parser

    def test_cmd_args(self):
        args = self.parser.parse_args([])
        self.assertEqual(args.cmd_args, "")
        args = self.parser.parse_args(["--cmd-args", "ls"])
        self.assertEqual(args.cmd_args, "ls")

    def test_command(self):
        args = self.parser.parse_args([])
        self.assertEqual(args.command, "bash")

    def test_debug(self):
        args = self.parser.parse_args(["--debug"])
        self.assertTrue(args.debug)

    def test_help(self):
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--help"])

    def test_ports(self):
        """
        TODO: verify via a ping to that port
        """
        customer_port = str(randint(6000, 8000))
        args = self.parser.parse_args(["-p", customer_port])
        self.assertEqual(args.port, customer_port)
        args = self.parser.parse_args(["--port", customer_port])
        self.assertEqual(args.port, customer_port)

    def test_version(self):
        args = self.parser.parse_args(["--version"])
        self.assertTrue(args.version)

    def test_bad_version(self):
        with self.assertRaises(SystemExit):
            args = self.parser.parse_args(["--help"])
            self.assertFalse(args.version)
