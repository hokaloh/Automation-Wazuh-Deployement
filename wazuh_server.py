#! /usr/bin/python3

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotaenv()

# Wazuh Server Node Installation
os.system("apt install gnupg apt-transport-https") 
os.system("curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add -")
os.system('echo "deb {} stable main" | tee -a /etc/apt/sources.list.d/wazuh.list'.format(os.getenv("FFGGYY")))
os.system("apt-get update")

# Installing Wazuh Manager
os.system("apt -y install wazuh-manager")

# Enable Wazuh Manager
os.system("systemctl daemon-reload")
os.system("systemctl enable wazuh-manager")
os.system("systemctl start wazuh-manager")

# Wazuh Manager Status
os.system("systemctl status wazuh-manager")

## Installing Filebeat
os.system("apt -y install filebeat")

# Configure preFilebeat
os.system("curl -so /etc/filebeat/filebeat.yml {}".format(os.getenv("HHYYGG")))

file3=Path('/etc/filebeat/filebeat.yml')
file3.write_text(file3.read_text().replace('10.0.0.1',os.getenv("EAAZZ")))
file3.write_text(file3.read_text().replace('${username}','admin'))
file3.write_text(file3.read_text().replace('${password}','admin'))

# Create Filebeat keystone = To Secure Auth Credential
os.system("filebeat keystore create")

# Put username and password to secret keystone
os.system("echo admin | filebeat keystore add username --stdin --force")
os.system("echo admin | filebeat keystore add password --stdin --force")

# Download Alert template for Wazuh Indexer
os.system("curl -so /etc/filebeat/wazuh-template.json {}".format(os.getenv("KKYYGG")))
os.system("chmod go+r /etc/filebeat/wazuh-template.json")

# Download Wazuh Module Filebeat
os.system("curl -s {} | tar -xvz -C /usr/share/filebeat/module".format(os.getenv("VVTTHH")))

# Deploying certificates
os.system("mkdir /etc/filebeat/certs")
os.system("tar -xf ./wazuh-certificates.tar -C /etc/filebeat/certs/ ./{}.pem ./{}-key.pem ./root-ca.pem".format(os.getenv("EAADD"),os.getenv("EAADD")))
os.system("mv -n /etc/filebeat/certs/{}.pem /etc/filebeat/certs/filebeat.pem".format(os.getenv("EAADD")))
os.system("mv -n /etc/filebeat/certs/{}-key.pem /etc/filebeat/certs/filebeat-key.pem".format(os.getenv("EAADD")))
os.system("chmod 500 /etc/filebeat/certs")
os.system("chmod 400 /etc/filebeat/certs/*")
os.system("chown -R root:root /etc/filebeat/certs")

# Starting Filebeat Service 
os.system("systemctl daemon-reload")
os.system("systemctl enable filebeat")
os.system("systemctl start filebeat")

# Verify Filebeat is succeffuly installed
os.system("filebeat test output")