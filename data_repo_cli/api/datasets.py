from data_repo_cli.api.jobs import wait_for_job
from data_repo_cli.common.gcloud_commands import get_current_gcloud_user

from data_repo_cli.common.client_logger import logger


def setup_parser(subparsers):
    delete_dataset_parser = subparsers.add_parser('delete-dataset', help='delete a dataset from TDR')
    delete_dataset_parser.set_defaults(func=dispatch_delete_dataset)
    delete_dataset_parser.add_argument('id', metavar='id', nargs=1, help='The ID of the dataset to delete')
    delete_dataset_parser.add_argument('--add-steward', action='store_true', help='Add the currently-authed gcloud '
                                                                                  'user as steward before deleting')


def dispatch_delete_dataset(clients, args):
    dataset_id = args.id[0]
    add_steward = args.add_steward
    delete_dataset(clients, dataset_id, add_steward)


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