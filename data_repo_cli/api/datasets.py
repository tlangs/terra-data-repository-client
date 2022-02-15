from data_repo_cli.api.jobs import wait_for_job
from data_repo_cli.common.gcloud_commands import get_current_gcloud_user

from data_repo_cli.common.client_logger import logger


def enumerate_datasets(clients, filter_string, sort, direction, offset, limit):
    return clients.datasets_api.enumerate_datasets(
        filter=filter_string,
        sort=sort,
        direction=direction,
        offset=offset,
        limit=limit
    )


def retrieve_dataset(clients, dataset_id, include):
    return clients.datasets_api.retrieve_dataset(dataset_id, include=include)


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
