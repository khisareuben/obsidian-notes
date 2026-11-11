# IT Career Path: Start Here → Go Here → End Here
## From Zero to Network Security Engineer (A+ → Network+ → Security+ → CCNA → Beyond)

> **The Golden Rule:** Don't skip steps to save time. You will pay for it later in failed exams.
> This path is built like a building. Each cert is the floor for the next one.

---

## Overview: The Full Road At A Glance

| Time | Cert | Job Title | Approx Pay (Kenya) |
| :--- | :--- | :--- | :--- |
| Month 0-1 | Foundation (No Cert) | Student / Self-Learner | 0 |
| Month 1-4 | **CompTIA A+** | IT Support / Help Desk | 30k - 60k KES |
| Month 4-7 | **CompTIA Network+** | NOC Analyst / Network Support | 50k - 90k KES |
| Month 7-10 | **CompTIA Security+** | SOC Analyst / Security Analyst | 80k - 150k KES |
| Month 10-16 | **Cisco CCNA** | Network Security Engineer | 120k - 220k KES |
| Year 3+ | **CCNP / CySA+ / PenTest+** | Senior Engineer / Architect | 200k - 400k+ KES |

**Total exam cost for the core 4 certs:** ~$1,686
- A+ $548 (2 exams) + Network+ $399 + Security+ $439 + CCNA $300
- Spread over 16 months = about 17k KES per month if you save.

**Your Destination Is NOT Just Sec+ OR Just CCNA.**
Your destination is: **Network Security Engineer with A+ + Network+ + Security+ + CCNA.**
That person can build the network AND secure it. That is the highest-paid mid-level job in IT in Kenya.

---

## STAGE 0: FOUNDATION (Month 0 - 1)
### Before You Pay For Any Exam

**Goal:** Be able to do this, or A+ will crush you.

### Learn:
- How to use Windows properly - install, update, users, control panel
- Basic computer parts - CPU, RAM, Hard Drive, Motherboard
- What is Internet, IP Address, Wi-Fi, Router
- Basic command line: `ping`, `ipconfig`

### Do:
- Get a laptop, install Windows fresh from USB
- Open it, identify RAM and Hard Drive
- Set up your home Wi-Fi, change password, connect 2 devices

**Job:** None yet. You're a student.
**Cost:** $0 - YouTube only

> If you can't do Stage 0, don't start A+. You'll waste money.

---

## STAGE 1: GET EMPLOYED - CompTIA A+ (Month 1 - 4)
### Your First Cert. Your First Job.

**Cert:** CompTIA A+ (220-1201 + 220-1202)
**Exams:** 2 exams, must pass both, in any order
**Cost:** ~$548 total ($274 per exam, US list price)
**Study Time:** 3-4 months
**Recommended Experience:** 12 months as IT support specialist (recommendation, NOT a requirement)
**Passing Score:** 675 (Core 1) and 700 (Core 2) on 100-900 scale
**Valid For:** 3 years
**Renewal:** 20 CEUs + $75 fee, OR get a higher cert

### What You Learn:
- Hardware, motherboards, RAM, storage, laptops, mobile devices, printers
- Windows, macOS, Linux, ChromeOS basics
- Networking basics - just enough to troubleshoot Wi-Fi, IP, DNS, DHCP
- Security basics, operational procedures, customer service / ticketing

### How A+ Tests You (Not Just Theory):
A+ is NOT just multiple choice. It has Performance-Based Questions (PBQs):
- Drag-and-drop the right cable/port to the right device
- Configure a small network: set IP, subnet, gateway, DNS
- Partition a disk, set up RAID
- Fix boot order in BIOS
- Match a troubleshooting ticket to the right tool

You cannot memorize PBQs. You have to have clicked through it before.

**Example of a real A+ question style:**
> Not: "What is DHCP?"
> But: "A user can't connect to the internet. Their IP is 169.254.x.x. Other users are fine. What is the MOST likely cause and what do you do first?"
> Answer: DHCP failed.

