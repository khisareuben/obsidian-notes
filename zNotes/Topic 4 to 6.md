
# Topic 4: End-to-End Protocols

Imagine sending a parcel across the country. You need to:

1. Pack it properly (format data).
2. Decide on a delivery route (network layer).
3. Ensure it arrives intact (transport layer).
4. Confirm the recipient got it (acknowledgment).

In networking, `end-to-end protocols` handle all these steps. They ensure that data sent from one computer reaches another reliably, securely, and efficiently.

### Connection-Oriented vs Connectionless Protocols

#### 1. Connection-Oriented Protocols

- Establish a connection before sending data.
- Think of it like making a phone call: you dial, wait for the other person to pick up, then talk.
- Features:
	- Reliable delivery
	- Data sequencing
	- Error checking
- **Example:** TCP(Transmission Control Protocol)

##### How TCP works:
1. Three-way Handshake:
	- Sender sends SYN (synchronize)
	- Receiver replies SYN-ACK(synchronize acknowledgment)
	- Sender replies ACK
2. Data is sent in order, and the receiver confirms each packet
3. If a packet is lost, TCP re-transmits it

#### Connectionless Protocols

- No prior connection; just send packets directly.
- Think of it like sending postcards—no guarantee they’ll arrive, and no acknowledgment is expected.
- Features:
	- Faster
	- Less reliable
- Example: UDP (User Diagram Protocol)
	- Used for streaming, online gaming, or video calls where speed matters more than perfect delivery

**Protocol Components Overview**
**Protocols define:**
	• Syntax: How data is formatted
	• Semantics: What each part of the data means
	• Timing: When data is sent and how often

These rules ensure that devices can understand each other, even if they are from
different manufacturers.

#### Application Layer Protocols

The application layer (OSI Layer 7) deals with end-user services. Here are some common ones:

1. **HTTP (Hypertext Transfer Protocol):**
	o Transfers web pages from servers to browsers.
	o Example: When you open www.google.com, HTTP fetches the HTML
	content.
2. **FTP (File Transfer Protocol):**
	o Transfers files between computers over a network.
	o Example: Uploading your project files to a school server.
3. **SMTP (Simple Mail Transfer Protocol):**
	o Sends emails from client to server.
	o Example: Sending an email from Gmail.
4. **DNS (Domain Name System):**
	o Converts domain names (www.example.com) to IP addresses.
	o Example: Your browser doesn’t understand “www.google.com”—DNS
	translates it to 142.250.72.196.

#### Transport Layer Protocols

The transport layer (Layer 4) ensures reliable delivery, flow control, and congestion control.

Key Concepts

1. **Reliable vs. Unreliable Data Transfer:**
	o TCP: Reliable (checks for errors, ensures packets arrive in order)
	o UDP: Unreliable (no guarantees, faster)
2. **Flow Control:**
	o Prevents fast senders from overwhelming slow receivers.
	o Example: TCP sliding window method
3. **Congestion Control:**
	o Prevents network overload.
	o Example: TCP slows down transmission if packets are getting dropped
	due to congestion.

#### Network Layer Protocols

The network layer (Layer 3) handles addressing and routing.

1. **IPv4 (Internet Protocol version 4):**
	o Provides unique addresses to devices.
	o Example: 192.168.1.1
	o Breaks data into packets with source and destination IP addresses.
2. **ICMP (Internet Control Message Protocol):**
	o Used for network diagnostics and error messages.
	o Example: Ping command checks connectivity.

**End-to-End Example: Sending and Email**

Let's follow the path of an email from your computer to your friend's inbox

1. **Application Layer (SMTP):** You type your email and click send.
2. **Transport Layer (TCP):** Email is broken into packets, sequenced, and acknowledged.
3. **Network Layer (IP):** Packets are assigned source and destination IP addresses.
4. **Data-Link Layer (Ethernet/Wi-Fi):** Frames carry packets over your LAN to the router.
5. **Physical Layer:** Electrical signals or radio waves transmit the bits.
6. Packets travel through the internet, pass routers, and eventually reach your friend’s server.
7. TCP reassembles packets, checks for errors, and SMTP delivers the email to the inbox.

