#! /usr/bin/python3

import os
from pathlib import Path
#from dotenv import load_dotenv

load_dotaenv()

# # Wazuh Dashboard # #

# Installing Package depencies
os.system("apt install debhelper tar curl libcap2-bin")

# Adding Wazuh Repository 
os.system("apt install gnupg apt-transport-https") 
os.system("curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add -")
os.system('echo "deb {} stable main" | tee -a /etc/apt/sources.list.d/wazuh.list'.format(os.getenv("FFGGYY")))
os.system("apt-get update")

# Installing Wazuh Dashboard
os.system("apt -y install wazuh-dashboard")

# Configuring Wazuh Dashboard
file4=Path('/etc/wazuh-dashboard/opensearch_dashboards.yml')
file4.write_text(file4.read_text().replace('locahost',os.getenv("EAAZZ")))

# Deploying certificates
os.system("mkdir /etc/wazuh-dashboard/certs")
os.system("tar -xf ./wazuh-certificates.tar -C /etc/wazuh-dashboard/certs/ ./{}.pem ./{}-key.pem ./root-ca.pem".format(os.getenv("EAADD"),os.getenv("EAADD")))
os.system("mv -n /etc/wazuh-dashboard/certs/{}.pem /etc/wazuh-dashboard/certs/dashboard.pem".format(os.getenv("EAADD")))
os.system("mv -n /etc/wazuh-dashboard/certs/{}-key.pem /etc/wazuh-dashboard/certs/dashboard-key.pem".format(os.getenv("EAADD")))
os.system("chmod 500 /etc/wazuh-dashboard/certs")
os.system("chmod 400 /etc/wazuh-dashboard/certs/*")
os.system("chown -R wazuh-dashboard:wazuh-dashboard /etc/wazuh-dashboard/certs")

# Starting Wazuh Dashboard Service
os.system("systemctl daemon-reload")
os.system("systemctl enable wazuh-dashboard")
os.system("systemctl start wazuh-dashboard")