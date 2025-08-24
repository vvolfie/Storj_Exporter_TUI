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
        "quic": "N/A",
    }
    disk_metrics = {
        "used": "N/A",
        "available": "N/A",
        "trash": "N/A",
    }

    satellite_info_saltlake = {
        "satellitename": "N/A",
        "storageSummary": "N/A",
        "bandwidthSummary": "N/A",
        "egressSummary": "N/A",
        "ingressSummary": "N/A",
        "disqualified": "N/A",
        "suspended": "N/A",
    }

    satellite_info_ap1 = {
        "satellitename": "N/A",
        "storageSummary": "N/A",
        "bandwidthSummary": "N/A",
        "egressSummary": "N/A",
        "ingressSummary": "N/A",
        "disqualified": "N/A",
        "suspended": "N/A",
    }

    satellite_info_us1 = {
        "satellitename": "N/A",
        "storageSummary": "N/A",
        "bandwidthSummary": "N/A",
        "egressSummary": "N/A",
        "ingressSummary": "N/A",
        "disqualified": "N/A",
        "suspended": "N/A",
    }
    satellite_info_eu1 = {
        "satellitename": "N/A",
        "storageSummary": "N/A",
        "bandwidthSummary": "N/A",
        "egressSummary": "N/A",
        "ingressSummary": "N/A",
        "disqualified": "N/A",
        "suspended": "N/A",
    }

    for line in metrics.splitlines():

        #Node Info
        if "storj_node_info" in line:
            if 'wallet="' in line:
                node_info["wallet"] = line.split('wallet="')[1].split('"')[0]
            if 'version="' in line:
                node_info["version"] = line.split('version="')[1].split('"')[0]
            if 'nodeID="' in line:
                node_info["nodeID"] = line.split('nodeID="')[1].split('"')[0]
            if 'quicStatus=' in line:
                node_info["quic"] = line.split('quicStatus="')[1].split('"')[0]

        # Disk Metrics
        
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


        #Satellites INFO

        #saltlake
        if "storj_sat_summary" in line:
            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line:
                    satellite_info_saltlake["satellitename"] = line.split('url="')[1].split('"')[0]

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "storageSummary" in line:
                    satellite_info_saltlake["storageSummary"] = line.split()[-1]

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "bandwidthSummary" in line:
                    satellite_info_saltlake["bandwidthSummary"] = line.split()[-1]

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "egressSummary" in line:
                    satellite_info_saltlake["egressSummary"] = line.split()[-1]

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "ingressSummary" in line:
                    satellite_info_saltlake["ingressSummary"] = line.split()[-1]

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "disqualified" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_saltlake["disqualified"] = "False"
                else:
                    satellite_info_saltlake["disqualified"] = "True"

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "suspended" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_saltlake["suspended"] = "False"
                else:
                    satellite_info_saltlake["suspended"] = "True"

        #ap1satellite_info_ap1
        if "storj_sat_summary" in line:
            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line:
                    satellite_info_ap1["satellitename"] = line.split('url="')[1].split('"')[0]

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "storageSummary" in line:
                    satellite_info_ap1["storageSummary"] = line.split()[-1]

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "bandwidthSummary" in line:
                    satellite_info_ap1["bandwidthSummary"] = line.split()[-1]

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "egressSummary" in line:
                    satellite_info_ap1["egressSummary"] = line.split()[-1]

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "ingressSummary" in line:
                    satellite_info_ap1["ingressSummary"] = line.split()[-1]

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "disqualified" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_ap1["disqualified"] = "False"
                else:
                    satellite_info_ap1["disqualified"] = "True"

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "suspended" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_ap1["suspended"] = "False"
                else:
                    satellite_info_ap1["suspended"] = "True"

        #us1.storj.io:7777
        if "storj_sat_summary" in line:
            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line:
                    satellite_info_us1["satellitename"] = line.split('url="')[1].split('"')[0]

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "storageSummary" in line:
                    satellite_info_us1["storageSummary"] = line.split()[-1]

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "bandwidthSummary" in line:
                    satellite_info_us1["bandwidthSummary"] = line.split()[-1]

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "egressSummary" in line:
                    satellite_info_us1["egressSummary"] = line.split()[-1]

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "ingressSummary" in line:
                    satellite_info_us1["ingressSummary"] = line.split()[-1]

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "disqualified" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_us1["disqualified"] = "False"
                else:
                    satellite_info_us1["disqualified"] = "True"

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "suspended" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_us1["suspended"] = "False"
                else:
                    satellite_info_us1["suspended"] = "True"

        #eu1.storj.io:7777
        if "storj_sat_summary" in line:
            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line:
                    satellite_info_eu1["satellitename"] = line.split('url="')[1].split('"')[0]

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "storageSummary" in line:
                    satellite_info_eu1["storageSummary"] = line.split()[-1]

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "bandwidthSummary" in line:
                    satellite_info_eu1["bandwidthSummary"] = line.split()[-1]

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "egressSummary" in line:
                    satellite_info_eu1["egressSummary"] = line.split()[-1]

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "ingressSummary" in line:
                    satellite_info_eu1["ingressSummary"] = line.split()[-1]

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "disqualified" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_eu1["disqualified"] = "False"
                else:
                    satellite_info_eu1["disqualified"] = "True"

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "suspended" in line:
                if (line.split()[-1] == "0.0"):
                    satellite_info_eu1["suspended"] = "False"
                else:
                    satellite_info_eu1["suspended"] = "True"            



    return satellite_info_eu1, disk_metrics, node_info, satellite_info_ap1, satellite_info_saltlake, satellite_info_us1
    # return node_info, disk_metrics satellite_info_saltlake





def display_node_info(satellite_info_eu1):
    print(satellite_info_eu1["satellitename"])
    print(satellite_info_eu1["storageSummary"])
    print(satellite_info_eu1["bandwidthSummary"])
    print(satellite_info_eu1["egressSummary"])
    print(satellite_info_eu1["ingressSummary"])
    print(satellite_info_eu1["disqualified"])
    print(satellite_info_eu1["suspended"])

    

    """"
    print("\nNode Information:")
    print(f"Node ID:        {node_info['nodeID']}")
    print(f"Wallet Address: {node_info['wallet']}")
    print(f"Version:        {node_info['version']}")
    """


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


