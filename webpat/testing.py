def generate_client_fixture(app_cls, base):
    """
    :param app_cls: an app class
    :param base: a delcarative base
    :returns: a test client fixture
    """
    def client(request, tmpdir):
        f = tmpdir.join('testing.sqlite3')

        uri = 'sqlite:///' + f.strpath
        app = app_cls(__name__, uri=uri, base=base)

        app.config['TESTING'] = True

        ctx = app.test_request_context()
        ctx.push()

        def fin():
            ctx.pop()
        request.addfinalizer(fin)

        return app.test_client()
    return client
