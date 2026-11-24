
# Topic 7: Wide Area Network (WANs)

A WAN is a network that spans a **large geographic area**, often connecting multiple
LANs and MANs (Metropolitan Area Networks) together.

#### Characteristics of WANs

1. **Geographical Coverage:**
	o Covers regions, countries, or even the entire world.
	o Example: An airline with offices across continents connects them via WAN.
2.  **Ownership:**
	o Unlike LANs, which are usually owned by one organization, WANs are often built on shared or leased infrastructure.
	o Telecom companies provide WAN services over phone lines, fiber optics, or satellites.
3. **Speed:**
	o Typically, slower than LANs because of the vast distances and reliance on shared resources.
	o Modern WAN technologies (like fiber-optic backbones) are improving speeds drastically.
4. **Technology Used:**
	o WANs often use technologies like leased lines, satellite links, MPLS (Multiprotocol Label Switching), VPNs, and the Internet itself.
5. **Complexity:**
	o WANs are more complex than LANs—they need advanced routing, security, and redundancy mechanisms to work reliably across long distances.

##### Differences Between WANs and LANs

| Feature         | LAN(Locla Area Network)                  | WAN(Wide Area Network)                                 |
| --------------- | ---------------------------------------- | ------------------------------------------------------ |
| Coverage        | Small (office, home, building)           | Large (cities, countries, global)                      |
| Ownsership      | Typically owned by one organization      | Shared/leased infrastructure(telecom providers)        |
| Speed           | High speed (100 Mbps - 10 Gbps & beyond) | Moderate speed (1Mps - several Gbps depending on tech) |
| Cost            | Relatively cheap to set up and maintain  | Expensive (leased lines, telecom charges)              |
| Technology      | Ethernet, Wi-Fi                          | MPLS, leased lines, satellite, VPNs                    |
| Fault Tolerance | Easier to troubleshoot (small area)      | Complex-requires redundancy and advanced monitoring    |

#### Types of WAN Connections

1. **Leased Lines:**
	o A dedicated line rented from a telecom company.
	o Provides guaranteed bandwidth and security.
	o Example: A bank connecting its headquarters in Nairobi to a branch in Mombasa via fiber-optic leased line.
2. **Circuit Switching (Traditional):**
	o The old telephone system method.
	o Establishes a dedicated circuit for the duration of communication (like a phone call).
	o Example: Dial-up Internet in the 1990s.
3. **Packet Switching (Modern):**
	o Data is broken into packets and sent across shared networks.
	o More efficient and widely used in modern WANs.
	o Example: The Internet uses packet switching.
4. **VPN (Virtual Private Network):**
	o Uses the public Internet to create a secure, encrypted “tunnel” between two networks.
	o Example: A company with remote workers uses VPNs to connect them securely to the office network.
5. **MPLS (Multiprotocol Label Switching):**
	o A modern WAN technology that routes data based on short path labels instead of
	long IP addresses.
	o Provides efficiency and quality of service (QoS) for video, voice, and data.
6. **Satellite Links:**
	o Used in remote areas where fiber or cables can’t reach.
	o Example: Military outposts or ships at sea using satellite WANs for communication.

#### Real-World Applications of WANs

1. **The Internet:**
	o The biggest WAN in existence.
	o Connects billions of devices across the globe.
2. **Corporate WANs:**
	o Multinational companies use WANs to connect headquarters and regional offices.
	o Example: Google’s global WAN connecting its data centers worldwide.
3. **Banking Networks:**
	o ATMs connected to central banking systems use WANs.
	o Ensures you can withdraw cash from anywhere and still update your bank balance instantly.
4. **Government and Defense:**
	o Governments set up secure WANs for communication across agencies and
	regions.
5. **Education:**
	o Universities connect multiple campuses with WANs for resource sharing and
	collaboration.

#### WAN Devices

Several networking devices support WAN connectivity:

- **Routers:** Direct data between LANs and WANs.
- **Switches:** Manage packet forwarding within a network, sometimes used in WAN backbones.
- **Modems:** Convert digital signals to analog for transmission over phone lines or DSL.
- **CSU/DSU (Channel Service Unit/Data Service Unit):** Interfaces between a router and a digital circuit like a leased line.
- **Firewalls:** Secure WAN connections by filtering traffic.