### How To Pass Without A Job (The Break-It Lab):
You don't need a job. You need a laptop and willingness to break things.

**1. The Break-It Lab (Core 1 - Hardware)**
- Open your laptop (YouTube your model + "disassembly"). Identify RAM, hard drive, CMOS battery, Wi-Fi card. Put it back.
- Go into BIOS/UEFI. Change boot order. Turn Secure Boot on/off. See what happens.
- Install Windows from USB. Then install Ubuntu alongside it (dual boot). Then wipe it and do it again.

**2. The Network Lab (Core 1 + Core 2)**
- Run these until you understand them, not just memorize:
  `ipconfig`, `ping 8.8.8.8`, `ping google.com`, `tracert google.com`, `nslookup google.com`, `netstat`, `arp -a`
- Set a static IP manually, break your internet on purpose, then fix it back to DHCP.
- Use phone hotspot + laptop + router at home. That's a 3-device network.

**3. The Virtual Lab (Free)**
- **VirtualBox (free)** - Install Windows and Linux as virtual machines. Practice installing OS, partitioning disks, snapshots, networking between VMs.
- **Professor Messer / Jason Dion labs on YouTube** - Watch, pause, DO it at the same time. Don't just watch.

**4. The "Fix It For Real" Lab**
- Offer to fix 1 family member's slow laptop. Document it like a ticket: Problem -> What you checked -> What you fixed -> Result.
- Do 5 of those and you have more real troubleshooting experience than someone who watched 100 hours of theory.

### How To Break The Experience Catch-22:
**The Problem:** A+ recommends 12 months experience, but jobs require A+.
**The Truth:** That 12 months is a recommendation, not a rule. Employers know it. Most people get A+ BEFORE their first IT job.

**Manufacture Experience Without A Job Title:**
- **Home lab / family & friends IT guy:** "Provided IT support for 15+ households / small businesses"
- **Volunteer / church / mosque / school / cyber cafe:** Offer to fix computers, set up Wi-Fi, manage printer/network for free for 2-3 months. Get a reference letter.
- **Internship / attachment:** Even unpaid 1-3 months at ISP, cyber, repair shop, school, NGO, county office counts. Walk in with CV.
- **Freelance repair:** Advertise on WhatsApp status / Facebook: "Laptop repair, Windows install, Wi-Fi setup in Mombasa."
- **Help desk simulation:** Use free tools like Spiceworks, Freshdesk free tier. Practice documenting tickets.

**What To Say In Interview:**
> "I don't have a formal IT title yet, but for the last 6 months I've been doing support for [church/school/family businesses] — Windows installs, Wi-Fi and printer setup, virus removal, and user support. I also run a home lab where I practice troubleshooting network and OS issues. That's why I did A+ — to formalize what I've been doing."

### Study Method That Works:
Don't do: Watch all videos -> Read book -> Take exam
Do this loop for each topic:
1. **Watch** 20-30 mins (Professor Messer is free and best for A+)
2. **DO** it in your lab immediately (15 mins)
3. **Teach it** out loud: "If a user says X, I would check Y, then Z"
4. **Test** yourself with 10 practice questions on just that topic

If you can't do step 2 and 3, you don't know it yet — you just recognize it.

### Self-Test: Are You Ready?
Can you answer WITHOUT Googling, and explain WHY?
1. A PC won't boot, it beeps 3 times. What do you check first?
2. A user gets 169.254.x.x. What does that mean and what's your first 2 steps?
3. You need to install Windows, but BIOS boots to hard drive first. What do you change?
4. A printer prints blank pages. Is it hardware, driver, or toner? How do you prove it?

### Job You Get After This:
**Help Desk Technician / IT Support Specialist / Desktop Support / Field Service Technician / ISP Customer Support**
**Pay in Kenya:** 30k - 60k KES

**THIS IS YOUR BASE.** You are now IN IT. You are earning while you learn the next steps. Don't quit your job to study full-time after this.

---

## STAGE 2: LEARN NETWORKS - CompTIA Network+ (Month 4 - 7)
### Do This WHILE Working In Your Stage 1 Job

