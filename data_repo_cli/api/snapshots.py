from data_repo_cli.api.jobs import wait_for_job
from data_repo_cli.common.gcloud_commands import get_current_gcloud_user
from data_repo_cli.common.client_logger import logger


def add_snapshot_policy_member(clients, snapshot_id, email, policy_name):
    snapshots_api = clients.snapshots_api
    request = {'email': email}
    snapshots_api.add_snapshot_policy_member(snapshot_id, policy_name, policy_member=request)
    logger.info(f'Added {email} as a {policy_name} on snapshot with id: {snapshot_id}')


def add_snapshot_steward(clients, snapshot_id, email):
    add_snapshot_policy_member(clients, snapshot_id, email, 'steward')


def delete_snapshot(clients, snapshot_id, add_steward):
    snapshots_api = clients.snapshots_api
    logger.info(f'Deleting snapshot with ID: {snapshot_id}')
    if add_steward:
        current_user = get_current_gcloud_user()
        logger.info(f'adding {current_user} as a steward before deleting the snapshot')
        add_snapshot_steward(clients, snapshot_id, current_user)

    delete_snapshot_job = snapshots_api.delete_snapshot(snapshot_id)
    wait_for_job(clients, delete_snapshot_job)
    logger.info(f'Successfully deleted snapshot with id: {snapshot_id}')


def get_snaphsots_for_dataset_worker(clients, dataset_id: str, offset: int, limit: int, acc: list):
    snapshots_api = clients.snapshots_api
    response = snapshots_api.enumerate_snapshots(dataset_ids=[dataset_id], offset=offset, limit=limit)
    acc.extend(response.items)
    if len(acc) < response.filtered_total:
        return get_snaphsots_for_dataset_worker(clients, dataset_id, offset + limit, limit, acc)
    return acc


def get_snapshots_for_dataset(clients, dataset_id):
    logger.info(f'Getting snapshots off of dataset with ID: {dataset_id}')
    snapshots = get_snaphsots_for_dataset_worker(clients, dataset_id, 0, 10, [])
    return snapshots
