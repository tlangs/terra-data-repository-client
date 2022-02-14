import json

from data_repo_client import Configuration, ApiClient, ProfilesApi, DatasetsApi, SnapshotsApi, JobsApi
import argparse

from data_repo_cli.api.jobs import setup_parser as setup_job_parser
from data_repo_cli.api.datasets import setup_parser as setup_dataset_parser
from data_repo_cli.api.snapshots import setup_parser as setup_snapshot_parser
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

    setup_job_parser(subparsers)
    setup_dataset_parser(subparsers)
    setup_snapshot_parser(subparsers)
    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    host = ENVIRONMENTS[args.env]
    clients = Clients(host)
    result = args.func(clients, args)
    if result is not None:
        print(json.dumps(result, default=lambda o: o.to_dict(),  indent=4))
