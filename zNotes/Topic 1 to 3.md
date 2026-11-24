
# Topic 1: Intro to Computer Networking


`Computer Network` is a collection of interconnected devices that communicate with each other to exchange data and resources.


#### Purpose of Computer Networks

1. Resource Sharing
2. Communication
3. Data Sharing
4. Centralize Management

#### Classification of Networks

1. **Personal Area Network (PAN)** - This connects personal devices within a very short range around a single user
2. **Local Area Network (LAN)** - This connects computers and devices within a limited area such as a home, office or building.
3. **Campus Area Network (CAN)** - Connects multiple LANs within a campus or a group of nearby buildings
4. **Metropolitan Area Network (MAN)** - Connects multiple networks within a city or metropolitan region
5. **Wide Area Network (WAN)** - Connects networks over large geographical areas such as countries or continents

#### Basic Networking Terminology

`Node` - Any device connected to a network (computer, printer, router).
`Host` - A device that provides or consumes network services.
`Bandwidth` - The maximum data transfer rater of a network.
`Latency` - Delay in data transfer
`Protocol` - Rules that define how data is transmitted and received

---
# Topic 2: Network Architecture

Network Architecture is the design and structure of a computer network including its physical components, logical organization and communication protocols.

#### Components of a Network

1. **Network Devices(Hardware):**
	- **Router** - Connects multiple networks and directs data between them
	- **Switch** - Connects devices within the same network and manages internal data communication
	- **Hub** - Acts as a basic device that connects multiple devices with a network
	- **Access Point (AP)** - Provides wireless connectivity to devices in a network
	- **Network Interface Card (NIC)** - A hardware in computers to connect to the network

2. **Transmission Media** 
	- **Physical cables:** Ethernet cables(Cat5e, Cat6), fiber optics
	- **Wireless:** Wi-Fi, Bluetooth, microwave links
	- Example: Fiber optic cables in a city MAN for high-speed data

3. **End Devices:**
	- Computers, laptops, printers, IP phones, servers- basically anything that sends or receives data

4. **Networking Software & Protocols:**
	- Operating systems, network management software and protocols that govern communication

#### Network Protocols

They define rules for data formatting, addressing, transmission, and error handling. Without protocols, devices
wouldn’t understand each other.

##### Examples of Protocol Types

1. `Communication Protocols:` Rules for exchanging data(e.g, TCP/IP).
2. `Routing Protocol:`  Help routers find the best path (e.g OSPF, BGP)
3. `Security Protocols:` Encrypt and protect data(e.g HTTPS, SSL/TLS)


#### The OSI Model (Open Systems Interconnection)

Is a 7-layer framework used to understand and design network communication. Each layer has a clearly defined function and works independently of the others


| Layer           | Purpose                            | Example                  |
| --------------- | ---------------------------------- | ------------------------ |
| 7. Application  | User-facing application & services | HTTP, FTP, Email         |
| 6. Presentation | Data translation, encryption       | JPEG, SSL, TLS           |
| 5. Session      | Managing sessions/connections      | API calls, video calls   |
| 4. Transport    | Reliable/unreliable delivery       | TCP(reliable), UDP(fast) |
| 3. Network      | Routing & addressing               | IP, ICMP                 |
| 2. Data Link    | MAC addressing, frame delivery     | Ethernet, Switches       |
| 1. Physical     | Physical medium & Signals          | Cabels, Wi-Fi            |

#### Network Topologies

##### Mesh Topology

In a mesh topology, every device is connected to another device via a particular channel. Every device is connected to another via dedicated channels. These channels are known as links. Mesh topology does not depend on specific protocols; it focuses on direct device-to-device connections.

**Advantages**
- Communication is very fast between the nodes.
- Mesh Topology is robust.
- The fault is diagnosed easily. Data is reliable because data is transferred among the devices through dedicated channels or links.
- Provides security and privacy.
    
**Disadvantages**
- Installation and configuration are difficult.
- The cost of cables is high as bulk wiring is required, hence suitable for less number of devices.
- The cost of maintenance is high.


##### Star Topology

In Star Topology, all the devices are connected to a single hub through a cable. This hub is the central node and all other nodes are connected to the central node. The hub can be passive in nature i.e., not an intelligent hub such as broadcasting devices, at the same time the hub can be intelligent known as an active hub. Active hubs have repeaters in them.

**Advantages**
- If N devices are connected to each other in a star topology, then the number of cables required to connect them is N. So, it is easy to set up.
- Each device requires only 1 port i.e. to connect to the hub, therefore the total number of ports required is N.
- It is Robust. If one link fails only that link will affect and not other than that.
- Easy to fault identification and fault isolation.
- Star topology is cost-effective as it uses inexpensive coaxial cable.

**Disadvantages**
- If the concentrator (hub) on which the whole topology relies fails, the whole system will crash down.
- The cost of installation is high.
- Performance is based on the single concentrator i.e. hub.

##### Bus Topology

Bus Topology is a network type in which every computer and network device is connected to a single cable. It is bi-directional. It is a multi-point connection and a non-robust topology because if the backbone fails the topology crashes. IBus-topology Ethernet uses only the CSMA/CD MAC protocol. TDMA, CDMA, Pure ALOHA, and Slotted ALOHA were never used in Ethernet.


**Advantages**

- If N devices are connected to each other in a bus topology, then the number of cables required to connect them is 1, known as backbone cable, and N drop lines are required.
- Coaxial or twisted pair cables are mainly used in bus-based networks that support up to 10 Mbps.
- The cost of the cable is less compared to other topologies, but it is used to build small networks.
- Bus topology is familiar technology as installation and troubleshooting techniques are well known.
- CSMA/CD was the only MAC method used in traditional bus Ethernet. Modern switched Ethernet does not use CSMA/CD because full-duplex operation eliminates collisions.
    
