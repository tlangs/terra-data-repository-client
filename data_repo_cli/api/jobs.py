import time

from data_repo_cli.common.client_logger import logger
from data_repo_cli.common.utils import dispatch_single_id_arg


def setup_parser(subparsers):
    job_status_parser = subparsers.add_parser('job-status', help='Get the status of a job')
    job_status_parser.set_defaults(func=dispatch_single_id_arg(get_job_status))
    job_status_parser.add_argument('id', metavar='id', nargs=1, help='The ID of the job to get status of')

    job_result_parser = subparsers.add_parser('job-result', help='Get the result of a job')
    job_result_parser.set_defaults(func=dispatch_single_id_arg(get_job_result))
    job_result_parser.add_argument('id', metavar='id', nargs=1, help='The ID of the job to get result of')


def get_job_status(clients, job_id):
    return clients.jobs_api.retrieve_job(job_id)


def get_job_result(clients, job_id):
    return clients.jobs_api.retrieve_job_result(job_id)


def wait_for_job(clients, job_model):
    result = job_model
    while True:
        if result is None or result.job_status == "running":
            time.sleep(10)
            logger.info(f"Waiting for job {job_model.id} to finish")
            result = clients.jobs_api.retrieve_job(job_model.id)
        elif result.job_status == 'failed':
            result = clients.jobs_api.retrieve_job_result(job_model.id)
            raise f"Could not complete job with id {job_model.id}, got result {result}"
        elif result.job_status == "succeeded":
            logger.info(f"Job {job_model.id} succeeded")
            result = clients.jobs_api.retrieve_job_result(job_model.id)
            return result
        else:
            raise "Unrecognized job state %s" % result.job_status