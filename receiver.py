import socket, os, requests

def start_server(host='0.0.0.0', port=5000, save_dir='received_chunks'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Listening as {host}:{port}...")

        while True:
            client_socket, address = server_socket.accept()
            print(f"Connection from {address} has been established.")

            received = client_socket.recv(1024).decode('utf-8')
            metadata, _, partial_content = received.partition('\n')
            filename, filesize = metadata.split(':', 1)
            filename = os.path.basename(filename)
            filesize = int(filesize)

            path = os.path.join(save_dir, filename)
            with open(path, 'wb') as f:
                f.write(partial_content.encode('utf-8'))
                filesize -= len(partial_content)
                while filesize > 0:
                    data = client_socket.recv(4096)
                    f.write(data)
                    filesize -= len(data)

            print(f"File {filename} has been received successfully.")
            client_socket.close()

# def download_chunk(peer_address, chunk_name, save_dir='received_chunks'):
#     """Connect to a peer and download a specific chunk."""
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect(peer_address)
#         s.sendall(chunk_name.encode())

#         # Receive and save the chunk
#         chunk_path = os.path.join(save_dir, chunk_name)
#         with open(chunk_path, 'wb') as chunk_file:
#             while True:
#                 data = s.recv(1024)
#                 if not data:
#                     break
#                 chunk_file.write(data)

# # def reconstruct_file(chunks_dir, output_file):
# #     """Reconstruct the original file from its chunks."""
# #     chunks = sorted(os.listdir(chunks_dir))
# #     with open(output_file, 'wb') as outfile:
# #         for chunk in chunks:
# #             with open(os.path.join(chunks_dir, chunk), 'rb') as chunk_file:
# #                 outfile.write(chunk_file.read())

# # Example usage
# # Assuming `get_tracker_info()` returns a list of tuples with peer addresses and chunk names
# # and `tracker_address` is the address of the tracker

# def retrieve_file_from_peers(tracker_url, file_id, save_dir='received_chunks'):
#     chunk_info = get_chunk_info_from_tracker(tracker_url, file_id)
#     if chunk_info is not None:
#         for peer_info in chunk_info:
#             peer_address, chunk_name = peer_info
#             print(f"Downloading {chunk_name} from {peer_address}...")
#             download_chunk(peer_address, chunk_name, save_dir)
#         print("All chunks downloaded successfully.")
#     else:
#         print("Could not retrieve file.")

# Note: `get_tracker_info()` is a placeholder for the actual implementation
# of the communication with the tracker to retrieve peer and chunk information.

if __name__ == "__main__":
    start_server()
