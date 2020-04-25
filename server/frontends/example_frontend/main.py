from server.shellman import ShellmanCore


class ShellmanFrontend:
    def __init__(self):
        pass

    async def on_connection(self, connection):
        print(f"example_frontend: connection {connection.id} received, listening")
        connection.add_frontend(self)

    async def on_read(self, connection, data):
        print(f'example_frontend: received data from connection {connection.id}: {data} - sending back the same')
        await connection.write(data, self)

    async def on_disconnect(self, connection):
        print(f'example_frontend: {connection.id} disconnected :(')

    async def on_write_by_other(self, connection, data):
        print(f'example_frontend: another frontend wrote {data} to {connection.id}')
