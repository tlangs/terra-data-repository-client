from data_repo_cli.api.snapshots import get_snapshots_for_dataset
from data_repo_cli.dispatch.snapshots import dispatch_delete_snapshot
from data_repo_cli.dispatch.utils import dispatch_single_id_arg


def setup_snapshots_parser(subparsers):
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
