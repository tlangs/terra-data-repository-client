import json


def convert_list_to_dicts(data_repo_objects):
    dicts = list(map(lambda o: o.to_dict(), data_repo_objects))


def convert_to_dict(data_repo_object):
    return data_repo_object.to_dict()