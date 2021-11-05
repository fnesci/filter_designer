import json_io
import math


def default_json_encoding(label, o):
    return {label: o.__dict__}


class FilterDescriptor:
    """
    This class describes the idea filter response
    """

    # There are multiple segment types
    # Horizontal
    # Line
    # Spline

    # Segments will be sorted by start freq and then stop freq
    # if multiple segments overlap, the minimum value will be used
    # Gaps in the frequency response are unconstrained and
    # the filter generation algorithm can do anything with
    # these undefined gaps
    #
    # The linear_phase boolean is a hint that the
    # algorithm should attempt to make the filter
    # have linear phase through the defined regions

    @staticmethod
    def get_json_codecs():
        codecs = [
            json_io.DefaultClassCodec('filter_descriptor', FilterDescriptor, FilterDescriptor.__json_factory),
            FilterDescriptor.HorizontalSegment.get_json_codecs(),
            FilterDescriptor.LinearSegment.get_json_codecs()
        ]

        # encoders = [
        #     (FilterDescriptor, lambda o: default_json_encoding("filter_descriptor", o)),
        #     (FilterDescriptor.HorizontalSegment, lambda o: default_json_encoding("horizontal_segment", o)),
        #     (FilterDescriptor.LinearSegment, lambda o: default_json_encoding("linear_segment", o))
        # ]
        # decoders = [
        #     ("filter_descriptor", FilterDescriptor.json_factory)
        # ]

        return codecs

    @staticmethod
    def __json_factory(json):
        return FilterDescriptor(**json)

    class HorizontalSegment:
        @staticmethod
        def get_json_codecs():
            return json_io.DefaultClassCodec('horizontal_segment', FilterDescriptor.HorizontalSegment,
                                             FilterDescriptor.HorizontalSegment.__json_factory)

        @staticmethod
        def __json_factory(json):
            return FilterDescriptor.HorizontalSegment(**json)

        def __init__(self, start_w, stop_w, mag, weight=1.0):
            self.start_w = start_w
            self.stop_w = stop_w
            self.mag = mag
            self.weight = weight

        def render_to(self, num_points, response, weights):
            start = math.floor(num_points * (0.5 * (self.start_w + math.pi) / math.pi + 0.5))
            stop = math.floor(num_points * (0.5 * (self.stop_w + math.pi) / math.pi + 0.5)) + 1
            for i in range(start, stop):
                if i >= num_points:
                    i -= num_points

                if math.isnan(response[i]) or self.mag < response[i]:
                    response[i] = self.mag
                    weights[i] = self.weight

    class LinearSegment:
        @staticmethod
        def get_json_codecs():
            return json_io.DefaultClassCodec('linear_segment', FilterDescriptor.LinearSegment,
                                             FilterDescriptor.LinearSegment.__json_factory)

        @staticmethod
        def __json_factory(json):
            return FilterDescriptor.LinearSegment(**json)

        def __init__(self, start_w, start_mag, stop_w, stop_mag, weight = 1.0):
            self.start_w = start_w
            self.start_mag = start_mag
            self.stop_w = stop_w
            self.stop_mag = stop_mag
            self.weight = weight

    def __init__(self, segments = [], linear_phase = False):
        self.segments = segments
        self.linear_phase = linear_phase

    def render(self, num_points):
        """

        :param points:
        :return:
        """

        # Calculate the frequencies that will be used
        # to define the filter
        ws = [(-math.pi + 2.0 * math.pi * i / num_points) for i in range(num_points)]

        # Calculate the frequency response
        # Nans will be used for undefined regions
        response = [float('nan')] * num_points
        weights = [float('nan')] * num_points

        for segment in self.segments:
            segment.render_to(num_points, response, weights)