import json

class DefaultClassCodec:
    def __init__(self, label, class_info, factory):
        self.label = label
        self.class_info = class_info
        self.factory = factory

    def encode(self):
        pass

    def decode(self):
        pass

class JsonCodec:
    @staticmethod
    def default_encoding(label, o):
        return {label : o.__dict__}

    class JsonEncoder(json.JSONEncoder):
        def __init__(self, codecs, *args, **kwargs):
            json.JSONEncoder.__init__(self, *args, **kwargs)
            self.__class_to_codec = codecs

        def default(self, o):
            codec = self.__class_to_codec[type(o)]

            if codec is not None:
                assert isinstance(o, codec.class_info)
                return {codec.label : o.__dict__}
            else:
                return {'"{}"'.format(type(o)): o.__dict__}

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

    def __object_pairs_hook(self, o):
        if len(o) == 1 and o[0][0] in self.label_to_codec:
            codec = self.label_to_codec[o[0][0]]
            params = o[0][1]
            print("Making object of type {} with {}".format(o[0][0], params))
            kwarg = {kv[0] : kv[1] for kv in params}
            return codec.factory(kwarg)

        # The default is to return what was passed in
        return o

        # #if len(o) == 1 and
        # if 'horizontal_segment' in o:
        #     params = o['horizontal_segment']
        #     return FilterDescriptor.FilterDescriptor.HorizontalSegment(
        #         start_w=params['start_w'],
        #         stop_w=params['stop_w'],
        #         mag=params['mag'],
        #         weight=params['weight']
        #     )
        # print(o)
        # return o

    def __make_encoder(self, *args, **kwargs):
        je = JsonCodec.JsonEncoder(self.class_to_codec, *args, **kwargs)

        return je

    def add_encoder(self, encoder):
        pass

    def add_decoder(self, decoder):
        pass

    def get_encoder_cls(self):
        return None

    def get_decoder_cls(self):
        pass

    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=self.__make_encoder)

    def loads(self, *args, **kwargs):
        return json.loads(*args, **kwargs, object_pairs_hook=self.__object_pairs_hook)