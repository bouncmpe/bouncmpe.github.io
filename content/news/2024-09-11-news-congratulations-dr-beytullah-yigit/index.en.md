---
type: news
title: Congratulations Dr. Beytullah Yiğit!
description: Beytullah Yiğit has successfully defended her PhD thesis
featured: true
date: 2024-06-03
thumbnail: uploads/beytullah-yigit-doktora.png
---
## A Security Framework for Software-Defined Networks

## Abstract

Software-Defined Networking (SDN) emerges as a transformative technology,
offering the flexibility and scalability crucial for modern digital services.
While SDN presents opportunities to address security shortcomings in
traditional networks, it also introduces new vulnerabilities, particularly
in data and control plane communications.

This thesis proposes a security framework to mitigate these risks, focusing on securing data exchange among SDN entities (controllers, switches, and applications). In our model, Transport Layer Security (TLS) can be activated between SDN nodes to ensure confidentiality, integrity, authentication, and authorization, leveraging specialized certificate fields. Additionally, an integrated security module enhances communication security by enforcing Access Control Lists (ACLs), hardening TLS configuration, and mitigating the risk of private key hijacking. From an availability perspective, the limited flow table capacity of switches leads to table saturation attacks. Besides, the disaggregated and layered architecture of SDN is susceptible to time-based fingerprinting attacks. To address this, we introduce an automated attacker tool that utilizes probing-based measurements for fingerprinting. This tool can discern network types (SDN or traditional), extract flow rule timeout values (hard and idle), determine flow table utilization rate, size, and replacement algorithm. Armed with this information, the attacker can execute intelligent saturation attacks. Furthermore, we propose a lightweight defense mechanism that randomizes rule timeouts and proactively deletes flow rules based on network status. Through comprehensive simulations under various network conditions, we demonstrate the efficacy of our proposed techniques, achieving superior success rates across diverse scenarios.
