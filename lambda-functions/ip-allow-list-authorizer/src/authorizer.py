import os

from netaddr import IPNetwork, IPAddress


def lambda_handler(event, context):
    source_ip = IPAddress(event["headers"]["x-forwarded-for"].strip())

    for cidr in allowed_cidrs():
        if source_ip in IPNetwork(cidr):
            return authorized()

    return denied()


def allowed_cidrs():
    return os.environ.get('ALLOWED_CIDRS', '').split(",")


def authorized():
    return {"isAuthorized": True}


def denied():
    return {"isAuthorized": False}
