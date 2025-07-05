import socket
import threading
import logging
import msgpack
import serde
import time
import json
import base64
import player_data

def dict_to_kv_list(d):
    result = []
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_to_kv_list(v)
        result.append([k, v])
    return result

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EndpointServer")

CROSS_DOMAIN_POLICY = (
    "<cross-domain-policy>"
    '<allow-access-from domain="*" to-ports="7777"/>'
    "</cross-domain-policy>\x00"
).encode("utf-8")


class EndpointServer:
    def __init__(self, host="127.0.0.1", port=7777):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            logger.info(f"Server started on {self.host}:{self.port}")
            threading.Thread(target=self.accept_loop, daemon=True).start()
        except Exception as e:
            logger.error(f"Error starting server: {e}")
            self.stop()

    def accept_loop(self):
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                logger.info(f"New connection from {client_address}")
                threading.Thread(target=self.handle_client, args=(client_socket, client_address), daemon=True).start()
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")

    def handle_client(self, sock, addr):
        # unpacker = msgpack.Unpacker(raw=False)
        serializer = serde.BinarySerializer()
        deserializer = serde.BinaryDeserializer()

        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                logger.info(f"[{addr}] Received: {data}")

                if data.startswith(b"<policy-file-request/>"):
                    sock.sendall(CROSS_DOMAIN_POLICY)
                    logger.info(f"[{addr}] Sent cross-domain policy")
                    break

                # In the connect handler, the client writes byte 0 and immediately flushes it. Ignoring it as it is probably a new message indication.
                if data[0] == 0x00:
                    logger.info(f"[{addr}] Received x00 --- ignoring")
                    data = data[1:]
                
                logger.info(f"[{addr}] RAW HEX: {data.hex()}")
                logger.info(f"[{addr}] RAW BASE64: {base64.b64encode(data).decode()}")

                try:
                    deserialized = deserializer.deserialize(data)
                    for message in deserialized:
                        logger.info(f"[{addr}] Message item: {message}")
                except Exception as e:
                    logger.warning(f"[{addr}] Deserialization failed: {e}")
                    continue

                # Client sends join message (from API server)
                if data.startswith(b'\x87\xc4join\xcedefaultJoinKey'):
                    logger.info(f"[{addr}] Join room request received")

                    # Assume the client joined successfully
                    successful_join = True
                    if successful_join:
                        msg = ["playerio.joinresult", True]
                    else:
                        # If failed, send back PlayerIOError of type 11
                        msg = ["playerio.joinresult", False, 11, "Failed to join room: Unknown connection"]

                    try:
                        serialized = serializer.serialize(msg)
                        logger.info(f"[{addr}] Sending: {serialized}")
                        sock.sendall(serialized)

                    except Exception as e:
                        logger.error(f"[{addr}] Serialization/send failed: {e}")

                    # game ready (gr) message. Contains messageId, serverTime, binaries (config.xml), costTableData, srvTableData (survivor), loginPlayerState.
                    time.sleep(1)

                    config_path, config_uri = "DeadZone-Private-Server-main/socket_server/config.xml.gz", "xml/config.xml"
                    buildings_path, buildings_uri = "DeadZone-Private-Server-main/socket_server/buildings.xml.gz", "xml/buildings.xml"
                    res_second_path, res_second_uri = "DeadZone-Private-Server-main/socket_server/resources_secondary.xml", "xml/resources_secondary.xml"
                    alliances_path, alliances_uri = "DeadZone-Private-Server-main/socket_server/alliances.xml.gz", "xml/alliances.xml"
                    
                    msg = [
                        "gr", 
                        time.time(), 
                        player_data.generate_binaries({
                            (config_path, config_uri, True),
                            (buildings_path, buildings_uri, True),
                            (res_second_path, res_second_uri, False),
                            (alliances_path, alliances_uri, True),
                        }), 
                        player_data.generate_cost_table(), 
                        player_data.generate_srv_table(),
                        player_data.generate_login_state(), 
                    ]
                    serialized = serializer.serialize(msg)
                    logger.info(f"[{addr}] Sending: {serialized}")
                    sock.sendall(serialized)
                
                # Client sends auth message after join
                for message in deserialized:
                    if isinstance(message, list) and len(message) > 0:
                        if message[0] == "auth":
                            token = message[1] if len(message) > 1 else None
                            logger.info(f"[{addr}] Auth token received: {token}")

                            auth_response = [
                                "authresult",
                                json.dumps({
                                    "playerId": "user123",
                                    "name": "TestPlayer",
                                    "level": 5,
                                    "xp": 1200,
                                    "resources": {
                                        "wood": 300,
                                        "metal": 200,
                                        "cloth": 100
                                    },
                                    "buildings": [],
                                    "inventory": [],
                                    "alliance": None
                                })
                            ]
                            try:
                                serialized = serializer.serialize(auth_response)
                                logger.info(f"[{addr}] Sending authresult: {serialized}")
                                sock.sendall(serialized)
                            except Exception as e:
                                logger.error(f"[{addr}] Failed to send authresult: {e}")

        except Exception as e:
            logger.error(f"[{addr}] Connection error: {e}")
        finally:
            sock.close()
            logger.info(f"[{addr}] Connection closed")

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception as e:
                logger.error(f"Error closing socket: {e}")
        logger.info("Server stopped")


def main():
    server = EndpointServer()
    server.start()
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    finally:
        server.stop()


if __name__ == "__main__":
    main()
