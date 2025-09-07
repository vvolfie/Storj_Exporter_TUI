from ast import Continue
from select import select
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Select, Static
from textual.containers import Horizontal, Container, Vertical, Center
from utils import *
import asyncio

class NodeExporter2Bash(App):
    # Textual TUI application for browsing Storj Node Exporter data.
    # This app provides multiple tabs to visualize exporter connectivity,
    # node information, disk metrics, and satellite details. Background
    # tasks periodically fetch and refresh metrics without blocking the UI.
    # TUI FOR NODE EXPORTER

    def __init__(self):  # Initialize static variables (UI state only)
        super().__init__()
        self.static_ip = ""
        self.static_port = ""
        self.node_data = {"wallet": "N/A", "nodeID": "N/A", "version": "N/A", "quic": "N/A",}
        self.disk_metrics_data = {"used": "N/A", "available": "N/A", "trash": "N/A",}
        self.satellite_saltlake = {"satellitename": "N/A", "storageSummary": "N/A", "bandwidthSummary": "N/A", "egressSummary": "N/A", "ingressSummary": "N/A", "disqualified": "N/A", "suspended": "N/A",}
        self.sat_info_saltlake = {"satellitename": "N/A", "storageSummary": "N/A", "bandwidthSummary": "N/A", "egressSummary": "N/A", "ingressSummary": "N/A", "disqualified": "N/A", "suspended": "N/A", "monthly_egress_repair": "N/A", "monthly_egress_audit": "N/A", "monthly_egress_usage": "N/A", "monthly_ingress_repair": "N/A", "monthly_ingress_usage": "N/A",}
        self.sat_info_eu1 = {"satellitename": "N/A", "storageSummary": "N/A", "bandwidthSummary": "N/A", "egressSummary": "N/A", "ingressSummary": "N/A", "disqualified": "N/A", "suspended": "N/A", "monthly_egress_repair": "N/A", "monthly_egress_audit": "N/A", "monthly_egress_usage": "N/A", "monthly_ingress_repair": "N/A", "monthly_ingress_usage": "N/A",}
        self.sat_info_ap1 = {"satellitename": "N/A", "storageSummary": "N/A", "bandwidthSummary": "N/A", "egressSummary": "N/A", "ingressSummary": "N/A", "disqualified": "N/A", "suspended": "N/A", "monthly_egress_repair": "N/A", "monthly_egress_audit": "N/A", "monthly_egress_usage": "N/A", "monthly_ingress_repair": "N/A", "monthly_ingress_usage": "N/A",}
        self.sat_info_us1 = {"satellitename": "N/A", "storageSummary": "N/A", "bandwidthSummary": "N/A", "egressSummary": "N/A", "ingressSummary": "N/A", "disqualified": "N/A", "suspended": "N/A", "monthly_egress_repair": "N/A", "monthly_egress_audit": "N/A", "monthly_egress_usage": "N/A", "monthly_ingress_repair": "N/A", "monthly_ingress_usage": "N/A",}
        self.payout = {"egressBandwidth": "N/A", "egressBandwidthPayout": "N/A", "egressRepairAudit": "N/A", "egressRepairAuditPayout": "N/A", "diskSpace": "N/A", "diskSpacePayout": "N/A", "heldRate": "N/A", "payout": "N/A", "held": "N/A", "currentMonthExpectations": "N/A",}
        
        self.connection_status = False
        self.background_task = None
        self.current_tab = None
##########################################
    def compose(self) -> ComposeResult:  # Compose the app layout
        # Builds the initial application layout and static widgets.
        # Returns the header/title, tab buttons, a placeholder body container
        # (that will host tab content), and a footer with connection status
        # and author credit.
        ##### App title and header #####
        apptitle = Static("Node Exporter TUI")
        apptitle.styles.text_align = "center"
        apptitle.styles.background = "black"
        apptitle.styles.color = "white"
        apptitle.styles.bold = True   
        yield apptitle

        ##### Body #####
        with Horizontal():
            yield Button("Node Exporter Info", id="nodexinfo", variant="primary")
            yield Button("Node Info", id="nodeInfo", variant="primary")
            yield Button ("Disk Metrics", id="diskmetrics", variant="primary" )
            yield Button ("Satellites", id="satellites", variant="primary")
            yield Button ("Payout",id="payout", variant="primary")
            yield Button ("About", id="about", variant="primary")

        self.popup = self.popup_container() # Popup to configure Node Exporter IP and Port
        self.body = Container(self.popup)
        yield self.body


        ##### Footer #####
        self.status = Static(f"Waiting for connection...")
        self.status.styles.background = "black"
        self.status.styles.text_align = "center"


        author = Static(f"By W0lf13", id="author")
        author.styles.text_align = "center"
        author.styles.background = "black"
        author.styles.color = "white"
        yield self.status
        yield author 
        

