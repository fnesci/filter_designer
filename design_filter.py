import argparse
import json
import sys

import FilterDescriptor

class JsonCodec:
    @staticmethod
    def default_encoding(label, o):
        return {label : o.__dict__}

    class JsonEncoder(json.JSONEncoder):
        def __init__(self, *args, **kwargs):
            json.JSONEncoder.__init__(self, *args, **kwargs)
            self.object_to_json = {}

            encoders, decoders = FilterDescriptor.FilterDescriptor.get_json_codec()
            self.__add_encoder(encoders)

        def __add_encoder(self, encoder):
            """
            This method recusrively goes through the possible
            list of list of lists of encoders
            :param encoder:
            :return:
            """
            if isinstance(encoder, list):
                for e in encoder:
                    self.__add_encoder(e)
            else:
                label, entry = encoder
                self.object_to_json[label] = entry

        def default(self, o):
            encoder = self.object_to_json.get(type(o), None)
            if encoder is not None:
                return encoder(o)
            else:
                return {'"{}"'.format(type(o)) : o.__dict__}

    def __init__(self):
        self.json_to_object = {}

    def __add_decoder(self, decoder):
        """
        This method recusrively goes through the possible
        list of list of lists of encoders
        :param encoder:
        :return:
        """
        if isinstance(decoder, list):
            for e in decoder:
                self.__add_decoder(e)
        else:
            label, entry = decoder
            self.json_to_object[label] = entry

    def __object_hook(self, o):
        if len(o) == 1 and 
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


    def add_encoder(self, encoder):
        pass

    def add_decoder(self, decoder):
        pass

    def get_encoder_cls(self):
        return None

    def get_decoder_cls(self):
        pass

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
    #cl = parse_command_line()
    fd = get_sample_filter_descriptor()

    fd_data = json.dumps(fd, indent=2, cls=JsonCodec.JsonEncoder)
    print(fd_data)

    #fd_data = json.dumps(fd, indent=2, cls=json.JSONDecoder)

    fd2 = json.loads(fd_data, cls=FilterDescriptorDecoder)
    print(fd2)

