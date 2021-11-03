import json

class DefaultClassCodec:
    def __init__(self, label, class_info):
        self.label = label
        self.class_info = class_info

    def encode(self):
        pass

    def decode(self):
        pass

class JsonCodec:
    @staticmethod
    def default_encoding(label, o):
        return {label : o.__dict__}

    class JsonEncoder(json.JSONEncoder):
        def __init__(self, *args, **kwargs):
            json.JSONEncoder.__init__(self, *args, **kwargs)
            self.object_to_json = {}

            #encoders, decoders = FilterDescriptor.FilterDescriptor.get_json_codecs()
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

    def __init__(self, codecs):
        self.json_to_object = {}
        self.class_to_codec = {}
        self.label_to_codec = {}
        self.__add_codecs(codecs)

    def __add_codecs(self, codecs):
        if isinstance(codecs, list):
            for c in codecs:
                self.__add_codecs(c)
        else:
            self.class_to_codec[codecs.class_info] = codecs
            self.label_to_codec[codecs.label] = codecs

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
        #if len(o) == 1 and
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