#### TABS ####
    def about_tab(self):
        self.current_tab = "about"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        title = Static(" ******** About ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"

        about_text = Static("""This TUI application allows you to monitor your Storj Node Exporter service.
It provides multiple tabs to visualize exporter connectivity, node information, disk metrics, and satellite details.
The application is built using the Textual framework and runs in your terminal.
Uses the /metrics endpoint of the Node Exporter service by anclrii to fetch data.
Developed by W0lf13 - https://github.com/vvolfie
                            """)
        
        about_text.styles.padding = (1,2)
        about_text.styles.text_align = "center"
        
        self.body.mount(title, about_text)



    async def node_exporter_info_tab(self):  # Container for Node Exporter Info TAB
        # Render the Node Exporter connectivity tab.
        # Shows current ONLINE/OFFLINE state, configured IP/Port and a
        # framed info box. The content is updated by the background refresher.
        self.current_tab = "node_exporter_info"
        self.body.remove_children()
        self.body.styles.height = "70%"
        self.body.styles.width = "100%"

        #Grab values from static variables
        ip_value = self.static_ip
        port_value = self.static_port

        #Title Styles
        title = Static(" ******** Node Exporter Service Info ********")
        title.styles.bold = True
        title.styles.text_align = "center"

        #Container Elements
        ip_static = Static(f"IP: {ip_value}")
        port_static = Static(f"Port: {port_value}")

        if self.connection_status:
            status = Static("ONLINE")
        else:
            status = Static("OFFLINE")

        info_box = Container(
            title,
            status,
            ip_static,
            port_static,
        )
        #Container Styles
        info_box.styles.border = ("round", "green")
        info_box.styles.padding = (1,2)
        info_box.styles.margin = 0
        info_box.styles.width = 75
        info_box.styles.min_height = 5
        info_box.styles.max_height = 9

        centered_infobox = Center(info_box)

        self.status_static = status

        self.body.mount(centered_infobox)

##########################################
    async def payout_tab(self):
        self.current_tab = "payout"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        #Title Styles
        title = Static(" ******** Payout ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"

        #Info Elements

        payout_info = self.payout

        self.payout_egressbandwidth_static = Static(f"\nEgress Bandwidth: {payout_info["egressBandwidth"]}")
        self.payout_egressbandwidthpayout_static = Static(f"Egress Bandwidth Payout: {payout_info["egressBandwidthPayout"]} USD")
        self.payout_egressrepairaudit_static = Static(f"Egress Repair Audit: {payout_info["egressRepairAudit"]}")
        self.payout_egressrepairauditpayout_static = Static(f"Egress Repair Audit Payout: {payout_info["egressRepairAuditPayout"]} USD")
        self.payout_diskspace_static = Static(f"\nDisk Space: {payout_info["diskSpace"]}")
        self.payout_diskspacepayout_static = Static(f"Disk Space Payout: {payout_info["diskSpacePayout"]} USD")
        self.payout_heldrate_static = Static(f"\nHeld Rate: {payout_info["heldRate"]}")
        self.payout_payout_static = Static(f"Payout: {payout_info["payout"]} USD")
        self.payout_held_static = Static(f"Held: {payout_info["held"]} USD")
        self.payout_currentmonthexpectations_static = Static(f"Current Month Expectations: {payout_info["currentMonthExpectations"]} USD")



        payout_container = Container(
            self.payout_egressbandwidth_static,
            self.payout_egressbandwidthpayout_static,
            self.payout_egressrepairaudit_static,
            self.payout_egressrepairauditpayout_static,
            self.payout_diskspace_static,
            self.payout_diskspacepayout_static,
            self.payout_heldrate_static,
            self.payout_payout_static,
            self.payout_held_static,
            self.payout_currentmonthexpectations_static,
        )

        payout_container.styles.margin = (1,2)
        payout_container.styles.padding = (1,2)
        payout_container.styles.border = ("round", "green")


        self.body.mount(title, payout_container)

##########################################
    async def node_info(self):  # Container for Node Info TAB
        # Render the Node Info tab with wallet, nodeID, version and QUIC.
        self.current_tab = "node_info"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        node_info = self.node_data

        #Title Styles
        title = Static(" ******** Node Info ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"


        #Container Elements
        wallet_static = Static(f"Wallet: {node_info['wallet']}")
        nodeid_static = Static(f"NodeID: {node_info['nodeID']}")
        version_static = Static(f"Version: {node_info['version']}")
        quic_static = Static(f"QUIC: {node_info['quic']}")

        

        info_container = Container(
            wallet_static,
            nodeid_static,
            version_static,
            quic_static,
        )

        info_container.styles.margin = (1, 2)
        info_container.styles.padding = (1,2)
        info_container.styles.border = ("round", "green")

        self.body.mount(title)
        self.body.mount(info_container)
##########################################

    async def disk_metrics(self):
        # Render the Disk Metrics tab with textual chart and values.
        # The ASCII chart is computed from the current `disk_metrics_data` and
        # is refreshed periodically by the background task while this tab is
        # active.
        # Misc
        self.current_tab = "disk_metrics"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        disk_metrics = self.disk_metrics_data


        #Title Styles
        title = Static(" ******** Disk Metrics ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"



        #Container Elements
        used_disk_static = Static(f'Used Space: {disk_metrics["used"]} GB')
        available_disk_static = Static(f'Available Space: N/A GB')    
        trash_in_disk_static = Static(f"Trash: {disk_metrics["trash"]} GB")

        # Chart generation (ASCII bars). Values are parsed defensively.
        try:
            # Extract values
            used_val = float(disk_metrics["used"].split()[0])
            available_val = float(disk_metrics["available"].split()[0])
            trash_val = float(disk_metrics["trash"].split()[0])
            
            
            total_disk = used_val + available_val
            
            # Graph bars
            used_bars = "░" * max(1, int((used_val / total_disk) * 40))  
            available_bars = "░" * max(1, int(((available_val - used_val)/ total_disk) * 40))  
            trash_bars = "░" * max(1, int((trash_val / total_disk) * 40))  
            
            # Chart
            chart_text = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                           DISK USAGE CHART                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Used:      [{used_bars:<40}] {used_val:>8.3f} GB       ║
║  Available: [{available_bars:<40}] {available_val-used_val:>8.3f} GB       ║
║  Trash:     [{trash_bars:<40}] {trash_val:>8.2f} GB       ║
╚══════════════════════════════════════════════════════════════════════════╝
            """
            
            chart_widget = Static(chart_text)
            chart_widget.styles.padding = (1, 2) 
            chart_widget.styles.text_align = "center"
            
           
            self.chart_widget = chart_widget
            
        except Exception as e:
            print(f"DEBUG: Error creating chart = {e}")
            chart_widget = Static("Chart not available")
            self.chart_widget = chart_widget
            
        self.disk_used_static = used_disk_static
        self.available_disk_static = available_disk_static
        self.trash_in_disk_static = trash_in_disk_static

        disk_metrics_container = Container(
            used_disk_static,
            available_disk_static,
            trash_in_disk_static,
            chart_widget,
        )

        disk_metrics_container.styles.margin = (1,2)
        disk_metrics_container.styles.padding = (1,2)
        disk_metrics_container.styles.border = ("round", "green")


        self.body.mount(title)
        self.body.mount(disk_metrics_container)

##########################################
    async def sat_eu1(self):
        # Render the EU1 satellite detail view with metrics and status.
        # Misc
        self.current_tab = "sat_eu1"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        #Title Styles
        title = Static(" ******** EU1 Info ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"

        button_return = Button("RETURN", id="but_sat_return", variant="primary")

        stripe = Static("")
        stripe.styles.background = "black"
        stripe.styles.width = 2
        stripe.styles.height = "100%"

        # Grab current satellite info snapshot
        eu1 = self.sat_info_eu1

        self.eu1_sat_name_static = Static(f"\nSatellite: {eu1["satellitename"]}")
        self.eu1_sat_storagesum_static = Static(f"Storage Summary: {eu1["storageSummary"]} GB")
        self.eu1_sat_bandwithsum_static =  Static(f"Bandwith Summary: {eu1["bandwidthSummary"]} GB")
        self.eu1_sat_egresssum_static = Static(f"Egress Summary: {eu1["egressSummary"]} GB")
        self.eu1_sat_ingresssum_static = Static(f"Ingress Summary: {eu1["ingressSummary"]} GB")
        self.eu1_sat_disqualified_static = Static(f"Disqualified Status: {eu1["disqualified"]}")
        self.eu1_sat_suspended_static = Static(f"Suspended Status: {eu1["suspended"]}")
        self.eu1_sat_month_egress_repair_static = Static(f"\nMonthly Egress Repair: {eu1["monthly_egress_repair"]} GB")
        self.eu1_sat_month_egress_audit_static = Static(f"Monthly Egress Audit: {eu1["monthly_egress_audit"]} GB")
        self.eu1_sat_month_egress_usage_static = Static(f"Monthly Egress Usage: {eu1["monthly_egress_usage"]} GB")
        self.eu1_sat_month_ingress_repair_static = Static(f"\nMonthly Ingress Repair: {eu1["monthly_ingress_repair"]} GB")
        self.eu1_sat_month_ingress_usage_static = Static(f"Monthly Ingress Usage: {eu1["monthly_ingress_usage"]} GB") 



        # Satellite info container (labels on the right panel)
        container = Container(
            self.eu1_sat_name_static,
            self.eu1_sat_storagesum_static,
            self.eu1_sat_bandwithsum_static,
            self.eu1_sat_egresssum_static,
            self.eu1_sat_ingresssum_static,
            self.eu1_sat_disqualified_static,
            self.eu1_sat_suspended_static,

            self.eu1_sat_month_egress_repair_static,
            self.eu1_sat_month_egress_audit_static,
            self.eu1_sat_month_egress_usage_static,

            self.eu1_sat_month_ingress_repair_static,
            self.eu1_sat_month_ingress_usage_static
            
        )

        #Container Styles
        container.styles.margin = (1,2)
        container.styles.padding = (1,2)

        row = Horizontal(
            button_return,
            stripe,
            container,
        )

        self.body.mount(title, row)

######################        
    async def sat_saltlake(self):
        # Render the Saltlake satellite detail view with metrics and status.
        # Misc
        self.current_tab = "sat_saltlake"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        #Title Styles
        title = Static(" ******** Saltlake Info ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"

        button_return = Button("RETURN", id="but_sat_return", variant="primary")

        stripe = Static("")
        stripe.styles.background = "black"
        stripe.styles.width = 2
        stripe.styles.height = "100%"

        # Grab current satellite info snapshot
        saltlake = self.sat_info_saltlake

        self.saltlake_sat_name_static = Static(f"Satellite: {saltlake["satellitename"]}")
        self.saltlake_sat_storagesum_static = Static(f"Storage Summary: {saltlake["storageSummary"]} GB")
        self.saltlake_sat_bandwithsum_static =  Static(f"Bandwith Summary: {saltlake["bandwidthSummary"]} GB")
        self.saltlake_sat_egresssum_static = Static(f"Egress Summary: {saltlake["egressSummary"]} GB")
        self.saltlake_sat_ingresssum_static = Static(f"Ingress Summary: {saltlake["ingressSummary"]} GB")
        self.saltlake_sat_disqualified_static = Static(f"Disqualified Status: {saltlake["disqualified"]}")
        self.saltlake_sat_suspended_static = Static(f"Suspended Status: {saltlake["suspended"]}")
        self.saltlake_sat_month_egress_repair_static = Static(f"Monthly Egress Repair: {saltlake["monthly_egress_repair"]} GB")
        self.saltlake_sat_month_egress_audit_static = Static(f"Monthly Egress Audit: {saltlake["monthly_egress_audit"]} GB")
        self.saltlake_sat_month_egress_usage_static = Static(f"Monthly Egress Usage: {saltlake["monthly_egress_usage"]} GB")
        self.saltlake_sat_month_ingress_repair_static = Static(f"Monthly Ingress Repair: {saltlake["monthly_ingress_repair"]} GB")
        self.saltlake_sat_month_ingress_usage_static = Static(f"Monthly Ingress Usage: {saltlake["monthly_ingress_usage"]} GB")


        # Satellite info container (labels on the right panel)
        container = Container(
            self.saltlake_sat_name_static,
            self.saltlake_sat_storagesum_static,
            self.saltlake_sat_bandwithsum_static,
            self.saltlake_sat_egresssum_static,
            self.saltlake_sat_ingresssum_static,
            self.saltlake_sat_disqualified_static,
            self.saltlake_sat_suspended_static,
            self.saltlake_sat_month_egress_repair_static,
            self.saltlake_sat_month_egress_audit_static,
            self.saltlake_sat_month_egress_usage_static,
            self.saltlake_sat_month_ingress_repair_static,
            self.saltlake_sat_month_ingress_usage_static,
            
        )

        #Container Styles
        container.styles.margin = (1,2)
        container.styles.padding = (1,2)
        container.styles.border = ("round", "green")


        row = Horizontal(
            button_return,
            stripe,
            container,
        )

        self.body.mount(title, row)

############
    async def sat_us1(self):
        #
        # Misc
        self.current_tab = "sat_us1"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        # Style
        title = Static(" ******** US1 Info ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"

        #Buttons and Misc
        button_return = Button("RETURN", id="but_sat_return", variant="primary")

        stripe = Static("")
        stripe.styles.background = "black"
        stripe.styles.width = 2
        stripe.styles.height = "100%"

        # Grabs info from exporter
        us1 = self.sat_info_us1

        self.us1_sat_name_static = Static(f"Satellite: {us1['satellitename']}")
        self.us1_sat_storagesum_static = Static(f"Storage Summary: {us1['storageSummary']} GB")
        self.us1_sat_bandwithsum_static = Static(f"Bandwith Summary: {us1['bandwidthSummary']} GB")
        self.us1_sat_egresssum_static = Static(f"Egress Summary: {us1['egressSummary']} GB")
        self.us1_sat_ingresssum_static = Static(f"Ingress Summary: {us1['ingressSummary']} GB")
        self.us1_sat_disqualified_static = Static(f"Disqualified Status: {us1['disqualified']}")
        self.us1_sat_suspended_static = Static(f"Suspended Status: {us1['suspended']}")
        self.us1_sat_month_egress_repair_static = Static(f"Monthly Egress Repair: {us1['monthly_egress_repair']} GB")
        self.us1_sat_month_egress_audit_static = Static(f"Monthly Egress Audit: {us1['monthly_egress_audit']} GB")
        self.us1_sat_month_egress_usage_static = Static(f"Monthly Egress Usage: {us1['monthly_egress_usage']} GB")
        self.us1_sat_month_ingress_repair_static = Static(f"Monthly Ingress Repair: {us1['monthly_ingress_repair']} GB")
        self.us1_sat_month_ingress_usage_static = Static(f"Monthly Ingress Usage: {us1['monthly_ingress_usage']} GB")

        # container for labels
        container = Container(
            self.us1_sat_name_static,
            self.us1_sat_storagesum_static,
            self.us1_sat_bandwithsum_static,
            self.us1_sat_egresssum_static,
            self.us1_sat_ingresssum_static,
            self.us1_sat_disqualified_static,
            self.us1_sat_suspended_static,

            self.us1_sat_month_egress_repair_static,
            self.us1_sat_month_egress_audit_static,
            self.us1_sat_month_egress_usage_static,

            self.us1_sat_month_ingress_repair_static,
            self.us1_sat_month_ingress_usage_static,
        )

        #Container Styles
        container.styles.margin = (1,2)
        container.styles.padding = (1,2)
        container.styles.border = ("round", "green")

        row = Horizontal(
            button_return,
            stripe,
            container,
        )

        self.body.mount(title, row)

#############
    async def sat_ap1(self):
        # Render the AP1 satellite detail view with metrics and status.
        # Misc
        self.current_tab = "sat_ap1"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        #Title Styles
        title = Static(" ******** AP1 Info ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"

        button_return = Button("RETURN", id="but_sat_return", variant="primary")

        stripe = Static("")
        stripe.styles.background = "black"
        stripe.styles.width = 2
        stripe.styles.height = "100%"

        # Grab current satellite info snapshot
        ap1 = self.sat_info_ap1

        self.ap1_sat_name_static = Static(f"Satellite: {ap1["satellitename"]}")
        self.ap1_sat_storagesum_static = Static(f"Storage Summary: {ap1["storageSummary"]} GB")
        self.ap1_sat_bandwithsum_static =  Static(f"Bandwith Summary: {ap1["bandwidthSummary"]} GB")
        self.ap1_sat_egresssum_static = Static(f"Egress Summary: {ap1["egressSummary"]} GB")
        self.ap1_sat_ingresssum_static = Static(f"Ingress Summary: {ap1["ingressSummary"]} GB")
        self.ap1_sat_disqualified_static = Static(f"Disqualified Status: {ap1["disqualified"]}")
        self.ap1_sat_suspended_static = Static(f"Suspended Status: {ap1["suspended"]}")
        self.ap1_sat_month_egress_repair_static = Static(f"Monthly Egress Repair: {ap1["monthly_egress_repair"]} GB")
        self.ap1_sat_month_egress_audit_static = Static(f"Monthly Egress Audit: {ap1["monthly_egress_audit"]} GB")
        self.ap1_sat_month_egress_usage_static = Static(f"Monthly Egress Usage: {ap1["monthly_egress_usage"]} GB")
        self.ap1_sat_month_ingress_repair_static = Static(f"Monthly Ingress Repair: {ap1["monthly_ingress_repair"]} GB")
        self.ap1_sat_month_ingress_usage_static = Static(f"Monthly Ingress Usage: {ap1["monthly_ingress_usage"]} GB")


        # Satellite info container (labels on the right panel)
        container = Container(
            self.ap1_sat_name_static,
            self.ap1_sat_storagesum_static,
            self.ap1_sat_bandwithsum_static,
            self.ap1_sat_egresssum_static,
            self.ap1_sat_ingresssum_static,
            self.ap1_sat_disqualified_static,
            self.ap1_sat_suspended_static,
            self.ap1_sat_month_egress_repair_static,
            self.ap1_sat_month_egress_audit_static,
            self.ap1_sat_month_egress_usage_static,
            self.ap1_sat_month_ingress_repair_static,
            self.ap1_sat_month_ingress_usage_static
            
        )
       
        #Container Styles
        container.styles.margin = (1,2)
        container.styles.padding = (1,2)
        container.styles.border = ("round", "green")

        row = Horizontal(
            button_return,
            stripe,
            container,
        )

        self.body.mount(title, row)

##########################################
    def sattelites_tab(self):
        # Render the Satellites hub tab with navigation buttons.
        # Misc
        self.current_tab = "satellites"
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        #Title Styles
        title = Static(" ******** Satellites Info ********")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"
        
        button_saltlake = Button("SALTLAKE", id="sat_saltlake", variant="primary")
        button_AP1 = Button("AP1", id="sat_ap1", variant="primary")
        button_EU1 = Button("EU1", id="sat_eu1", variant="primary")
        button_US1 = Button("US1", id="sat_us1", variant="primary")

        stripe = Static("")
        stripe.styles.background = "black"
        stripe.styles.width = 2
        stripe.styles.height = "100%"


        buttons = Vertical(
            button_saltlake,
            button_AP1,            
            button_EU1,
            button_US1,            
        )

        # Container with buttons and separator line
        left_panel = Horizontal(
            buttons,
            stripe,
        )
        left_panel.styles.width = 17  # Fixed width to hold buttons + separator

        row = Horizontal(
            left_panel,
        )

        self.body.mount(title, row)
##########################################

    #### POPUPS ####
    def popup_container(self):  # Hidden Popup for initial config that shows up on startup
        # Create the initial configuration popup for IP and Port input.
        
        pop_title =  Static("NODE EXPORTER TUI CONFIGURATION")
        pop_title.styles.padding = (1,2)


        ip_input =  Input(placeholder="Enter Node Exporter Service IP: ", id='ip_input')
        port_input = Input(placeholder="Enter Node Exporter Service Port: ", id='port_input')
        sub_button = Button("Submit", id="submit_button")
        sub_button.styles.margin = (2, 2)


        self.popup = Container(
            # Popup Elements
            pop_title,
            ip_input,
            port_input,
            sub_button
        )
        

        # Popup Styles
        self.popup.styles.background = "black"
        self.popup.styles.padding = (0,2)
        self.popup.styles.border = ("heavy", "white")     
        self.popup.visible = False

        return self.popup
##########################################

    async def on_mount(self):  # Show popup on startup
        # Display configuration popup and start the background fetcher.
        self.popup.visible = True  # For initial config
        self.background_task = asyncio.create_task(self.background_data_fetcher())  # Starts task after popup

##########################################
    #### EVENT HANDLER ####
    async def on_button_pressed(self, event: Button.Pressed):  # Event Handlers for buttons
        # Handle all button clicks from the header and tab content.

        if event.button.id == "submit_button":
            ip = self.query_one("#ip_input").value
            port = self.query_one("#port_input").value
            self.static_ip = ip
            self.static_port = port
            self.log(f"Node Exporter IP: {self.static_ip}, Port: {self.static_port}")  # Logs
            self.popup.visible = False

        #Whenver a button is pressed:
        elif event.button.id == "nodexinfo":
            await self.node_exporter_info_tab()
        elif event.button.id == "nodeInfo":
            await self.node_info()
        elif event.button.id == "diskmetrics":
            await self.disk_metrics()
        elif event.button.id == "satellites":
            self.sattelites_tab()
        elif event.button.id == "sat_saltlake":
            await self.sat_saltlake()
        elif event.button.id == "but_sat_return":
              self.sattelites_tab()
        elif event.button.id == "sat_ap1":
            await self.sat_ap1()
        elif event.button.id == "sat_eu1":
            await self.sat_eu1()
        elif event.button.id == "sat_us1":
            await self.sat_us1()
        elif event.button.id == "payout":
            await self.payout_tab()
        elif event.button.id == "about":
            self.about_tab()

##########################################        
    async def background_data_fetcher(self):  # Fetches Data in the background
        # Background loop to test connectivity and refresh metrics.
        # Runs every second, updating in-memory state and refreshing UI widgets
        # on the active tab if they are mounted.
        while True:
            try:
                self.connection_status = await self.test_connection_to_storj_exporter()

                if self.connection_status:
                    loop = asyncio.get_running_loop()
                    metrics = await loop.run_in_executor(
                        None, get_storj_metrics, self.static_ip, self.static_port
                    )
                    if metrics:
                        try:
                            self.sat_info_eu1, self.disk_metrics_data, self.node_data ,self.sat_info_ap1,self.sat_info_saltlake, self.sat_info_us1, self.payout = parse_storj_metrics(metrics)
                        except Exception as e:
                            print(f"Error parsing metrics: {e}")
                            # Keep default values if there's an error
                            pass

                self._set_footer_status(self.connection_status)

                try:
                    # Node Exporter Info tab: update ONLINE/OFFLINE label
                    if self.current_tab == "node_exporter_info" and hasattr(self, 'status_static'):
                        if self.connection_status:
                            self.status_static.update(f"ONLINE")
                        else:
                            self.status_static.update(f"OFFLINE")
                    ########
                    # Satellites (Saltlake) labels
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_name_static"):
                        self.saltlake_sat_name_static.update(f"\nSatellite: {self.sat_info_saltlake['satellitename']}")

                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_storagesum_static"):
                        self.saltlake_sat_storagesum_static.update(f"Storage Summary: {self.sat_info_saltlake['storageSummary']} GB")
                    
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_bandwithsum_static"):
                        self.saltlake_sat_bandwithsum_static.update(f"Bandwith Summary: {self.sat_info_saltlake['bandwidthSummary']} GB")
                    
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_egresssum_static"):
                        self.saltlake_sat_egresssum_static.update(f"Egress Summary: {self.sat_info_saltlake['egressSummary']} GB")
                    
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_ingresssum_static"):
                        self.saltlake_sat_ingresssum_static.update(f"Ingress Summary: {self.sat_info_saltlake['ingressSummary']} GB")
                    
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_disqualified_static"):
                        self.saltlake_sat_disqualified_static.update(f"Disqualified Status: {self.sat_info_saltlake['disqualified']}")
                    
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_suspended_static"):
                        self.saltlake_sat_suspended_static.update(f"Suspended Status: {self.sat_info_saltlake['suspended']}")

                    # Monthly Egress Stats
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_month_egress_repair_static"):
                        self.saltlake_sat_month_egress_repair_static.update(f"\nMonthly Egress Repair: {self.sat_info_saltlake['monthly_egress_repair']} GB")

                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_month_egress_audit_static"):
                        self.saltlake_sat_month_egress_audit_static.update(f"Monthly Egress Audit: {self.sat_info_saltlake['monthly_egress_audit']} GB")

                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_month_egress_usage_static"):
                        self.saltlake_sat_month_egress_usage_static.update(f"Monthly Egress Usage: {self.sat_info_saltlake['monthly_egress_usage']} GB")
                    # Monthly Ingress Stats
                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_month_ingress_repair_static"):
                        self.saltlake_sat_month_ingress_repair_static.update(f"\nMonthly Ingress Repair: {self.sat_info_saltlake['monthly_ingress_repair']} GB")

                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_month_ingress_audit_static"):
                        self.saltlake_sat_month_ingress_audit_static.update(f"Monthly Ingress Audit: {self.sat_info_saltlake['monthly_ingress_audit']} GB")

                    if self.current_tab == "sat_saltlake" and hasattr(self, "saltlake_sat_month_ingress_usage_static"):
                        self.saltlake_sat_month_ingress_usage_static.update(f"Monthly Ingress Usage: {self.sat_info_saltlake['monthly_ingress_usage']} GB")




                    ############


                    #EU1 labels

                    if self.current_tab == "sat_eu1" and hasattr(self, "\neu1_sat_name_static"):
                        self.eu1_sat_name_static.update(f"Satellite: {self.sat_info_eu1['satellitename']}")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_storagesum_static"):
                        self.eu1_sat_storagesum_static.update(f"Storage Summary: {self.sat_info_eu1['storageSummary']} GB")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_bandwithsum_static"):
                        self.eu1_sat_bandwithsum_static.update(f"Bandwith Summary: {self.sat_info_eu1['bandwidthSummary']} GB")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_egresssum_static"):
                        self.eu1_sat_egresssum_static.update(f"Egress Summary: {self.sat_info_eu1['egressSummary']} GB")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_ingresssum_static"):
                        self.eu1_sat_ingresssum_static.update(f"Ingress Summary: {self.sat_info_eu1['ingressSummary']} GB")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_disqualified_static"):
                        self.eu1_sat_disqualified_static.update(f"Disqualified Status: {self.sat_info_eu1['disqualified']}")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_suspended_static"):
                        self.eu1_sat_suspended_static.update(f"Suspended Status: {self.sat_info_eu1['suspended']}")


                    if self.current_tab == "sat_eu1" and hasattr(self, "\neu1_sat_month_egress_repair_static"):
                        self.eu1_sat_month_egress_repair_static.update(f"Monthly Egress Repair: {self.sat_info_eu1['monthly_egress_repair']} GB")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_month_egress_audit_static"):
                        self.eu1_sat_month_egress_audit_static.update(f"Monthly Egress Audit: {self.sat_info_eu1['monthly_egress_audit']} GB")
                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_month_egress_usage_static"):
                        self.eu1_sat_month_egress_usage_static.update(f"Monthly Egress Usage: {self.sat_info_eu1['monthly_egress_usage']} GB")
                

                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_month_ingress_repair_static"):
                        self.eu1_sat_month_ingress_repair_static.update(f"\nMonthly Ingress Repair: {self.sat_info_eu1['monthly_ingress_repair']} GB")


                    if self.current_tab == "sat_eu1" and hasattr(self, "eu1_sat_month_ingress_usage_static"):
                        self.eu1_sat_month_ingress_usage_static.update(f"Monthly Ingress Usage: {self.sat_info_eu1['monthly_ingress_usage']} GB")


                    ###########

                    # US1 labels

                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_name_static"):
                        self.us1_sat_name_static.update(f"\nSatellite: {self.sat_info_us1['satellitename']}")
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_storagesum_static"):
                        self.us1_sat_storagesum_static.update(f"Storage Summary: {self.sat_info_us1['storageSummary']} GB")
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_bandwithsum_static"):
                        self.us1_sat_bandwithsum_static.update(f"Bandwith Summary: {self.sat_info_us1['bandwidthSummary']} GB")
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_egresssum_static"):
                        self.us1_sat_egresssum_static.update(f"Egress Summary: {self.sat_info_us1['egressSummary']} GB")
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_ingresssum_static"):
                        self.us1_sat_ingresssum_static.update(f"Ingress Summary: {self.sat_info_us1['ingressSummary']} GB")
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_disqualified_static"):
                        self.us1_sat_disqualified_static.update(f"Disqualified Status: {self.sat_info_us1['disqualified']}")
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_suspended_static"):
                        self.us1_sat_suspended_static.update(f"Suspended Status: {self.sat_info_us1['suspended']}")


                    # Monthly Egress Stats
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_month_egress_repair_static"):
                        self.us1_sat_month_egress_repair_static.update(f"\nMonthly Egress Repair: {self.sat_info_us1['monthly_egress_repair']} GB")

                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_month_egress_audit_static"):
                        self.us1_sat_month_egress_audit_static.update(f"Monthly Egress Audit: {self.sat_info_us1['monthly_egress_audit']} GB")

                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_month_egress_usage_static"):
                        self.us1_sat_month_egress_usage_static.update(f"Monthly Egress Usage: {self.sat_info_us1['monthly_egress_usage']} GB")

                    # Monthly Ingress Stats
                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_month_ingress_repair_static"):
                        self.us1_sat_month_ingress_repair_static.update(f"\nMonthly Ingress Repair: {self.sat_info_us1['monthly_ingress_repair']} GB")


                    if self.current_tab == "sat_us1" and hasattr(self, "us1_sat_month_ingress_usage_static"):
                        self.us1_sat_month_ingress_usage_static.update(f"Monthly Ingress Usage: {self.sat_info_us1['monthly_ingress_usage']} GB")



                    ####

                    # (AP1) labels
                    
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_name_static"):
                        self.ap1_sat_name_static.update(f"\nSatellite: {self.sat_info_ap1["satellitename"]}")

                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_storagesum_static"):
                        self.ap1_sat_storagesum_static.update(f"Storage Summary: {self.sat_info_ap1["storageSummary"]} GB")
                        
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_bandwithsum_static"):
                        self.ap1_sat_bandwithsum_static.update(f"Bandwith Summary: {self.sat_info_ap1["bandwidthSummary"]} GB")
                    
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_bandwithsum_static"):
                            self.ap1_sat_bandwithsum_static.update(f"Bandwith Summary: {self.sat_info_ap1["bandwidthSummary"]} GB")

                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_egresssum_static"):
                            self.ap1_sat_egresssum_static.update(f"Egress Summary: {self.sat_info_ap1["egressSummary"]} GB")
                    
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_ingresssum_static" ):
                            self.ap1_sat_ingresssum_static.update(f"Ingress Summary: {self.sat_info_ap1["ingressSummary"]} GB")
                        
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_disqualified_static"):    
                            self.ap1_sat_disqualified_static.update(f"Disqualified Status: {self.sat_info_ap1["disqualified"]}")
                        
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_suspended_static" ):
                        self.ap1_sat_suspended_static.update(f"Suspended Status: {self.sat_info_ap1["suspended"]}")
                    

                    # Monthly Egress Stats
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_month_egress_repair_static"):
                        self.ap1_sat_month_egress_repair_static.update(f"\nMonthly Egress Repair: {self.sat_info_ap1["monthly_egress_repair"]} GB")

                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_month_egress_audit_static"):
                        self.ap1_sat_month_egress_audit_static.update(f"Monthly Egress Audit: {self.sat_info_ap1["monthly_egress_audit"]} GB")

                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_month_egress_usage_static"):
                        self.ap1_sat_month_egress_usage_static.update(f"Monthly Egress Usage: {self.sat_info_ap1["monthly_egress_usage"]} GB")

                    # Monthly Ingress Stats
                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_month_ingress_repair_static"):
                        self.ap1_sat_month_ingress_repair_static.update(f"\nMonthly Ingress Repair: {self.sat_info_ap1["monthly_ingress_repair"]} GB")

                    if self.current_tab == "sat_ap1" and hasattr(self, "ap1_sat_month_ingress_usage_static"):
                        self.ap1_sat_month_ingress_usage_static.update(f"Monthly Ingress Usage: {self.sat_info_ap1["monthly_ingress_usage"]} GB")

                    ##########################
                    #Payout Labels

                    if self.current_tab == "payout" and hasattr(self, "payout_egressbandwidth_static"):
                        self.payout_egressbandwidth_static.update(f"\nEgress Bandwidth: {self.payout["egressBandwidth"]}")

                    if self.current_tab == "payout" and hasattr(self, "payout_egressbandwidthpayout_static"):
                        self.payout_egressbandwidthpayout_static.update(f"Egress Bandwidth Payout: {self.payout["egressBandwidthPayout"]} USD")

                    if self.current_tab == "payout" and hasattr(self, "payout_egressrepairaudit_static"):
                        self.payout_egressrepairaudit_static.update(f"Egress Repair Audit: {self.payout["egressRepairAudit"]}")

                    if self.current_tab == "payout" and hasattr(self, "payout_egressrepairauditpayout_static"):
                        self.payout_egressrepairauditpayout_static.update(f"Egress Repair Audit Payout: {self.payout["egressRepairAuditPayout"]} USD")

                    if self.current_tab == "payout" and hasattr(self, "payout_diskspace_static"):
                        self.payout_diskspace_static.update(f"\nDisk Space: {self.payout["diskSpace"]}")

                    if self.current_tab == "payout" and hasattr(self, "payout_diskspacepayout_static"):
                        self.payout_diskspacepayout_static.update(f"Disk Space Payout: {self.payout["diskSpacePayout"]} USD")

                    if self.current_tab == "payout" and hasattr(self, "payout_heldrate_static"):
                        self.payout_heldrate_static.update(f"\nHeld Rate: {self.payout["heldRate"]}")

                    if self.current_tab == "payout" and hasattr(self, "payout_payout_static"):
                        self.payout_payout_static.update(f"Payout: {self.payout["payout"]} USD")

                    if self.current_tab == "payout" and hasattr(self, "payout_held_static"):
                        self.payout_held_static.update(f"Held: {self.payout["held"]} USD")

                    if self.current_tab == "payout" and hasattr(self, "payout_currentmonthexpectations_static"):
                        self.payout_currentmonthexpectations_static.update(f"Current Month Expectations: {self.payout["currentMonthExpectations"]} USD")

                    ##########################

                    
                    ######################

                    # Disk Metrics
                    if self.current_tab == "disk_metrics" and hasattr(self, "disk_used_static"):
                        self.disk_used_static.update(f"Used Space: {self.disk_metrics_data["used"]} GB")

                    if self.current_tab == "disk_metrics" and hasattr(self, "available_disk_static"):
                        # Use real data from Node Exporter
                        self.available_disk_static.update(f"Available Space: {self.disk_metrics_data["available"]} GB")
                    
                    if self.current_tab == "disk_metrics" and hasattr(self, "trash_in_disk_static"):
                        self.trash_in_disk_static.update(f"Trash: {self.disk_metrics_data["trash"]} GB")


                    if self.current_tab == "disk_metrics" and hasattr(self, "chart_widget"):
                        try:
                            # Recompute chart bars on live updates
                            
                            used_val = float(self.disk_metrics_data["used"].split()[0])
                            available_val = float(self.disk_metrics_data["available"].split()[0])
                            trash_val = float(self.disk_metrics_data["trash"].split()[0])
                            
                            
                            total_disk = used_val + available_val
                            
                            
                            used_bars = "░" * max(1, int((used_val / total_disk) * 40)) 
                            available_bars = "░" * max(1, int(((available_val - used_val) / total_disk) * 40)) 
                            trash_bars = "░" * max(1, int((trash_val / total_disk) * 40)) 
                            

                            chart_text = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                           DISK USAGE CHART                               ║
╠══════════════════════════════════════════════════════════════════════════╣
║  Used:      [{used_bars:<40}] {used_val:>8.3f} GB       ║
║  Available: [{available_bars:<40}] {available_val-used_val:>8.3f} GB       ║
║  Trash:     [{trash_bars:<40}] {trash_val:>8.2f} GB       ║
╚══════════════════════════════════════════════════════════════════════════╝
                            """
                            
                            # Update the existing widget
                            self.chart_widget.update(chart_text)
                            
                        except Exception as e:
                            print(f"DEBUG: Error loading chart = {e}")

                except:
                    pass


            except Exception as e:
                self.connection_status = False
                self._set_footer_status(False)
            
            await asyncio.sleep(1)
##########################################

    async def test_connection_to_storj_exporter(self):  # Test connection to Node Exporter
        # Check exporter reachability using current IP/Port in a thread pool.
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, test_connection_to_storj_exporter, self.static_ip, self.static_port
        )
##########################################

    def _set_footer_status(self, connected: bool):  # Footer Connection State
            # Update footer label and color according to connectivity.
            if connected:
                self.status.update("ONLINE")
                self.status.styles.color = ("green")
            else: 
                self.status.update("OFFLINE")
                self.status.styles.color = ("red")
##########################################


if __name__ == "__main__":
    NodeExporter2Bash().run()
