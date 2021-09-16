import json
from types import SimpleNamespace


def parse_to_dataclass(data: object):
    """
    https://stackoverflow.com/questions/6578986/how-to-convert-json-data-into-a-python-object

    :param data:
    :return:
    """
    json_str = json.dumps(data)
    return json.loads(json_str, object_hook=lambda d: SimpleNamespace(**d))