**Cert:** CompTIA Network+ (N10-009)
**Exams:** 1 exam
**Cost:** ~$399 (US list price)
**Study Time:** 2-3 months (6-10 weeks full-time)
**Recommended Experience:** A+ plus 9 to 12 months as junior network admin / network support
**Prerequisite:** NONE official - A+ is recommended, not required. Anyone can register.
**Passing Score:** 720 on 100-900 scale
**Valid For:** 3 years
**Renewal:** 30 CEUs + $150 fee, OR get a higher cert

### What You Learn:
- TCP/IP, subnetting, routing, switching, VLANs, wireless
- Network infrastructure, cabling, cloud and virtualization networking
- Network operations, monitoring, troubleshooting methodology
- Network security concepts (but not as deep as Security+)

### Network+ vs A+:
- **A+ = Breadth:** You can support users, PCs, OS, basic network issues.
- **Network+ = Depth in one area:** You understand how networks actually work, and can design, manage, troubleshoot them.

A+ covers the whole support desk. Network+ goes deeper on networking alone.

### Do You Have To Do A+ First?
**No.** There is no official prerequisite.

**But you can't be a network specialist without knowing SOME A+ stuff:**

**You NEED this A+ stuff for networking:**
- OS basics: `ipconfig / ifconfig`, `ping`, `tracert`, `nslookup`, `netstat`, `arp`
- Hardware basics: What a NIC is, RAM/CPU/storage bottlenecks
- Networking basics: IP, subnet mask, gateway, DNS, DHCP
- Troubleshooting mindset: Is it cable, PC, switch, or ISP?

**You can SKIP this A+ stuff for pure networking:**
- Printer troubleshooting, printer types
- Motherboard form factors, RAM types in detail, CPU sockets
- Mobile device repair
- Detailed Windows imaging / customer service ticketing

**The Shortcut:** Don't get the A+ certificate, but steal the A+ knowledge. Do a crash course on just networking + hardware + OS sections. If you can set a static IP, ping a gateway, check DNS, and tell if a problem is PC vs network, you can go straight to Network+.

### Lab You Must Do:
- **Packet Tracer (free from Cisco)** - Build a 3-router network, configure DHCP, break it, fix it.
- Practice subnetting daily until it's automatic.

### Job You Get After This:
**Network Support Technician / NOC Analyst / Junior Network Administrator / IT Infrastructure Support**
**Pay in Kenya:** 50k - 90k KES

**IMPORTANT:** When you pass Network+, your A+ is automatically renewed for 3 more years. You don't pay for A+ again.

---

## THE FORK IN THE ROAD
### You Are Now At The Fork. Choose ONE Destination To Focus On First.

You can get the other later, but you can't chase both at the same time or you'll fail both.

---

## DESTINATION A: THE NETWORK ENGINEER (The CCNA Road)
### Pick This If You Love Building Networks

### STAGE 3A: Cisco CCNA (Month 7 - 13)

**Cert:** Cisco Certified Network Associate (CCNA)
**Exam:** 1 exam: 200-301 - Implementing and Administering Cisco Solutions
**Cost:** ~$300 (US list price)
**Study Time:** 3-6 months (because of labs)
**Valid For:** 3 years
**Renewal:** 30 CE credits

### Network+ vs CCNA - The Real Difference:

|  | Network+ | CCNA |
| :--- | :--- | :--- |
| Vendor | Vendor-neutral (Cisco, Huawei, Mikrotik, Ubiquiti, TP-Link) | Cisco-specific (Cisco commands, Cisco equipment) |
| What It Proves | You UNDERSTAND networking concepts | You can CONFIGURE a real network |
| Difficulty | Moderate | Moderate-Hard |
| Test Style | "Explain it" - What is a VLAN? What is OSPF? | "Do it" - Log in, configure OSPF, set up VLANs, fix ACL |
| Study Time | 6-10 weeks | 3-6 months |

