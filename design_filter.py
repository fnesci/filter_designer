import argparse
import json
import sys

from json_io import JsonCodec

import FilterDescriptor


# Force a minimum python version
MIN_PYTHON = (3, 3)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)


def parse_command_line():
    parser = argparse.ArgumentParser(description="Filter Desinger", )
    parser.add_argument("--filter", type=str, action='store', required=True, )

    return parser.parse_args()


def get_sample_filter_descriptor():
    fd = FilterDescriptor.FilterDescriptor()
    fd.segments.append(FilterDescriptor.FilterDescriptor.HorizontalSegment(0.0, 3.0, 1.0))
    fd.segments.append(FilterDescriptor.FilterDescriptor.LinearSegment(3.0, 0.0, 6.0, 0.0))
    return fd


class FilterDescriptorEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, FilterDescriptor.FilterDescriptor):
            return {"filter_descriptor" : o.__dict__}
        if isinstance(o, FilterDescriptor.FilterDescriptor.LinearSegment):
            return {"linear_segment" : o.__dict__}
        if isinstance(o, FilterDescriptor.FilterDescriptor.HorizontalSegment):
            return {"horizontal_segment": o.__dict__}
        else:
            return {'"{}"'.format(type(o)) : o.__dict__}


class FilterDescriptorDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        if 'horizontal_segment' in o:
            params = o['horizontal_segment']
            return FilterDescriptor.FilterDescriptor.HorizontalSegment(
                start_w=params['start_w'],
                stop_w=params['stop_w'],
                mag=params['mag'],
                weight=params['weight']
            )
        print(o)
        return o


if __name__ == '__main__':
    jio = JsonCodec(FilterDescriptor.FilterDescriptor.get_json_codecs())

    #cl = parse_command_line()
    fd = get_sample_filter_descriptor()

    fd_data = jio.dumps(fd, indent=2)
    print(fd_data)

    #fd_data = json.dumps(fd, indent=2, cls=JsonCodec.JsonEncoder)
    #print(fd_data)

    #fd_data = json.dumps(fd, indent=2, cls=json.JSONDecoder)

    #fd2 = json.loads(fd_data, cls=FilterDescriptorDecoder)
    #print(fd2)