Mini Diagram (Simplified Flow)
[Email App] -> [TCP] -> [IP] -> [Ethernet/Wi-Fi] -> [Router] -> [Internet] -> [Friend's Server]

• Each layer handles its specific task to ensure the email arrives correctly.

When troubleshooting end-to-end communication:
	• **Application Layer:** Check if the service is running (web server, email server).
	• **Transport Layer:** Check TCP/UDP ports and firewalls.
	• **Network Layer:** Check IP addresses, routing, and connectivity (ping/traceroute).

---

# Topic 5 Local Area Networks (LANs)

A LAN is like your digital neighbourhood; it connects computers, printers, phones, and other devices within a limited area such as a home, office, school, or campus. LANs are fast, secure, and relatively inexpensive compared to larger networks like WANs.

#### LAN Technologies

There are different technologies used to implement LANs, each with its own history and strengths.

##### 1. Ethernet
• Most common LAN technology today.
• Uses cables (usually Cat5e, Cat6, or fiber optics) and switches.
• Operates at high speeds (100 Mbps, 1 Gbps, 10 Gbps, or more).
• Uses CSMA/CD (Carrier Sense Multiple Access with Collision Detection) to manage data transmission.
• Example: Your home network where a switch/router connects your PC, smart TV, and printer.

##### 2. Token Ring
• Older technology (IBM popularized it).
• Devices pass a “token” around the network; only the device with the token can transmit.
• Prevents collisions but slower and more expensive than Ethernet.
• Rarely used today.

##### 3. Fast Ethernet
• An improved version of Ethernet with speeds up to 100 Mbps.
• Commonly used before Gigabit Ethernet became standard.
• Still seen in older office networks.

#### VLANs (Virtual LANs)

A VLAN is like creating multiple small LANs within a single physical LAN.


• Imagine a school with one network but different departments (Admin, Teachers,
Students). VLANs allow separating traffic logically, even if everyone is using the
same switch.
- Benefits:
	o Improved security (students can’t access admin files).
	o Better performance (traffic is segmented).
	o Easier management.

**Example:**
• VLAN 10 → Admin Staff
• VLAN 20 → Teachers
• VLAN 30 → Students

Even though all devices are plugged into the same switch, traffic is isolated between
VLANs.

#### Configuring a Computer for the Internet

To connect a computer to the Internet through a LAN, you need to configure network settings.

**Steps (Typical Windows Example):**

1. **Connect physically or via Wi-Fi:**
	o Plug in an Ethernet cable or connect to Wi-Fi.
2. **Obtain an IP Address:**
	o Most routers use DHCP (Dynamic Host Configuration Protocol) to assign IPs automatically.
	o Example: Your computer might get 192.168.1.101 with a gateway of 192.168.1.1.
3. **Configure DNS:**
	o DNS servers resolve website names to IP addresses.
	o Can be provided automatically by the router or set manually (e.g., Google
	DNS: 8.8.8.8).
4. **Test Connectivity:**
	o Ping the gateway: ping 192.168.1.1
	o Ping an external site: ping google.com

#### Configuring the Modem

The modem connects your LAN to the ISP (Internet Service Provider).

Typical Configuration Steps:

 1. Plug the ISP line into the modem.
 2. Connect the modem to a router or directly to your computer.
 3. Enter ISP credentials (if required) in the modem/router web interface.
	o Example: PPPoE username and password.
4. Save settings → The modem authenticates with the ISP.
5. Test internet access.

#### Surfing the Internet (How It Actually Works)

When you type www.example.com into your browser:

1. Your computer checks DNS to translate the name into an IP address.
2. A TCP connection is established with the web server (usually over port 80 for HTTP or 443 for HTTPS).
3. Your request (GET request) is sent.
4. The server responds with the web page data.
5. Your browser displays the page.

#### Practical Example: Small LAN Setup

Imagine setting up a LAN in a small office with 5 computers and 1 printer.

Steps:

1. Connect all computers and the printer to a central switch using Ethernet cables
2. Connect the switch to a router (which also connects to the modem for internet)
3. Configure IP addresses:
	o Router: 192.168.1.1
	o Computer 1: 192.168.1.2
	o Computer 2: 192.168.1.3
	o … and so, on
	o Printer: 192.168.1.50
4. Enable file and printer sharing on each computer.
5. Test connectivity by pinging each device.

Result:
• Everyone can share files, access the printer, and use the Internet.

conceptual Diagram

When a device won’t connect to the Internet:
1. Check physical connections (cable, Wi-Fi signal).
2. Verify IP address (shouldn’t be 169.x.x.x → that means no DHCP).
3. Ping the gateway (192.168.1.1).
4. If that works, check DNS settings.
5. Still no Internet? Check modem/router or call your ISP.

---

# Topic 6: Internet Protocol and Applications

Now let’s focus on the Internet Protocol (IP)—the heart of all network communication.
Think of IP as the postal system of the Internet: it provides every device with a unique address (IP address) and ensures that data is delivered to the right place, even across massive global networks. Without IP, your computer wouldn’t know where to send your Google search request, or how Netflix streams should reach your TV.

##### IP Protocol Architecture
At its core, the Internet Protocol (IP) is part of the network layer (Layer 3) in the OSI
model.

What IP Does:
	**Addressing:** Every device gets a unique IP address.
	**Routing:** Decides the best path data should take through the network.
	**Encapsulation:** Wraps data in packets with source and destination IPs.
	**Fragmentation & Reassembly:** Breaks large packets into smaller ones and reassembles them at the destination.
	**Sending a package internationally:** IP is like writing the sender’s and receiver’s addresses on the parcel.
	Routers are like postal sorting offices that decide where to forward the package.


##### IP Addresses

An IP address is like a digital home address for a device.

**IPv4**
32-bit addresses (written as four numbers separated by dots).
• Example: 192.168.1.1
Supports about 4.3 billion unique addresses (but we’ve almost run out).

**IPv6**
128-bit addresses (written as eight groups of hexadecimal numbers).
• Example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
Provides virtually unlimited addresses for the future Internet of Things (IoT).

##### IP Address Classes (IPv4)

**Class A:** For very large networks (e.g., ISPs). Range: 1.0.0.0 – 126.255.255.255
**Class B:** For medium-sized networks. Range: 128.0.0.0 – 191.255.255.255
**Class C:** For small networks. Range: 192.0.0.0 – 223.255.255.255
**Class D:** For multicast groups.
**Class E:** Experimental.

##### Public vs. Private IPs

**Public IPs:** Globally unique, used on the Internet. Example: 8.8.8.8 (Google DNS).
**Private IPs:** Used within LANs, not routable on the Internet.

**Common ranges:**
10.0.0.0 – 10.255.255.255
172.16.0.0 – 172.31.255.255
192.168.0.0 – 192.168.255.255

##### Data Units in IP
When data is sent across the Internet, it is broken down into units called packets.
Each packet has two parts:
	`Header` → contains IP source and destination addresses, protocol info, etc.
	`Payload` → the actual data (e.g., part of a webpage, email, or video).
If a file is too large, it is split into multiple packets. The receiving device reassembles
them into the original file.

##### Interface Configuration

To communicate on a network, a device needs proper IP configuration.

Four Key Elements:

**IP Address:** Identifies the device.
	• Example: 192.168.1.100
**Subnet Mask:** Defines the “network portion” of the IP address.
	• Example: 255.255.255.0 means the first three numbers (192.168.1) define the network, while the last (100) identifies the device.
**Default Gateway:** The router’s IP—used to reach devices outside the local network.
	• Example: 192.168.1.1
**DNS Server:** Translates domain names to IP addresses.
	• Example: Google DNS → 8.8.8.8


**Windows Example:**
Go to Control Panel > Network and Sharing Center > Change Adapter Settings > Properties >
IPv4 Settings
Enter IP, subnet mask, gateway, and DNS manually, or choose “Obtain automatically”
to use DHCP.

**Address Resolution**
Computers don’t just need IP addresses—they also need MAC addresses (unique hardware addresses).
This is where ARP (Address Resolution Protocol) comes in.
ARP maps an IP address to its corresponding MAC address.
	• Example:
Your computer wants to send data to 192.168.1.5.
It sends an ARP request: “Who has 192.168.1.5?”
The device replies with its MAC address.
Data is then sent to the correct hardware address.
Without ARP, devices wouldn’t know how to physically reach each other on a LAN.


##### Internet Applications
**Web Browsing (HTTP/HTTPS):** You type www.example.com.
DNS resolves it to an IP.
Your browser uses TCP/IP to request and receive the webpage.

**Email (SMTP, IMAP, POP3):** Outgoing mail uses SMTP.
Incoming mail uses IMAP (modern) or POP3 (older).

**File Transfer (FTP):** Upload or download files between client and server.
Streaming (RTSP, RTP, HTTP Live Streaming):
Uses UDP for faster, real-time delivery.

**Remote Access (SSH, Telnet):** SSH secures remote login.
Telnet (older, insecure) allows command-line access.
Practical Example: Accessing a website
Here’s what happens when you open www.wikipedia.org: You type the URL.

DNS converts www.wikipedia.org to an IP (e.g., 208.80.154.224).
Your computer sends the request using **HTTP (or HTTPS)** over **TCP.**
Packets are addressed with source IP (192.168.1.101) and destination IP (208.80.154.224).
Data travels across your LAN → router → ISP → Internet backbone → Wikipedia servers.
The server responds with the webpage, broken into packets.
Your browser reassembles packets into a complete page.

When diagnosing Internet issues:
	• If you can’t reach a website by name but can by IP → DNS issue.
	• If you can’t reach anything outside your LAN → gateway issue.
	• If you can’t reach devices inside your LAN → IP configuration or ARP issue.


