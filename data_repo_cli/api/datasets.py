from data_repo_cli.api.jobs import wait_for_job
from data_repo_cli.common.gcloud_commands import get_current_gcloud_user

from data_repo_cli.common.client_logger import logger
from data_repo_cli.common.constants import SORT_FIELDS, SORT_DIRECTIONS
from data_repo_cli.dispatch.datasets import dispatch_delete_dataset, dispatch_enumerate_datasets


def setup_parser(subparsers):
    delete_dataset_parser = subparsers.add_parser('delete-dataset', help='delete a dataset from TDR')
    delete_dataset_parser.set_defaults(func=dispatch_delete_dataset)
    delete_dataset_parser.add_argument('id', metavar='id', nargs=1, help='The ID of the dataset to delete')
    delete_dataset_parser.add_argument('--add-steward', action='store_true', help='Add the currently-authed gcloud '
                                                                                  'user as steward before deleting')

    enumerate_datasets_parser = subparsers.add_parser('enumerate-datasets', help="Enumerate datasets")
    enumerate_datasets_parser.set_defaults(func=dispatch_enumerate_datasets)
    enumerate_datasets_parser.add_argument('-f', '--filter', type=str, default=None,
                                           help="Case-insensitive match on the name or description")
    enumerate_datasets_parser.add_argument('-s', '--sort', type=str, choices=SORT_FIELDS, default=None,
                                           help="Field to sort results by")
    enumerate_datasets_parser.add_argument('-d', '--direction', type=str, choices=SORT_DIRECTIONS, default=None,
                                           help="The direction of sorting")
    enumerate_datasets_parser.add_argument('-r', '--region', type=str, default=None,
                                           help="Restrict results to the provided region")
    enumerate_datasets_parser.add_argument('-o', '--offset', type=int, default=None,
                                           help="Offset the results be the specified amount")
    enumerate_datasets_parser.add_argument('-l', '--limit', type=int, default=None,
                                           help="Limit the results to the specified number")


def enumerate_datasets(clients, filter_string, sort, direction, offset, limit):
    return clients.datasets_api.enumerate_datasets(
        filter=filter_string,
        sort=sort,
        direction=direction,
        offset=offset,
        limit=limit
    )


def add_dataset_policy_member(clients, dataset_id, email, policy_name):
    datasets_api = clients.datasets_api
    request = {'email': email}
    datasets_api.add_dataset_policy_member(dataset_id, policy_name, policy_member=request)
    logger.info(f'Added {email} as a {policy_name} on dataset with id: {dataset_id}')


def add_dataset_steward(clients, dataset_id, email):
    add_dataset_policy_member(clients, dataset_id, email, 'steward')


def delete_dataset(clients, dataset_id, add_steward):
    datasets_api = clients.datasets_api
    logger.info(f'Deleting dataset with ID: {dataset_id}')
    if add_steward:
        current_user = get_current_gcloud_user()
        logger.info(f'adding {current_user} as a steward before deleting the dataset')
        add_dataset_steward(clients, dataset_id, current_user)

    delete_dataset_job = datasets_api.delete_dataset(dataset_id)
    wait_for_job(clients, delete_dataset_job)
    logger.info(f'Successfully deleted dataset with id: {dataset_id}')
