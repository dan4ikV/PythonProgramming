import pytest

class BadRequestTypeError(Exception):
    def __init__(self, message="Request type is non-existent"):
        self.message = message
        super().__init__(message)


class BadHTTPVersionError(Exception):
    def __init__(self, message="HTTP version is non-existent "):
        self.message = message
        super().__init__(message)


class HTTPRequest:
    def __init__(self, method, source, protocol):
        self.method = method
        self.source = source
        self.protocol = protocol

    @classmethod
    def from_string(self, request_string):
        try:
            divided = request_string.split(" ")
            if divided.__len__() != 3:
                raise IndexError
            if not self.is_request_type(self, divided[0]):
                raise BadRequestTypeError(divided[0])
            if not divided[1].startswith("/"):
                raise ValueError
            if not self.is_http_version(self, divided[2]):
                raise BadHTTPVersionError(divided[2])
            return HTTPRequest(divided[0], divided[1], divided[2])
        except IndexError:
            return None

    def is_request_type(self, method):
        if method.lower() == 'get' or method.lower() == 'post' or method.lower() == 'put' or method.lower() == 'delete':
            return True
        return False

    def is_http_version(self, version):
        if version.lower() == 'http1.0' or version.lower() == 'http1.1' or version.lower() == 'http2.0':
            return True
        return False

    def __str__(self):
        return self.method + " " + self.source + " " + self.protocol

    def http_method(self):
        return self.method

    def http_source(self):
        return self.source

    def http_protocol(self):
        return self.protocol


def test_http_request_1():
    with pytest.raises(AttributeError):
        HTTPRequest.from_string(1)


def test_http_request2():
    assert type(HTTPRequest.from_string("GET / HTTP1.1")) is HTTPRequest


def test_http_request3():
    res = HTTPRequest.from_string("GET / HTTP1.1")
    assert res.method == 'GET' and res.source == '/' and res.protocol == 'HTTP1.1'


@pytest.mark.parametrize("method, source, protocol", [("GET", "/", "HTTP1.1"), ("POST", "/asd", "HTTP2.0")])
def test_http_request4(method, source, protocol):
    res = HTTPRequest.from_string(f'{method} {source} {protocol}')
    assert res.method == method and res.source == source and res.protocol == protocol


def test_http_request_5():
    assert HTTPRequest.from_string("GET /") is None
    assert HTTPRequest.from_string("GET / HTTP1.0 D") is None


def test_http_request_6():
    with pytest.raises(BadRequestTypeError):
        HTTPRequest.from_string("version / HTTP1.1")


def test_http_request_7():
    with pytest.raises(BadHTTPVersionError):
        HTTPRequest.from_string("GET / HTTP1")


def test_http_request_8():
    with pytest.raises(ValueError):
        HTTPRequest.from_string("GET asd HTTP1.0")


HTTPRequest.from_string("GET / HTTP1.1")