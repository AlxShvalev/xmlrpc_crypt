from uuid import UUID
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler

from server_services import server_service
from settings import settings


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_server = ("/RPC2")


server = SimpleXMLRPCServer(
    (settings.SERVER_HOST, settings.SERVER_PORT),
    requestHandler=RequestHandler,
    allow_none=True
)


class ServerMethods:
    def auth(self, username, password):
        user = server_service.get_user(username, password)
        return server_service.create_session(user)

    def get_partial_key(self, session_id: UUID, pub_keys) -> int:
        return server_service.get_partial_key(session_id, pub_keys)

    def get_challenge(self, session_id: UUID) -> str:
        return server_service.get_challenge(session_id)

    def shutdown(self):
        server.shutdown()


server.register_introspection_functions()
server.register_instance(ServerMethods())
