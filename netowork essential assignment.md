
========================================================================
                    IP SUBNETTING ASSIGNMENT RESULTS
========================================================================

------------------------------------------------------------------------
ASSIGNMENT 1: 10.0.0.0/9
------------------------------------------------------------------------
* Default Class: Class A (Default mask /8)
* Custom Mask: 255.128.0.0
* Subnet Bits Borrowed: 1
* Host Bits Remaining: 23 (32 - 9)

1. Number of Subnets:
   Formula: 2^subnet_bits = 2^1 = 2 subnets

2. How Many Hosts Per Subnet (Valid Hosts):
   Formula: 2^host_bits - 2 = 2^23 - 2 = 8,388,608 - 2 = 8,388,606 hosts

3. Subnet Range (Block Size / Increment):
   Formula: 256 - 128 = 128 (Increment occurs in the 2nd octet)

4. Valid Host Ranges and Broadcast Addresses:

Subnet 1:
   - Network Address:    10.0.0.0
   - First Valid Host:   10.0.0.1
   - Last Valid Host:    10.127.255.254
   - Broadcast Address:  10.127.255.255

Subnet 2:
   - Network Address:    10.128.0.0
   - First Valid Host:   10.128.0.1
   - Last Valid Host:    10.255.255.254
   - Broadcast Address:  10.255.255.255


------------------------------------------------------------------------
ASSIGNMENT 2: 192.168.1.0/25
------------------------------------------------------------------------
* Default Class: Class C (Default mask /24)
* Custom Mask: 255.255.255.128
* Subnet Bits Borrowed: 1
* Host Bits Remaining: 7 (32 - 25)

1. Number of Subnets:
   Formula: 2^subnet_bits = 2^1 = 2 subnets

2. How Many Hosts Per Subnet (Valid Hosts):
   Formula: 2^host_bits - 2 = 2^7 - 2 = 128 - 2 = 126 hosts

3. Subnet Range (Block Size / Increment):
   Formula: 256 - 128 = 128 (Increment occurs in the 4th octet)

4. Valid Host Ranges and Broadcast Addresses:

Subnet 1:
   - Network Address:    192.168.1.0
   - First Valid Host:   192.168.1.1
   - Last Valid Host:    192.168.1.126
   - Broadcast Address:  192.168.1.127

Subnet 2:
   - Network Address:    192.168.1.128
   - First Valid Host:   192.168.1.129
   - Last Valid Host:    192.168.1.254
   - Broadcast Address:  192.168.1.255


------------------------------------------------------------------------
ASSIGNMENT 3: 172.16.0.0  255.255.0.0
------------------------------------------------------------------------
* Default Class: Class B (Default mask /16)
* Custom Mask: 255.255.0.0
* Subnet Bits Borrowed: 0 (Network is unsubnetted)
* Host Bits Remaining: 16 (32 - 16)

1. Number of Subnets:
   Formula: 2^0 = 1 subnet

2. How Many Hosts Per Subnet (Valid Hosts):
   Formula: 2^16 - 2 = 65,536 - 2 = 65,534 hosts

3. Subnet Range (Block Size / Increment):
   The entire default class range spans across the full octets.

4. Valid Host Ranges and Broadcast Addresses:

Subnet 1:
   - Network Address:    172.16.0.0
   - First Valid Host:   172.16.0.1
   - Last Valid Host:    172.16.255.254
   - Broadcast Address:  172.16.255.255


------------------------------------------------------------------------
ASSIGNMENT 4: 192.168.10.0  255.255.255.0
------------------------------------------------------------------------
* Default Class: Class C (Default mask /24)
* Custom Mask: 255.255.255.0
* Subnet Bits Borrowed: 0 (Network is unsubnetted)
* Host Bits Remaining: 8 (32 - 24)

1. Number of Subnets:
   Formula: 2^0 = 1 subnet

2. How Many Hosts Per Subnet (Valid Hosts):
   Formula: 2^8 - 2 = 256 - 2 = 254 hosts

3. Subnet Range (Block Size / Increment):
   The entire default class range spans across the final octet.

4. Valid Host Ranges and Broadcast Addresses:

Subnet 1:
   - Network Address:    192.168.10.0
   - First Valid Host:   192.168.10.1
   - Last Valid Host:    192.168.10.254
   - Broadcast Address:  192.168.10.255
========================================================================
