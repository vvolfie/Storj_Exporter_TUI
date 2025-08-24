from ast import Continue
from select import select
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Select, Static
from textual.containers import Horizontal, Container, Vertical, Center
from utils import *
import asyncio

class NodeExporter2Bash(App):
    #TUI FOR NODE EXPORTER

    def __init__(self):# Initialize static variables
        super().__init__()
        self.static_ip = ""
        self.static_port = ""
        self.node_data = {"wallet": "N/A", "nodeID": "N/A", "version": "N/A", "quic": "N/A",}
        self.disk_metrics_data = {"used": "N/A", "available": "N/A", "trash": "N/A",}
        self.satellite_saltlake = {"satellitename": "N/A", "storageSummary": "N/A", "bandwidthSummary": "N/A", "egressSummary": "N/A", "ingressSummary": "N/A", "disqualified": "N/A", "suspended": "N/A",}
        self.connection_status = False
        self.background_task = None
        self.current_tab = None

    def compose(self) -> ComposeResult: # Compose the app
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
    async def node_exporter_info_tab(self):# Container for Node Exporter Info TAB
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

    async def node_info(self): # Container for Node Info TAB
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

        self.body.mount(title)
        self.body.mount(info_container)

    async def disk_metrics(self):
        #Misc
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

        # A.I Coded this entirely had to adjust some value and create 1 small detail ai wasnt being able to do
        try:
            # Extact values
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

        self.body.mount(title)
        self.body.mount(disk_metrics_container)

##########################################


##########################################
    def sattelites_tab(self):
        #Misc
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

        vertical_container = Vertical(
            button_saltlake
        )

        self.body.mount(title, vertical_container)


    #### POPUPS ####
    def popup_container(self):# Hidden Popup for initial config that shows up on startup
        
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


    async def on_mount(self):# Show popup on startup
        self.popup.visible = True # For initial config
        self.background_task = asyncio.create_task(self.background_data_fetcher()) #Starts task after popup

    #### EVENT HANDLER ####
    async def on_button_pressed(self, event: Button.Pressed):# Event Handlers for button

        if event.button.id == "submit_button":
            ip = self.query_one("#ip_input").value
            port = self.query_one("#port_input").value
            self.static_ip = ip
            self.static_port = port
            self.log(f"Node Exporter IP: {self.static_ip}, Port: {self.static_port}") #LOGS
            self.popup.visible = False

    
        elif event.button.id == "nodexinfo":
            await self.node_exporter_info_tab()
        elif event.button.id == "nodeInfo":
            await self.node_info()
        elif event.button.id == "diskmetrics":
            await self.disk_metrics()
        elif event.button.id == "satellites":
            self.sattelites_tab()


    #### MISC ####
            
    async def background_data_fetcher(self):#Fetches Data in the background
        while True:
            try:
                self.connection_status = await self.test_connection_to_storj_exporter()

                if self.connection_status:
                    loop = asyncio.get_running_loop()
                    metrics = await loop.run_in_executor(
                        None, get_storj_metrics, self.static_ip, self.static_port
                    )
                    if metrics:
                        self.sat_info_eu1, self.disk_metrics_data, self.node_data ,self.sat_info_ap1,self.sat_info_saltlake, self.sat_info_us1 = parse_storj_metrics(metrics)

                self._set_footer_status(self.connection_status)

                try:
                    #Node Info
                    if self.current_tab == "node_exporter_info" and hasattr(self, 'status_static'):
                        if self.connection_status:
                            self.status_static.update(f"ONLINE")
                        else:
                            self.status_static.update(f"OFFLINE")

                    #Satellites

                
  
                    #Disk Metrics###
                    if self.current_tab == "disk_metrics" and hasattr(self, "disk_used_static"):
                        self.disk_used_static.update(f"Used Space: {self.disk_metrics_data["used"]} GB")

                    if self.current_tab == "disk_metrics" and hasattr(self, "available_disk_static"):
                        # Usar dados reais do Node Exporter
                        self.available_disk_static.update(f"Available Space: {self.disk_metrics_data["available"]} GB")
                    
                    if self.current_tab == "disk_metrics" and hasattr(self, "trash_in_disk_static"):
                        self.trash_in_disk_static.update(f"Trash: {self.disk_metrics_data["trash"]} GB")


                    if self.current_tab == "disk_metrics" and hasattr(self, "chart_widget"):
                        try:
                            # A.I Coded this entirely had to adjust some value and create 1 small detail ai wasnt being able to do
                            
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
                            
                            # Updates the existing widget
                            self.chart_widget.update(chart_text)
                            
                        except Exception as e:
                            print(f"DEBUG: Error loading chart = {e}")

                except:
                    pass


            except Exception as e:
                self.connection_status = False
                self._set_footer_status(False)
            
            await asyncio.sleep(1)

    async def test_connection_to_storj_exporter(self):#Test connection to Node Exporter
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, test_connection_to_storj_exporter, self.static_ip, self.static_port
        )

    def _set_footer_status(self, connected: bool): #Footer Connection State
            if connected:
                self.status.update("ONLINE")
                self.status.styles.color = ("green")
            else: 
                self.status.update("OFFLINE")
                self.status.styles.color = ("red")



if __name__ == "__main__":
    NodeExporter2Bash().run()
