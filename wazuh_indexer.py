#! /usr/bin/python3

import os
from pathlib import Path
#from dotenv import load_dotenv

load_dotaenv()

# Generating the SSL Certificates
os.system("curl -sO https://packages.wazuh.com/4.3/wazuh-certs-tool.sh")
os.system("curl -sO https://packages.wazuh.com/4.3/config.yml")
# Edit Config.yml
file=Path('config.yml')
# Indexer
file.write_text(file.read_text().replace('node-1',os.getenv("EAADD")))
file.write_text(file.read_text().replace('<indexer-node-ip',os.getenv("EAAZZ")))
# Server
file.write_text(file.read_text().replace('wazuh-1',os.getenv("EBBDD")))
file.write_text(file.read_text().replace('<wazuh-manager>',os.getenv("EAAZZ")))
# Dashboard
file.write_text(file.read_text().replace('dashboard',os.getenv("ECCDD")))
file.write_text(file.read_text().replace('<dashboard-node-ip>',os.getenv("EAAZZ")))

# Nodes Installation
os.system("apt install debconf adduser procps")

# Adding Wazuh Repository
os.system("apt install gnupg apt-transport-https")
os.system("curl -s https://packages.wazuh.com/key/GPG-KEY-WAZUH | apt-key add -")
os.system('echo "deb {} stable main" | tee -a /etc/apt/sources.list.d/wazuh.list'.format(os.getenv("FFGGYY")))
os.system("apt-get update")

# Configuring Wazuh Indexer
file2=Path("/etc/wazuh-indexer/opensearch.yml")
file2.write_text(file2.read_text().replace('0.0.0.0',os.getenv("EAAZZ")))
file2.write_text(file2.read_text().replace('node-1',os.getenv("EAADD")))

# Adding Master Nodes
if os.getenv("ESSHH") != '':
    os.system('sed -i "/node-2/s/^#//g" {}'.format(file2))
    file2.write_text(file2.read_text().replace('node-2',os.getenv("ESSHH")))
if os.getenv("EFFSS") != '':
    os.system('sed -i "/node-3/s/^#//g" {}'.format(file2))
    file2.write_text(file2.read_text().replace('node-3'),os.getenv("EFFSS"))

# Discovery.seed_hosts
if os.getenv("DDFFJJ") != "":
    os.system('sed -i "/10.0.0.1/s/^#//g" {}'.format(file2))
file2.write_text(file2.read_text().replace('10.0.0.1',os.getenv("DDFFJJ")))
if os.getenv("JJYYFF") != "":
    os.system('sed -i "/10.0.0.2/s/^#//g" {}'.format(file2))
    file2.write_text(file2.read_text().replace('10.0.0.2',os.getenv("JJYYFF")))
if os.getenv("AAJJSS") != "":
    os.system('sed -i "/10.0.0.3/s/^#//g" {}'.format(file2))
    file2.write_text(file2.read_text().replace('10.0.0.3',os.getenv("AAJJSS")))

# List of the Distinguished Names of the certificates
file2.write_text(file2.read_text().replace('CN={},OU=Wazuh,O=Wazuh,L=California,C=US'.format(os.getenv("EAADD"))))
if os.getenv("ESSHH") != '':
    file2.write_text(file2.read_text().replace('CN={},OU=Wazuh,O=Wazuh,L=California,C=US',os.getenv("ESSHH")))
    os.system('sed -i "/{}/s/^#//g" {}'.format(os.getenv("ESSHH"),file2))
if os.getenv("EFFSS") != '':
    file2.write_text(file2.read_text().replace('CN={},OU=Wazuh,O=Wazuh,L=California,C=US',os.getenv("EFFSS")))
    os.system('sed -i "/{}/s/^#//g" {}'.format(os.getenv("EFFSS"),file2))

# Deploying Certificates
os.system("mkdir /etc/wazuh-indexer/certs")
os.system("tar -xf ./wazuh-certificates.tar -C /etc/wazuh-indexer/certs/ ./{}.pem ./{}-key.pem ./admin.pem ./admin-key.pem ./root-ca.pem".format(os.getenv("EAADD"),os.getenv("EAADD")))
os.system("mv -n /etc/wazuh-indexer/certs/{}.pem /etc/wazuh-indexer/certs/indexer.pem".format(os.getenv("EAADD")))
os.system("mv -n /etc/wazuh-indexer/certs/{}-key.pem /etc/wazuh-indexer/certs/indexer-key.pem".format(os.getenv("EAADD")))
os.system("chmod 500 /etc/wazuh-indexer/certs")
os.system("chmod 400 /etc/wazuh-indexer/certs/*")
os.system("chown -R wazuh-indexer:wazuh-indexer /etc/wazuh-indexer/certs")

# Starting The Service
os.system("systemctl daemon-reload") 
os.system("systemctl enable wazuh-indexer")
os.system("systemctl start wazuh-indexer")

# Cluster initialization
os.system("/usr/share/wazuh-indexer/bin/indexer-security-init.sh")

# Testing The Cluster Installation
os.system("curl -k -u admin:admin https://",os.getenv("EAAZZ"),":9200")
# Check Cluster is Working
os.system("curl -k -u admin:admin https://",os.getenv("EAAZZ"),":9200/_cat/nodes?v")