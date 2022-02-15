from data_repo_cli.common.constants import SORT_FIELDS, SORT_DIRECTIONS, RETRIEVE_DATASETS_INCLUDES
from data_repo_cli.dispatch.datasets import dispatch_delete_dataset, dispatch_enumerate_datasets, \
    dispatch_retrieve_dataset


def setup_datasets_parser(subparsers):
    retrieve_dataset_parser = subparsers.add_parser('retrieve-dataset', help='Get a dataset from TDR')
    retrieve_dataset_parser.set_defaults(func=dispatch_retrieve_dataset)
    retrieve_dataset_parser.add_argument('id', nargs=1, help='The ID of the dataset to retrieve')
    retrieve_dataset_parser.add_argument('-i', '--include', nargs='*', choices=RETRIEVE_DATASETS_INCLUDES,
                                         help='Information about the dataset to include')

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
