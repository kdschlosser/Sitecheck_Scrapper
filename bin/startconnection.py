class SshConnectManager(object):
    def __init__(self, host, username, password, port=22):
        self._host = host
        self._username = username
        self._password = password
        self._port = port

        self.conn = None
        # FIX HERE
        asyncio.async(self.start_connection())

    @asyncio.coroutine
    def start_connection(self):
        try:
            Client = self._create_ssh_client()
            self.conn, _ = yield from asyncssh.create_connection(Client,
                                                            self._host, port=self._port,
                                                            username=self._username,
                                                            password=self._password)
        except Exception as e:
            print("Connection error! {}".format(e))
            asyncio.async(self.start_connection())

    def _create_ssh_client(self):
        class MySSHClient(asyncssh.SSHClient):
            parent = self
            def connection_lost(self, exc):
                self.parent._handle_connection_lost(exc)
        return MySSHClient

    def _handle_connection_lost(self, exc):
        print('Connection lost on {}'.format(self.host))
        print(exc)
        # AND HERE
        asyncio.async(self.start_connection())


    ssh1 = SshConnectManager(settings.host, settings.username, settings.password, settings.port)

    asyncio.get_event_loop().run_until_complete(...)