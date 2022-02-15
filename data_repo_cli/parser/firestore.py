from data_repo_cli.dispatch.firestore import dispatch_calculate_dataset_file_size


def setup_firestore_parser(subparsers):
    dataset_file_size_parser = subparsers.add_parser('dataset-file-size',
                                                     help='Calculate the sum of file sizes in a dataset in bytes')
    dataset_file_size_parser.set_defaults(func=dispatch_calculate_dataset_file_size)
    dataset_file_size_parser.add_argument('id', metavar='id', nargs=1,
                                          help="The ID of the dataset to calculate size for")
    dataset_file_size_parser.add_argument('-d', '--data-project', default=None,
                                          help='Use this data project instead of getting the data project from the API')
