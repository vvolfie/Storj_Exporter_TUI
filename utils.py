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
        "version": "N/A",
        "quic": "N/A"
    }
    disk_metrics = {
        "used": "N/A",
        "available": "N/A",
        "trash": "N/A",
    }

    for line in metrics.splitlines():
        if "storj_node_info" in line:
            if 'wallet="' in line:
                node_info["wallet"] = line.split('wallet="')[1].split('"')[0]
            if 'version="' in line:
                node_info["version"] = line.split('version="')[1].split('"')[0]
            if 'nodeID="' in line:
                node_info["nodeID"] = line.split('nodeID="')[1].split('"')[0]
            if 'quicStatus=' in line:
                node_info["quic"] = line.split('quicStatus="')[1].split('"')[0]
        
        if "storj_total_diskspace" in line:
            if "used" in line:
                disk_metrics["used"] = line.split('used"}')[1]
                disk_metrics["used"] = f"{float(disk_metrics["used"]) / (1000**3):.5f}"
            if "available" in line:
                 disk_metrics["available"] = line.split('available"}')[1]
                 disk_metrics["available"] = f"{float(disk_metrics["available"]) / (1000**3):.2f}"
            if "trash" in line:
                 disk_metrics["trash"] = line.split('trash"}')[1]
                 disk_metrics["trash"] = f"{float(disk_metrics["trash"]) / (1000**3):.3f}"

            print(disk_metrics["trash"])
    return node_info, disk_metrics





def display_node_info(node_info):

    print("\nNode Information:")
    print(f"Node ID:        {node_info['nodeID']}")
    print(f"Wallet Address: {node_info['wallet']}")
    print(f"Version:        {node_info['version']}")



if __name__ == "__main__":

    ################################################
    # Grab ip and port from user and test connection

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

