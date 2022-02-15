from data_repo_cli.api.jobs import get_job_result, get_job_status
from data_repo_cli.dispatch.utils import dispatch_single_id_arg


def setup_jobs_parser(subparsers):
    job_status_parser = subparsers.add_parser('job-status', help='Get the status of a job')
    job_status_parser.set_defaults(func=dispatch_single_id_arg(get_job_status))
    job_status_parser.add_argument('id', metavar='id', nargs=1, help='The ID of the job to get status of')

    job_result_parser = subparsers.add_parser('job-result', help='Get the result of a job')
    job_result_parser.set_defaults(func=dispatch_single_id_arg(get_job_result))
    job_result_parser.add_argument('id', metavar='id', nargs=1, help='The ID of the job to get result of')
