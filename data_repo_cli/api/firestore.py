from data_repo_cli.api.datasets import retrieve_dataset
from data_repo_cli.common.client_logger import logger

from google.cloud import firestore
from multiprocessing.pool import ThreadPool as Pool


def calculate_dataset_file_size(clients, dataset_id, data_project):
    if data_project is None:
        dataset = retrieve_dataset(clients, dataset_id, ["ACCESS_INFORMATION"])
        data_project = dataset.access_information.big_query.project_id
        logger.info(f"Retrieved dataset, found data project: {data_project}")
    else:
        logger.info(f"Using supplied data-project: {data_project}")

    firestore_client = firestore.Client(project=data_project)
    file_collection = firestore_client.collection(f'{dataset_id}-files')
    documents_list = file_collection.list_documents()
    with Pool() as p:
        bar = p.map(lambda d: d.get(['size']).get('size'), documents_list)
    return sum(bar)
