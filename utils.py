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
        "monthly_egress_repair": "N/A",
        "monthly_egress_audit": "N/A",
        "monthly_egress_usage": "N/A",
        "monthly_ingress_repair": "N/A",
        "monthly_ingress_audit": "N/A",
        "monthly_ingress_usage": "N/A",
    }

    satellite_info_ap1 = {
        "satellitename": "N/A",
        "storageSummary": "N/A",
        "bandwidthSummary": "N/A",
        "egressSummary": "N/A",
        "ingressSummary": "N/A",
        "disqualified": "N/A",
        "suspended": "N/A",
        "monthly_egress_repair": "N/A",
        "monthly_egress_audit": "N/A",
        "monthly_egress_usage": "N/A",
        "monthly_ingress_repair": "N/A",
        "monthly_ingress_audit": "N/A",
        "monthly_ingress_usage": "N/A",
    }

    satellite_info_us1 = {
        "satellitename": "N/A",
        "storageSummary": "N/A",
        "bandwidthSummary": "N/A",
        "egressSummary": "N/A",
        "ingressSummary": "N/A",
        "disqualified": "N/A",
        "suspended": "N/A",
        "monthly_egress_repair": "N/A",
        "monthly_egress_audit": "N/A",
        "monthly_egress_usage": "N/A",
        "monthly_ingress_repair": "N/A",
        "monthly_ingress_audit": "N/A",
        "monthly_ingress_usage": "N/A",
    }
    satellite_info_eu1 = {
        "satellitename": "N/A",
        "storageSummary": "N/A",
        "bandwidthSummary": "N/A",
        "egressSummary": "N/A",
        "ingressSummary": "N/A",
        "disqualified": "N/A",
        "suspended": "N/A",
        "monthly_egress_repair": "N/A",
        "monthly_egress_audit": "N/A",
        "monthly_egress_usage": "N/A",
        "monthly_ingress_repair": "N/A",
        "monthly_ingress_audit": "N/A",
        "monthly_ingress_usage": "N/A",
    }

    payout = {
        "egressBandwidth": "N/A",
        "egressBandwidthPayout": "N/A",
        "egressRepairAudit": "N/A",
        "egressRepairAuditPayout": "N/A",
        "diskSpace": "N/A",
        "diskSpacePayout": "N/A",
        "heldRate": "N/A",
        "payout": "N/A",
        "held": "N/A",
        "currentMonthExpectations": "N/A",                 
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
        #saltlake.tardigrade.io:7777
        if "storj_sat_summary" in line:
            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line:
                    satellite_info_saltlake["satellitename"] = line.split('url="')[1].split('"')[0]

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "storageSummary" in line:
                satellite_info_saltlake["storageSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "bandwidthSummary" in line:
                satellite_info_saltlake["bandwidthSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "egressSummary" in line:
                satellite_info_saltlake["egressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "1wFTAgs9DP5RSnCqKV1eLf6N9wtk4EAtmN5DpSxcs8EjT69tGE" in line and "ingressSummary" in line:
                satellite_info_saltlake["ingressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

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

        #ap1.storj.io:7777
        if "storj_sat_summary" in line:
            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line:
                    satellite_info_ap1["satellitename"] = line.split('url="')[1].split('"')[0]

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "storageSummary" in line:
                satellite_info_ap1["storageSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "bandwidthSummary" in line:
                satellite_info_ap1["bandwidthSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "egressSummary" in line:
                satellite_info_ap1["egressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "121RTSDpyNZVcEU84Ticf2L1ntiuUimbWgfATz21tuvgk3vzoA6" in line and "ingressSummary" in line:
                satellite_info_ap1["ingressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

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
                satellite_info_us1["storageSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "bandwidthSummary" in line:
                satellite_info_us1["bandwidthSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "egressSummary" in line:
                satellite_info_us1["egressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "12EayRS2V1kEsWESU9QMRseFhdxYxKicsiFmxrsLZHeLUtdps3S" in line and "ingressSummary" in line:
                satellite_info_us1["ingressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

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
                satellite_info_eu1["storageSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "bandwidthSummary" in line:
                satellite_info_eu1["bandwidthSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "egressSummary" in line:
                satellite_info_eu1["egressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

            if "12L9ZFwhzVpuEKMUNUqkaTLGzwY9G24tbiigLiXpmZWKwmcNDDs" in line and "ingressSummary" in line:
                satellite_info_eu1["ingressSummary"] = f"{float(line.split()[-1]) / (1024**3):.2f}"

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

        #Monthly Egress Stats
        if "storj_sat_month_egress" in line:
            #Repair
            if 'type="repair"' in line:
                if "saltlake" in line:
                    try:
                        satellite_info_saltlake["monthly_egress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_saltlake["monthly_egress_repair"] = line.split()[-1]
                elif "ap1" in line:
                    try:
                        satellite_info_ap1["monthly_egress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_ap1["monthly_egress_repair"] = line.split()[-1]
                elif "us1" in line:
                    try:
                        satellite_info_us1["monthly_egress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_us1["monthly_egress_repair"] = line.split()[-1]
                elif "eu1" in line:
                    try:
                        satellite_info_eu1["monthly_egress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_eu1["monthly_egress_repair"] = line.split()[-1]
            #Audit
            if 'type="audit"' in line:
                if "saltlake" in line:
                    try:
                        satellite_info_saltlake["monthly_egress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_saltlake["monthly_egress_audit"] = line.split()[-1]
                elif "ap1" in line:
                    try:
                        satellite_info_ap1["monthly_egress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_ap1["monthly_egress_audit"] = line.split()[-1]
                elif "us1" in line:
                    try:
                        satellite_info_us1["monthly_egress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_us1["monthly_egress_audit"] = line.split()[-1]
                elif "eu1" in line:
                    try:
                        satellite_info_eu1["monthly_egress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_eu1["monthly_egress_audit"] = line.split()[-1]
            #Usage
            if 'type="usage"' in line:
                if "saltlake" in line:
                    try:
                        satellite_info_saltlake["monthly_egress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_saltlake["monthly_egress_usage"] = line.split()[-1]
                elif "ap1" in line:
                    try:
                        satellite_info_ap1["monthly_egress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_ap1["monthly_egress_usage"] = line.split()[-1]
                elif "us1" in line:
                    try:
                        satellite_info_us1["monthly_egress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_us1["monthly_egress_usage"] = line.split()[-1]
                elif "eu1" in line:
                    try:
                        satellite_info_eu1["monthly_egress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_eu1["monthly_egress_usage"] = line.split()[-1]
        #Monthly Ingress
        if "storj_sat_month_ingress" in line:
            #Repair
            if 'type="repair"' in line:
                if "saltlake" in line:
                    try:
                        satellite_info_saltlake["monthly_ingress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_saltlake["monthly_ingress_repair"] = line.split()[-1]
                elif "ap1" in line:
                    try:
                        satellite_info_ap1["monthly_ingress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_ap1["monthly_ingress_repair"] = line.split()[-1]
                elif "us1" in line:
                    try:
                        satellite_info_us1["monthly_ingress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_us1["monthly_ingress_repair"] = line.split()[-1]
                elif "eu1" in line:
                    try:
                        satellite_info_eu1["monthly_ingress_repair"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_eu1["monthly_ingress_repair"] = line.split()[-1]
            #Audit
            if 'type="audit"' in line:
                if "saltlake" in line:
                    try:
                        satellite_info_saltlake["monthly_ingress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_saltlake["monthly_ingress_audit"] = line.split()[-1]
                elif "ap1" in line:
                    try:
                        satellite_info_ap1["monthly_ingress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_ap1["monthly_ingress_audit"] = line.split()[-1]
                elif "us1" in line:
                    try:
                        satellite_info_us1["monthly_ingress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_us1["monthly_ingress_audit"] = line.split()[-1]
                elif "eu1" in line:
                    try:
                        satellite_info_eu1["monthly_ingress_audit"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_eu1["monthly_ingress_audit"] = line.split()[-1]
            #Usage
            if 'type="usage"' in line:
                if "saltlake" in line:
                    try:
                        satellite_info_saltlake["monthly_ingress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_saltlake["monthly_ingress_usage"] = line.split()[-1]
                elif "ap1" in line:
                    try:
                        satellite_info_ap1["monthly_ingress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_ap1["monthly_ingress_usage"] = line.split()[-1]
                elif "us1" in line:
                    try:
                        satellite_info_us1["monthly_ingress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_us1["monthly_ingress_usage"] = line.split()[-1]
                elif "eu1" in line:
                    try:
                        satellite_info_eu1["monthly_ingress_usage"] = f"{float(line.split()[-1]) / (1024**3):.2f}"
                    except:
                        satellite_info_eu1["monthly_ingress_usage"] = line.split()[-1]

        # Payout
        if "storj_payout_currentMonth" in line:
            try:
                if 'type="egressBandwidth"' in line:
                    # Convert bytes to GB for better readability
                    bytes_val = float(line.split()[-1])
                    payout["egressBandwidth"] = f"{bytes_val / (1024**3):.2f} GB"
                if 'type="egressBandwidthPayout"' in line:
                     payout["egressBandwidthPayout"] = line.split()[-1]
                if 'type="egressRepairAudit"' in line:
                    # Convert bytes to GB for better readability
                    bytes_val = float(line.split()[-1])
                    payout["egressRepairAudit"] = f"{bytes_val / (1024**3):.2f} GB"
                if 'type="egressRepairAuditPayout"' in line:
                     payout["egressRepairAuditPayout"] = line.split()[-1]
                if 'type="diskSpace"' in line:
                    # Convert bytes to GB for better readability
                    bytes_val = float(line.split()[-1])
                    payout["diskSpace"] = f"{bytes_val / (1024**3):.2f} GB"
                if 'type="diskSpacePayout"' in line:
                     payout["diskSpacePayout"] = f"{float(line.split()[-1]):.3f}"
                if 'type="heldRate"' in line:
                     payout["heldRate"] = line.split()[-1]
                if 'type="payout"' in line:
                     payout["payout"] = f"{float(line.split()[-1]):.3f}"
                if 'type="held"' in line:
                     payout["held"] = line.split()[-1]
                if 'type="currentMonthExpectations"' in line:
                     payout["currentMonthExpectations"] = line.split()[-1]
            except Exception as e:
                print(f"Error processing payout line: {line}, error: {e}")











    return satellite_info_eu1, disk_metrics, node_info, satellite_info_ap1, satellite_info_saltlake, satellite_info_us1, payout
   # satellite_info_saltlake
    # return node_info, disk_metrics satellite_info_saltlake





def display_node_info(satellite_info_saltlake):
    print(satellite_info_saltlake["monthly_egress_repair"])

    

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