**Advantages of WANs**
• Global Connectivity: Connects organizations across countries.
• Resource Sharing: Allows remote offices to share files, applications, and systems.
• Scalability: Can expand as an organization grows.
• Centralized Data: Companies can keep data in central servers while making it accessible globally.

**Challenges of WANs**
- High Cost: Leased lines and MPLS networks are expensive.
- Slower Speeds: Compared to LANs, WANs can experience latency.
- Complex Management: Requires skilled network administrators.
- Security Risks: Data traveling across public or shared networks is vulnerable without proper encryption.

---

# Topic 8: Network Security

Network Security is all about protecting the integrity, confidentiality, and availability of data as it travels across networks.

At its core, network security answers three big questions:

1. Who is allowed into the network? (Authentication & Access Control)
2. What are they allowed to do once inside? (Authorization & Monitoring)
3. How do we keep the bad guys out? (Defense tools like firewalls, encryption, and intrusion detection)


##### Why Network Security Matters
• **Data Protection:** Prevents unauthorized access to sensitive data (like passwords,
medical records, or financial info).
• **System Reliability:** Ensures systems stay available and resistant to downtime or
attacks.
• **Compliance:** Many industries (healthcare, banking, government) require strict
network security policies.
• **User Trust:** Users need confidence that their communication is safe and private.
• **Example:** When you log into your bank app, encryption makes sure that no one
on the network can “listen in” and steal your password or account balance.

##### Threats to Networks

1. Unauthorized Access: Hackers breaking into systems.
2. Data Interception: Attackers “sniffing” unencrypted traffic to steal passwords or credit card numbers.
3. Denial of Service (DoS/DDoS): Overloading a server or network with traffic so it can’t serve real users.
4. Malware & Viruses: Harmful programs that spread across networks.
5. Man-in-the-Middle (MITM): Attackers secretly intercept and alter communication between two parties.
6. Insider Threats: Employees misusing their access privileges.

##### Firewalls

A firewall is like the security guard of your network. It sits between your private network and the outside world (e.g., the Internet), filtering traffic based on rules.
If your LAN is a private party, the firewall is the bouncer at the door—checking ID and deciding who can enter, who gets thrown out, and what they can bring in.

##### Types of Firewalls

1. **Packet-Filtering Firewalls:**
	o The simplest type.
	o Examines the header of each packet (IP, port, protocol) and decides whether to allow or block it.
	o Fast but not very “smart”—it doesn’t look inside the packet’s data.
2. **Stateful Firewalls:**
	o Smarter than packet filters.
	o Tracks the “state” of active connections (e.g., ongoing web sessions).
	o Allows only traffic that is part of a legitimate, established connection.
3. **Application-Level (Proxy) Firewalls:**
	o Operate at the application layer.
	o Can examine actual content (like HTTP requests or emails) to block malicious data.
	o Example: Filtering out spam emails or blocking harmful website requests.
4. **Next-Generation Firewalls (NGFW):**
	o Combine packet filtering, stateful inspection, intrusion detection, and deep packet inspection.
	o Can even use AI to spot suspicious traffic.

**Firewall Rules**
Firewalls operate based on rules that administrators define:
•
 Example rule:
	o Block all traffic from IP address 203.0.113.45.
	o Allow HTTP/HTTPS traffic (ports 80 and 443).
	o Deny Telnet traffic (port 23) but allow SSH (port 22).

#### Simple Network Management Protocol (SNMP)

Now let’s talk about another important aspect: monitoring networks.

**What is SNMP?**
The `Simple Network Management Protocol (SNMP)` is a standard used to manage and monitor devices on a network.
Think of SNMP as a doctor for your network—it constantly checks the health of
routers, switches, printers, and servers.

**How It Works**
• Devices like routers and switches have SNMP agents installed.
• A central computer (the SNMP Manager) queries these devices.
• Devices respond with data like CPU usage, memory usage, packet loss, or interface errors.

##### SNMP Components

