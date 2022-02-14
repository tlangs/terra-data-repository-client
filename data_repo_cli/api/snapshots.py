from data_repo_cli.api.jobs import wait_for_job
from data_repo_cli.common.gcloud_commands import get_current_gcloud_user
from data_repo_cli.common.client_logger import logger
from data_repo_cli.dispatch.utils import dispatch_single_id_arg
from data_repo_cli.dispatch.snapshots import dispatch_delete_snapshot


def setup_parser(subparsers):
    delete_snapshot_parser = subparsers.add_parser('delete-snapshot', help='delete a snapshot from TDR')
    delete_snapshot_parser.set_defaults(func=dispatch_delete_snapshot)
    delete_snapshot_parser.add_argument('id', metavar='id', nargs=1, help='The ID of the snapshot to delete')
    delete_snapshot_parser.add_argument('--add-steward', action='store_true',
                                        help='Add the currently-authed gcloud user as steward before deleting')

    snapshots_for_dataset_parser = subparsers.add_parser('snapshots-for-dataset',
                                                         help='Get the snapshots belonging to a dataset')
    snapshots_for_dataset_parser.set_defaults(func=dispatch_single_id_arg(get_snapshots_for_dataset))
    snapshots_for_dataset_parser.add_argument('id', metavar='id', nargs=1,
                                              help='The ID of the dataset to get the snapshots for')


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
