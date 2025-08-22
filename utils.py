import requests, prometheus_client


def write_ip():
    ip = input("Enter the IP address > ")
    return ip

def write_port():
    port = input("Enter the port for storj exporter > ")
    return port

def test_connection_to_storj_exporter(ip, port):
    try:
        response = requests.get(f"http://{ip}:{port}", timeout=5)
        if response.status_code == 200:
            print("[200 OK]Connection to Storj exporter successful.")
            return True
        else:
            print(f"[ERROR]Failed to connect to Storj exporter. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[ERROR]Error connecting to Storj exporter: {e}")
        return False
    

def get_storj_metrics(ip, port):
    response = requests.get(f"http://{ip}:{port}")
    if response.status_code == 200:
        metrics = response.text
        return metrics
    else:
        print(f"[ERROR]Failed to retrieve metrics. Status code: {response.status_code}")
        return None

def parse_storj_metrics(metrics):
    # valores default
    node_info = {
        "wallet": "N/A",
        "nodeID": "N/A",
        "version": "N/A"
    }

    for line in metrics.splitlines():
        if "storj_node_info" in line:
            if 'wallet="' in line:
                node_info["wallet"] = line.split('wallet="')[1].split('"')[0]
            if 'version="' in line:
                node_info["version"] = line.split('version="')[1].split('"')[0]
            if 'nodeID="' in line:
                node_info["nodeID"] = line.split('nodeID="')[1].split('"')[0]
    
    return node_info


# Functions Of Curses TUI



"""""
def display_node_info(node_info):

    print("\nNode Information:")
    print(f"Node ID:        {node_info['nodeID']}")
    print(f"Wallet Address: {node_info['wallet']}")
    print(f"Version:        {node_info['version']}")



# TUI TERMINAL USER INTERFACE
def main(stdscr):
    curses.curs_set(0) # Hide cursor
    stdscr.addstr(0, 2, "Storj Node Monitor", curses.A_BOLD)



    stdscr.refresh()
    stdscr.getch() #Wait for u input

#MAIN


if __name__ == "__main__":

    ################################################
    # Grab ip and port from user and test connection
    curses.wrapper(main)
    ip = write_ip()
    port = write_port()
    test_connection_to_storj_exporter(ip, port)
    ################################################
    # Get metrics from Storj Exporter by https://github.com/anclrii and parse them
    metrics = get_storj_metrics(ip, port)
    parsed_metrics_node_dict = parse_storj_metrics(metrics)
    
    ################################################
    # Display the parsed node information
    display_node_info(parsed_metrics_node_dict)
    ################################################

"""
