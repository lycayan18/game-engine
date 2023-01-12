import sys

from game.client.main import main as client_main
from game.server.main import main as server_main
from game.client.UI.menu import menu

if len(sys.argv) <= 1:
    print("Help:")
    print("\t--server [IP:PORT] - Tells game to create a new server")
    print("\t--client [IP:PORT] - Tells game to connect to the server")
    menu()
else:
    if sys.argv[1] == "--server":
        ip, port = sys.argv[2].split(':')

        server_main(ip, int(port))
    elif sys.argv[1] == '--client':
        ip, port = sys.argv[2].split(':')

        client_main(ip, int(port))
    else:
        print(f"Unknown parameter \"{sys.argv[1]}\"")