**Disadvantages**
- A bus topology is quite simpler, but still, it requires a lot of cabling.
- If the common cable fails, then the whole system will crash down.
- If the network traffic is heavy, it increases collisions in the network. To avoid this, various protocols are used in the MAC layer known as Pure Aloha, Slotted Aloha, CSMA/CD, etc.
- Adding new devices to the network would slow down networks.
- Security is very low.


**Ring Topology**

In a Ring Topology, it forms a ring connecting devices with exactly two neighboring devices. A number of repeaters are used for Ring topology with a large number of nodes, because if someone wants to send some data to the last node in the ring topology with 100 nodes, then the data will have to pass through 99 nodes to reach the 100th node. Hence to prevent data loss repeaters are used in the network.


**Advantages**
- The data transmission is high-speed.
- The possibility of collision is minimum in this type of topology.
- Cheap to install and expand.

**Disadvantages**
- The failure of a single node in the network can cause the entire network to fail.
- Troubleshooting is difficult in this topology.
- Less secure.


**Tree Topology**

Tree topology is the variation of the Star topology. This topology has a hierarchical flow of data. In Tree Topology, protocols like [DHCP](https://www.geeksforgeeks.org/computer-networks/dynamic-host-configuration-protocol-dhcp/) and SAC (Standard Automatic Configuration) are used.

- Here, various secondary hubs are connected to the central hub which contains the repeater.
- This data flow from top to bottom i.e. from the central hub to the secondary and then to the devices or from bottom to top i.e. devices to the secondary hub and then to the central hub. 
- It is a [multi-point connection](https://www.geeksforgeeks.org/computer-networks/differences-between-point-to-point-and-multi-point-communication/) and a non-robust topology because if the backbone fails the topology crashes.
    

**Advantages**
- It allows more devices to be attached to a single central hub thus it decreases the distance that is traveled by the signal to come to the devices.
- It allows the network to get isolated and also prioritize from different computers.
- We can add new devices to the existing network.

**Disadvantages**
- If the central hub gets fails the entire system fails.
- The cost is high because of the cabling.
- If new devices are added, it becomes difficult to reconfigure.

---

# Topic 3: Media Access Protocols and Data-link Control

We are focusing on media access control (MAC) protocols and the Data Link Control

In networking, Media Access Control (MAC) protocols serve as the traffic rules for devices sharing a communication medium.

While, Data-Link Control ensures that data is packaged, transmitted, and received correctly between devices on the same network segment

#### Media Access Control (MAC)

MAC is part of the `data-link layer` (Layer 2) in the OSI model. It defines how multiple devices share a communication medium without interfering with each other.

#### Types of MAC Methods

1. **Contention-Based (Random Access) Methods**
	Devices "compete" for access to the network. Think of it like multiple people trying to speak in a group conversation.
	- CSMA (Carrier Sense Multiple Access):
		- Devices first "listen" to see if the medium is free
		- If the line is busy, the device waits a random amount of time before trying again.
		- Variants: CSMA/CD (Collision Detection) for Ethernet, CSMA/CA (Collision Avoidance) for Wi-Fi

2. **Controlled Access Methods**
	Devices take turns or are granted permission to transmit. Think of a teacher calling on students one at a time.

	- **Polling:** A central controller ask each device if it wants to send data.
	- **Token Passing:** A `token` circulates the network; only the device with the token can transmit

#### Why MAC Matters
• Prevents collisions when multiple devices try to send data at the same time.
• Ensures fairness—all devices get a chance to transmit.
• Optimizes network efficiency by reducing wasted bandwidth.

#### Data-Link Control

Data-Link Control is responsible for error detection, flow control, and framing. While MAC decides who can talk, data-link control ensures the message is delivered correctly

Key Functions

1. **Framing:**
	o Converts raw bits from the physical layer into meaningful frames for
	transmission.
	o A frame includes: header, payload (actual data), and trailer (for error
	checking).
	o Example: Ethernet frames contain source and destination MAC addresses
	and error-checking info.

2. **Error Detection and Correction:**
	o Parity Check: Simple method—adds a parity bit to detect errors.
	o Cyclic Redundancy Check (CRC): More robust, used in Ethernet.
	o If errors are detected, frames can be retransmitted.

3. **Flow Control:**
	o Ensures a fast sender doesn’t overwhelm a slow receiver.
	o Example: Stop-and-Wait protocol—sender waits for acknowledgment after each frame.


#### End-to-End Connection Methods

Networks also differ in how they handle the path data takes from source to destination.

1. **Circuit Switching**
	- A dedicated communication path is established before data is sent.
	- Think of it as a reserved private road for your data.
	- Pros: Consistent speed and guaranteed delivery.
	- Cons: Inefficient—resources are wasted if no data is sent.
	- Example: Traditional telephone networks.
2. **Packet Switching** 
	- Data is broken into small packets, each taking the best available route to the destination.
	- Think of it as sending multiple parcels through the postal system—they may take different routes but arrive eventually.
	- Pros: Efficient use of bandwidth, scalable.
	- Cons: Variable delivery times, potential packet loss.
	- Example: The Internet.

#### Practical Example: Office LAN
Imagine a small office with 5 computers connected via Ethernet (LAN):

1. Each computer listens to the network before sending data (CSMA/CD).
2. Data is packaged into frames, with MAC addresses indicating sender and receiver.
3. If two computers transmit at the same time, a collision is detected, and both re-transmit after a random delay.
4. Error-checking mechanisms ensure files and emails are delivered correctly
5. If the office connects to the Internet, data is routed via packet switching, while internal communication uses circuit-like LAN connections.