**Network+ asks:** "What is a VLAN?"
**CCNA asks:** "Here's 3 routers not talking. Log in, configure OSPF, set up VLANs, fix the ACL. You have 120 minutes."

CCNA has live simulation questions where you type Cisco IOS commands like:
```
enable
configure terminal
interface gigabitEthernet0/0
ip address 192.168.1.1 255.255.255.0
no shutdown
router ospf 1
network 192.168.1.0 0.0.0.255 area 0
```

If you've never labbed, you will fail CCNA even if you memorized the book.

### What You Learn:
- Routing: OSPF, EIGRP, static routing
- Switching: VLANs, STP, EtherChannel
- Security: ACLs, NAT, port security
- Wireless, automation, programmability basics

### Jobs:
**Network Engineer / Network Administrator / NOC Engineer / Infrastructure Engineer**
**Pay in Kenya:** 100k - 200k KES (ISP, Safaricom, bank, telco)

CCNA carries more weight for Network Engineer jobs. If job ad says "CCNA required", Network+ won't get you past HR. Most big ISPs, banks, telcos run Cisco.

### STAGE 4A: BECOME SENIOR (Year 2 - 4)
**Cert:** Cisco CCNP Enterprise
**Cost:** ~$700+ (2 exams)
**What It Is:** CCNA on steroids. You design large enterprise networks.
**Job:** Senior Network Engineer / Network Architect
**Pay in Kenya:** 180k - 350k+ KES

### STAGE 5A: THE TOP (Year 4+)
Pick ONE specialty:
- **CCNP Security** - Network Security Engineer (Firewalls, VPNs)
- **Cloud Networking** - AWS / Azure Network Engineer
- **Automation** - Python + Ansible for networks

**Final Destination A:** Network Architect. You design networks for entire companies.

---

## DESTINATION B: THE CYBERSECURITY ENGINEER (The Security+ Road)
### Pick This If You Love Catching Hackers And Protecting Systems

### STAGE 3B: CompTIA Security+ (Month 7 - 10)

**Cert:** CompTIA Security+ (SY0-701)
**Exam:** 1 exam
**Cost:** ~$439 (US list price)
**Study Time:** 2-3 months
**Valid For:** 3 years
**Renewal:** 50 CEUs + $150 fee

### What You Learn:
- Threats, attacks, malware, social engineering
- Cryptography, access control, identity management
- Firewalls, IDS/IPS, VPNs
- Incident response, risk management, compliance, governance

### CCNA vs Security+ - Which Carries More Weight?

Neither is universally "higher". They are for two different careers.

**CCNA carries more weight if:**
- Job is Network Engineer / Network Admin / ISP / Bank infrastructure
- Company runs Cisco equipment
- You want deep technical, hands-on job

**Security+ carries more weight if:**
- Job is SOC Analyst / Security Analyst / Cybersecurity
- Job is government, NGO, defense, bank security/compliance
- You want to get into cybersecurity

Security+ is often a MANDATORY requirement for government / DoD jobs. CCNA is not.
Cybersecurity is growing faster - Information security analysts projected at 21% growth, US median pay ~$129,180.

**Difficulty:**
- CCNA = Harder, hands-on labs, must configure routers/switches
- Security+ = Medium, more theory, concepts, best practices, no live device config

**Salary Ceiling:**
- CCNA path: Network Engineer → Senior → Architect = $80k-$130k+ US
- Security+ path: SOC Analyst → Security Analyst → Security Engineer / Pentester / Cloud Security = $90k-$150k+ US

Security roles tend to have higher compensation even at early career stage and offer rapid advancement because of shortage - 3.5 million unfilled cybersecurity positions globally.

### Job You Get After Security+:
**SOC Analyst / Security Analyst / IT Security Admin / Cybersecurity Analyst**
**Pay in Kenya:** 80k - 150k KES (Bank, cybersecurity firm, SOC)

**IMPORTANT:** When you pass Security+, your A+ AND Network+ are automatically renewed for 3 more years. You now only renew Security+.

### STAGE 4B: BECOME A REAL SECURITY PRO (Year 2 - 3)
Pick ONE specialty. Don't do both at once.

