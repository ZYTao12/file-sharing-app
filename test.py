import argparse
from sender import send_file_chunk
from receiver import start_server as start_receiver
from tracker import app as tracker_app

def main():
    parser = argparse.ArgumentParser(description="File Sharing System")
    subparsers = parser.add_subparsers(dest="command")

    # Sender command
    sender_parser = subparsers.add_parser("send", help="Send a file")
    sender_parser.add_argument("file", help="Path to the file to send")
    sender_parser.add_argument("tracker", help="Tracker URL")
    sender_parser.add_argument("port", type=int, help="Target port for sending the file")

    # Receiver command
    receiver_parser = subparsers.add_parser("receive", help="Receive files")
    receiver_parser.add_argument("--host", default="0.0.0.0", help="Host address to listen on")
    receiver_parser.add_argument("--port", type=int, default=5000, help="Port to listen on")

    # Tracker command
    tracker_parser = subparsers.add_parser("track", help="Run the tracker server")
    tracker_parser.add_argument("--port", type=int, default=5000, help="Port to run the tracker on")

    args = parser.parse_args()

    if args.command == "send": 
        send_file_chunk(args.file, args.tracker, args.port)
    elif args.command == "receive":
        start_receiver(args.host, args.port)
    elif args.command == "track":
        tracker_app.run(debug=True, host='0.0.0.0', port=args.port)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
