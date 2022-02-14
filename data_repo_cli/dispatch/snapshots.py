import data_repo_cli.api.snapshots as snapshots


def dispatch_delete_snapshot(clients, args):
    snapshot_id = args.id[0]
    add_steward = args.add_steward
    return snapshots.delete_snapshot(clients, snapshot_id, add_steward)