**Option 1 - The Defender (Blue Team):**
**Cert:** CompTIA CySA+ → Then Splunk / SIEM
**Job:** SOC Analyst L2 / Threat Hunter / Incident Responder
**Pay:** 150k - 300k KES

**Option 2 - The Attacker (Red Team):**
**Cert:** CompTIA PenTest+ → Then OSCP (The hardest, most respected hacking cert)
**Job:** Penetration Tester / Ethical Hacker
**Pay:** 150k - 350k+ KES

### STAGE 5B: THE TOP (Year 4 - 6)
**Cert:** CISSP (The king of security certs)
**Requirement:** 5 years experience to get full CISSP. You can pass exam earlier and become "Associate of ISC2".
**Job:** Security Manager / CISO / Security Architect
**Pay:** 300k - 600k+ KES / International remote jobs $100k+

**Final Destination B:** CISO / Security Architect. You protect entire companies.

---

## THE "BOTH WINS" PATH - THE ULTIMATE PATH
### The Person Who Has BOTH Wins

**A person with A+ + Network+ + Security+ + CCNA can walk into any ISP, bank, or cybersecurity firm in Kenya and say: "I can build the network, and I can secure it."**

### The Full Road In Order:

**Year 0-1:** A+ → Network+ → Get a job
**Year 1-2:** Security+ → Get a SOC / NOC job
**Year 2-3:** CCNA → Now you have BOTH
**Year 3+:** Pick your final boss: CCNP Security OR CySA+ / PenTest+

**Why This Order?**
1. A+ gets you a job
2. Network+ teaches you networking theory
3. Security+ teaches you security theory + renews the first two
4. CCNA teaches you how to ACTUALLY BUILD what Security+ told you to protect

**Final Job Title:** Network Security Engineer
**Pay:** 120k - 220k KES to start, 200k - 400k+ KES senior

---

## CERT RENEWAL - HOW IT WORKS (You Do NOT Retake Exams Every 3 Years)

### The Rule:
All CompTIA certs are valid for **3 years** from the date you pass.

You have 3 ways to renew:
1. **Earn CEUs (Most Common)**
2. **Get a Higher Cert (The Smart Hack)**
3. **Do CertMaster CE (The Lazy Option)**
4. **Retake Exam (Last Resort - Most Expensive)**

### Option 1: Earn CEUs
Prove you're still learning, no exam.

- **A+:** 20 CEUs + $75 fee for 3-year cycle
- **Network+:** 30 CEUs + $150 fee
- **Security+:** 50 CEUs + $150 fee

What counts: Training courses, webinars, conferences, other certs, work experience, teaching, mentoring. Upload proof to CompTIA account.

### Option 2: Get A Higher Cert - Automatic Renewal
**A higher CompTIA cert automatically renews the lower ones.**

- Get Network+ while A+ is still valid = A+ renewed for 3 more years. No extra fee for A+.
- Get Security+ while Network+ is still valid = BOTH A+ and Network+ renewed for 3 more years.

Example Timeline:
- Year 0: Pass A+
- Year 1: Pass Network+ → A+ now expires Year 4 (not Year 3)
- Year 2: Pass Security+ → A+ AND Network+ now expire Year 5
- All three now expire on same day - Security+ expiry date.

### Option 3: CertMaster CE
Short online course from CompTIA.
- A+ version: ~$129, 8-10 hours
- Network+ version: ~$189, 8-10 hours
Do course, pass quiz, renewed. No exam centre.

### Option 4: Retake Exam (Don't Plan For This)
- A+ = Retake BOTH Core 1 + Core 2 again at full price ($548)
- Network+ = Retake 1 exam ($399)
Nobody chooses this unless they let it expire completely.

### If You Get Higher Certs, Do You Renew All Or Just Highest?
**JUST THE HIGHEST ONE.**

You NEVER have to renew all three separately. You only renew the highest cert you hold, and it automatically renews everything below it.

