import json

from data_repo_client import Configuration, ApiClient, ProfilesApi, DatasetsApi, SnapshotsApi, JobsApi
import argparse

from data_repo_cli.parser.jobs import setup_jobs_parser
from data_repo_cli.parser.datasets import setup_datasets_parser
from data_repo_cli.parser.snapshots import setup_snapshots_parser
from data_repo_cli.parser.firestore import setup_firestore_parser
from data_repo_cli.common.constants import ENVIRONMENTS
from data_repo_cli.common.gcloud_commands import get_access_token


class Clients:
    def __init__(self, host):
        config = Configuration()
        config.host = host
        config.access_token = get_access_token()
        self.api_client = ApiClient(configuration=config)

        self.profiles_api = ProfilesApi(api_client=self.api_client)
        self.datasets_api = DatasetsApi(api_client=self.api_client)
        self.snapshots_api = SnapshotsApi(api_client=self.api_client)
        self.jobs_api = JobsApi(api_client=self.api_client)


def setup_parser():
    parser = argparse.ArgumentParser(prog='TDR Client')
    parser.add_argument('--env',
                        choices=['localhost', 'dev', 'prod'],
                        help='the TDR environment to talk to',
                        required=True)
    subparsers = parser.add_subparsers(help='The action to run')

    setup_jobs_parser(subparsers)
    setup_datasets_parser(subparsers)
    setup_snapshots_parser(subparsers)
    setup_firestore_parser(subparsers)
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    host = ENVIRONMENTS[args.env]
    clients = Clients(host)
    result = args.func(clients, args)
    if result is not None:
        print(json.dumps(result, default=lambda o: o.to_dict(),  indent=4))