1. Managed Devices: Devices you want to monitor (e.g., routers, switches).
2. SNMP Agent: Software running on the managed device that gathers information.
3. SNMP Manager: The central system that communicates with agents and collects data.

Example Use Case
• An SNMP system can alert administrators if a router’s CPU usage is too high or if a link goes down.
• Example: “Switch 2 in the Nairobi branch office is reporting 40% packet loss on port 3.”


##### Combining Firewalls and SNMP

While firewalls keep the “bad guys” out, SNMP helps ensure everything is running
smoothly inside the network.
For example:
• A firewall may block suspicious traffic from an unknown IP.
• SNMP may simultaneously alert admins that bandwidth on the WAN link has spiked, possibly due to an attempted attack.

Together, they provide protection (firewalls) and visibility (SNMP).

##### Real-World Examples of Network Security

1. **Banking Systems:**
	o Firewalls block unauthorized access.
	o SNMP monitors ATM network health.
2. **Corporate Offices:**
	o Firewalls restrict access to only necessary services.
	o SNMP tracks bandwidth to detect bottlenecks.
3. **Home Networks:**
	o Most home routers include a built-in firewall.
	o Power users sometimes use SNMP to monitor their home internet usage.

#### Challenges in Network Security
- Keeping up with evolving threats: Hackers constantly invent new attack methods.
- Balancing usability and security: Too many restrictions can frustrate users.
- Misconfigurations: Poorly set firewall rules can either leave holes open or block legitimate traffic.
- SNMP Vulnerabilities: If not properly secured, SNMP itself can be exploited (e.g., default community strings like “public” are a common weakness).

#### Best Practices in Network Security

1. Regular Updates: Keep firewalls and devices patched.
2. Least Privilege Principle: Only give users and apps the access they truly need.
3. Encryption: Use SSL/TLS, VPNs, and WPA3 for Wi-Fi.
4. Strong Authentication: Use multi-factor authentication for logins
5. SNMP Security: Change default community strings, and use SNMPv3 for encrypted communication.
6. Monitoring & Alerts: Always monitor logs and set up alerts for unusual traffic.

---

# Topic 9: Wireless Networking

In networking terms, `wireless networking` refers to communication between devices without physical cables, typically using radio waves or infrared signals. It’s flexible, convenient, and often cost-effective; but it also comes with challenges like interference, security risks, and bandwidth issues.

#### Wireless Networking Concepts

##### 1. Wireless Standards (Wi-Fi Generations)

Wireless networking is standardized by IEEE 802.11. Over time, new versions have improved speed, range, and reliability.

- **802.11b (1999):** Up to 11 Mbps, 2.4 GHz band
- **802.11g (2003):** Up to 54 Mbps, backward compatible with b.
- **802.11n (Wi-Fi 4) (2009):** Up to 600 Mbps, uses 2.4 and 5 GHz bands, supports MIMO (multiple antennas).
- **802.11ac (Wi-Fi 5) (2013):** Up to 3.5 Gbps, 5 GHz band, improved MIMO.
- **802.11ax (Wi-Fi 6/6E) (2019):** Up to 9.6 Gbps, works on 2.4, 5, and new 6 GHz bands, supports more devices at once.

Example:
- Wi-Fi 4 was fine for browsing on a few laptops.
- Wi-Fi 6 can handle dozens of devices streaming Netflix, playing games, and video calling—all at the same time.

##### 2. Wireless Network Modes

- **Infrastructure Mode:** Devices connect through a central access point (e.g., Wi-Fi router). Most home and office setups use this.
- **Ad-Hoc Mode:** Devices connect directly to each other without an access point. Useful for quick file sharing or temporary setups.
- **Mesh Networking:** Multiple access points work together to cover a large area (like campus Wi-Fi or smart home systems).

##### 3. Wireless Connectivity Devices

- **Access Points (APs):** Provide wireless coverage within a LAN.
- **Wireless Routers:** Combine a router, switch, and access point in one (common at home).
- **Wireless Network Interface Cards (NICs):** Built into laptops, phones, or USB adapters to enable Wi-Fi connectivity.
- **Repeaters/Extenders:** Boost signals to cover “dead zones.”
- **Antennas:** Used in APs/routers to direct and strengthen signals.

