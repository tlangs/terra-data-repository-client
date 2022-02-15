from data_repo_cli.api.firestore import calculate_dataset_file_size


def dispatch_calculate_dataset_file_size(clients, args):
    dataset_id = args.id[0]
    data_project = args.data_project
    return calculate_dataset_file_size(clients, dataset_id, data_project)
