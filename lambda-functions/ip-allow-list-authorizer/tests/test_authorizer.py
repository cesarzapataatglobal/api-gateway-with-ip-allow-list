import os
import unittest
from unittest import mock

from src.authorizer import lambda_handler


class LambdaHandlerTest(unittest.TestCase):

    @mock.patch.dict(os.environ, {"ALLOWED_CIDRS": "10.0.0.0/31"})
    def test_returns_false_when_cidr_does_not_contain_sourceIp(self):
        api_gateway_event = {"headers": {"x-forwarded-for": "192.168.0.1"}}

        response = lambda_handler(api_gateway_event, None)

        self.assertFalse(response["isAuthorized"])

    @mock.patch.dict(os.environ, {"ALLOWED_CIDRS": "10.0.0.0/32"})
    def test_returns_true_when_cidr_contain_sourceIp(self):
        api_gateway_event = {"headers": {"x-forwarded-for": "10.0.0.0"}}

        response = lambda_handler(api_gateway_event, None)

        self.assertTrue(response["isAuthorized"])

    @mock.patch.dict(os.environ, {"ALLOWED_CIDRS": "10.0.0.0/31"})
    def test_returns_true_when_cidr_contain_all_sourceIps(self):
        self.assertFalse(lambda_handler({"headers": {"x-forwarded-for": "9.255.255.255"}}, None)["isAuthorized"])
        self.assertTrue(lambda_handler({"headers": {"x-forwarded-for": "10.0.0.0"}}, None)["isAuthorized"])
        self.assertTrue(lambda_handler({"headers": {"x-forwarded-for": "10.0.0.1"}}, None)["isAuthorized"])
        self.assertFalse(lambda_handler({"headers": {"x-forwarded-for": "10.0.0.2"}}, None)["isAuthorized"])

    @mock.patch.dict(os.environ, {"ALLOWED_CIDRS": "10.0.0.0/32"})
    def test_should_trim_sourceIp_with_white_spaces(self):
        self.assertTrue(lambda_handler({"headers": {"x-forwarded-for": " 10.0.0.0 "}}, None)["isAuthorized"])

    @mock.patch.dict(os.environ, {"ALLOWED_CIDRS": "10.0.0.0/32,11.0.0.0/32,12.0.0.0/32"})
    def test_handle_multiple_cirds(self):
        self.assertTrue(lambda_handler({"headers": {"x-forwarded-for": "10.0.0.0"}}, None)["isAuthorized"])
        self.assertTrue(lambda_handler({"headers": {"x-forwarded-for": "11.0.0.0"}}, None)["isAuthorized"])
        self.assertTrue(lambda_handler({"headers": {"x-forwarded-for": "12.0.0.0"}}, None)["isAuthorized"])


if __name__ == "__main__":
    unittest.main()