Example:
In a university campus, multiple APs connect students’ laptops and phones to the Internet seamlessly while roaming from building to building.

#### Common Wireless Problems

##### 1. Connectivity Loss

- **Cause:** Weak signal, interference, or wrong configuration.
- **Fix:**
	o Move closer to the router.
	o Restart router or device.
	o Check Wi-Fi settings (SSID, password).
	o Ensure DHCP is assigning IPs correctly.

##### 2. Slow Speeds

- **Cause:** Too many devices, interference (microwaves, cordless phones), or outdated equipment.
- **Fix:**
	o Switch from 2.4 GHz to 5 GHz.
	o Upgrade router to Wi-Fi 6.
	o Limit bandwidth-hogging apps (e.g., torrents).
	o Place the router in a central, elevated position.

##### 3. Data Loss (Packet Drops)

- **Cause:** Interference, congestion, faulty drivers.
- **Fix:**
	o Update wireless adapter drivers.
	o Reduce interference by changing channels (1, 6, or 11 on 2.4 GHz).
	o Use wired connections for critical devices.

##### 4. Dead Zones

- **Cause:** Walls, distance, or poor router placement.
- **Fix:**
	o Use Wi-Fi extenders or mesh networks.
	o Relocate the router for better coverage.

#### Increasing Network Bandwidth

Wireless performance can always be improved with smart choices:

1. Use Latest Standards: Upgrade to Wi-Fi 6 routers and devices.
2. Dual-Band/Triple-Band Routers: Use both 2.4 GHz (longer range) and 5/6 GHz (higher speed, less interference).
3. QoS (Quality of Service): Prioritize important traffic like video calls or gaming over downloads.
4. Channel Management: Manually select less crowded channels (use Wi-Fi analyzer apps).
5. Ethernet Offload: Connect stationary devices (e.g., desktop PCs or smart TVs) with cables to free Wi-Fi bandwidth for mobile devices.

Example:
In a smart home with 20+ devices (TV, cameras, phones, laptops, Alexa, etc.), upgrading to Wi-Fi 6E with mesh routers ensures stable, high-speed connectivity everywhere

#### Wireless Security

Wireless networks, unlike wired ones, are inherently more vulnerable because anyone nearby can attempt to connect or eavesdrop.

##### Security Protocols

- **WEP (Wired Equivalent Privacy):** Outdated, easily hacked. Don’t use.
- **WPA (Wi-Fi Protected Access):** Better but also obsolete.
- **WPA2:** Industry standard for many years, strong AES encryption.
- **WPA3:** Latest, stronger encryption, protection against brute-force attacks.

###### Best Practices

1. Always use WPA2 or WPA3 security on Wi-Fi.
2. Change default SSIDs and router passwords.
3. Use strong, complex Wi-Fi passwords.
4. Disable WPS (Wi-Fi Protected Setup), as it can be exploited.
5. Keep router firmware updated.
6. Consider guest networks to separate visitor devices from your main network.

#### Real-World Applications of Wireless Networking

1. **Home Networks:** Wi-Fi routers powering laptops, smart TVs, and IoT devices.
2. **Business & Enterprise:** Offices using multiple APs and mesh systems for seamless roaming.
3. **Education:** Campus Wi-Fi connecting thousands of students.
4. **Healthcare:** Wireless medical equipment and patient monitoring systems.
5. **Public Hotspots:** Airports, cafes, and malls offering free Wi-Fi.

**Mini Conceptual Diagram**
[Internet] → [Router/Access Point] ))))) [Laptop]
							))))) [Smartphone]
							))))) [IoT Device]

##### Advantages of Wireless Networking

- Convenience and mobility.
- Easier and cheaper setup (no cabling).
- Scales easily—just add more APs.
- Supports a wide range of devices (phones, IoT, laptops).

##### Disadvantages

- Security risks (eavesdropping, unauthorized access).
- Performance issues (interference, lower speeds than wired).
- Reliability can drop in crowded or large environments.
