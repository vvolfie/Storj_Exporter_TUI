from ast import Continue
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static
from textual.containers import Horizontal, Container, Vertical, Center
from utils import *
import asyncio

class NodeExporter2Bash(App):
    #TUI FOR NODE EXPORTER

    def __init__(self):# Initialize static variables
        super().__init__()
        self.static_ip = ""
        self.static_port = ""

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
            yield Button("Node Exporter Info", id="nodeInfo", variant="primary")

        self.popup = self.popup_container() # Popup to configure Node Exporter IP and Port
        self.body = Container(self.popup)
        yield self.body


        ##### Footer #####
        author = Static("By W0lf13", id="author")
        author.styles.text_align = "center"
        author.styles.background = "black"
        author.styles.color = "white"
        yield author

    async def test_connection_to_storj_exporter(self):#Test connection to Node Exporter
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, test_connection_to_storj_exporter, self.static_ip, self.static_port
        )

    async def node_exporter_info_tab(self):# Container for Node Exporter Info Body
        self.body.remove_children()
        self.body.styles.height = "70%"
        self.body.styles.width = "100%"

        #Grab values from static variables
        ip_value = self.static_ip
        port_value = self.static_port

        #Title Styles
        title = Static(" ******** Node Exporter Service Info ********", id="title")
        title.styles.bold = True
        title.styles.text_align = "center"

        #Container Elements
        status = Static(f"\nEstablishing Connection...")
        ip_static = Static(f"IP: {ip_value}")
        port_static = Static(f"Port: {port_value}")

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

        self.body.mount(centered_infobox)

        #Sleep to not block UI
        await asyncio.sleep(0)
        connected = await self.test_connection_to_storj_exporter() #Test connection
        #Update status after connection test
        status.update(
            f"\nStatus: {'Online' if connected else 'OFFLINE - Connection to Node Exporter couldnt be established!'}"
        )

    async def node_info(self): # Container for Node Info Body
        
        self.body.remove_children()
        self.body.styles.height = "85%"
        self.body.styles.width = "100%"

        node_info = {
            "wallet": "N/A",
            "nodeID": "N/A",
            "version": "N/A",
        }

        #Tests connection and get metrics
        loop = asyncio.get_running_loop()
        status = await self.test_connection_to_storj_exporter()

        if (status):
            metrics = await loop.run_in_executor(
                None, get_storj_metrics, self.static_ip , self.static_port
            )
            if (metrics):
                node_info = await loop.run_in_executor(
                    None, parse_storj_metrics, metrics
                )

        #Title Styles
        title = Static(" ******** Node Info ********", id="title")
        title.styles.bold = True
        title.styles.text_align = "center"
        title.styles.background = "black"
        title.styles.color = "white"


        #Container Elements
        wallet_static = Static(f"Wallet: {node_info['wallet']}")
        nodeid_static = Static(f"NodeID: {node_info['nodeID']}")
        version_static = Static(f"Version: {node_info['version']}")

        info_container = Container(
            title,
            wallet_static,
            nodeid_static,
            version_static,
        )

        self.body.mount(info_container)

    def popup_container(self):# Hidden Popup for initial config that shows up on startup
        

        self.popup = Container(
            # Popup Elements
            Static("NODE EXPORTER TUI CONFIGURATION"),
            Input(placeholder="Enter Node Exporter Service IP: ", id='ip_input'),
            Input(placeholder="Enter Node Exporter Service Port: ", id='port_input'),
            Button("Submit", id="submit_button"),
        )

        # Popup Styles
        self.popup.styles.background = "black"
        self.popup.styles.padding = (0,2)
        self.popup.styles.border = ("heavy", "white")     
        self.popup.visible = False

        
        return self.popup

    async def on_mount(self):# Show popup on startup
        self.popup.visible = True # For initial config

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
            








if __name__ == "__main__":
    NodeExporter2Bash().run()