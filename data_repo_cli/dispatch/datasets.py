import data_repo_cli.api.datasets as datasets


def dispatch_retrieve_dataset(clients, args):
    dataset_id = args.id[0]
    include = args.include
    return datasets.retrieve_dataset(clients, dataset_id, include)


def dispatch_delete_dataset(clients, args):
    dataset_id = args.id[0]
    add_steward = args.add_steward
    return datasets.delete_dataset(clients, dataset_id, add_steward)


def dispatch_enumerate_datasets(clients, args):
    return datasets.enumerate_datasets(clients, args.filter, args.sort, args.direction, args.offset, args.limit)