- **CySA+** renews Security+, Network+, A+
- **PenTest+** renews Security+, Network+, A+
- **SecurityX (old CASP+)** renews all of them

**2 Rules You Must Not Break:**
1. **Lower cert must still be valid when you earn higher one.** If A+ already expired, Network+ will NOT bring dead A+ back. You'd have to retake A+.
2. **Renewal only goes DOWN, not UP.** Getting A+ does NOT renew Network+. Getting Network+ does NOT renew Security+. It only works upward.

Think of it like a ladder:
Security+ renews everything below it.
Network+ renews only A+.
A+ renews nothing else.

**Your Only Renewal Worry:** "When does my highest cert expire?" Renew that one, everything else follows.

---

## WHICH PATH SHOULD YOU PICK FIRST?

Ask yourself one question:
**Do you enjoy breaking/fixing networks, or catching hackers?**

- If you love routers, switches, VLANs, subnetting, making internet work → **CCNA first (after Network+)**
- If you love threats, hacking, firewalls, incident response, protecting systems → **Security+ first**
- If you love both → **Do Security+ first (faster, easier), then CCNA after.** Security+ will get you into SOC job faster, CCNA will make you a better security engineer later.

Don't pick based on "weight." Pick based on the job title you want to see on your LinkedIn in 2 years:
**Network Engineer** OR **Security Analyst / SOC Analyst**?

### Recommended Order For Most People In Kenya:
**1. A+ (Now)**
**2. Network+ (Next)**
**3. Security+ (Next)**
**4. CCNA (Last of the four)**

Don't do CCNA before Security+. Security+ is faster, renews everything, and gets you a better job faster. CCNA is harder and takes longer — do it when you already have a job and income.

---

## QUICK COMPARISON TABLES

### A+ vs Network+
|  | A+ | Network+ |
| :--- | :--- | :--- |
| Exams | 2: Core 1 (220-1201) + Core 2 (220-1202) | 1: N10-009 |
| Focus | Help desk, IT support, hardware, OS | Networks in depth |
| Cost | $548 total | $399 |
| Jobs | Help Desk, Desktop Support | Network Support, NOC Analyst |

### Network+ vs CCNA
|  | Network+ | CCNA |
| :--- | :--- | :--- |
| Vendor | Vendor-neutral | Cisco-specific |
| Proves | You understand networking | You can configure a network |
| Difficulty | Moderate | Moderate-Hard |
| Cost | ~$399 | ~$300 |
| Jobs | Network Support, NOC | Network Engineer, Network Admin |

### CCNA vs Security+
|  | CCNA | Security+ |
| :--- | :--- | :--- |
| Track | Networking / Infrastructure | Cybersecurity |
| Vendor | Cisco-specific | Vendor-neutral |
| Difficulty | Harder - hands-on labs | Medium - theory, concepts |
| Cost | ~$300 | ~$439 |
| Jobs | Network Engineer | SOC Analyst, Security Analyst |

---

## FINAL CHECKLIST - START TODAY

- [ ] Stage 0: Can you install Windows, set up Wi-Fi, use `ping` and `ipconfig`?
- [ ] Stage 1: Start A+ study - Professor Messer (free) + Lab + Fix 5 real laptops
- [ ] Get volunteer / attachment / internship - Church, school, cyber, repair shop
- [ ] Pass A+ Core 1, then Core 2 - Get first IT job
- [ ] Stage 2: Study Network+ while working - Packet Tracer labs daily
- [ ] Pass Network+ - Apply for NOC / Network Support
- [ ] Stage 3: Study Security+ - Get SOC job
- [ ] Stage 4: Study CCNA - Lab every day - Become Network Security Engineer
- [ ] Stage 5: Specialize - CCNP Security OR CySA+ / PenTest+ → CISSP

**Remember:** You don't need 12 months experience to START. You need to START to get 12 months experience.

---

*Created: November 10, 2026 - Mombasa, Kenya*
*Path: Foundation → A+ → Network+ → Security+ → CCNA → Specialize*
*Destination: Network Security Engineer*
