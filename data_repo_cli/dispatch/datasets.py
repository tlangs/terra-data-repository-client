import data_repo_cli.api.datasets as datasets


def dispatch_delete_dataset(clients, args):
    dataset_id = args.id[0]
    add_steward = args.add_steward
    datasets.delete_dataset(clients, dataset_id, add_steward)


def dispatch_enumerate_datasets(clients, args):
    return datasets.enumerate_datasets(clients, args.filter, args.sort, args.direction, args.offset, args.limit)
