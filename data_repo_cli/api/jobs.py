import time

from data_repo_cli.common.client_logger import logger


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
