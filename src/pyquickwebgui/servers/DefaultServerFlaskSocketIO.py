from .BaseDefaultServer  import BaseDefaultServer


class DefaultServerFlaskSocketIO(BaseDefaultServer):
    @staticmethod
    def get_server_kwargs(**kwargs):
        return {
            "app": kwargs.get("app"),
            "flask_socketio": kwargs.get("flask_socketio"),
            "port": kwargs.get("port"),
        }

    @staticmethod
    def server(**server_kwargs):
        server_kwargs["flask_socketio"].run(
            server_kwargs["app"], port=server_kwargs["port"]
        )


