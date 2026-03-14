# centralized log management system - ELK stack

This project implements a centralized logging system using Filebeat, Logstash, Elasticsearch, and Kibana deployed on Amazon EC2 instances.

In this setup, Filebeat is installed on a web server to collect log files and send them to a centralized Logstash server. Logstash processes and forwards the logs to Elasticsearch, where the data is stored and indexed. Kibana is used to visualize and analyze the logs through dashboards and search tools.

This architecture helps system administrators monitor server activity, troubleshoot issues, and analyze application logs from a single location instead of checking each server individually.

## Project Architecture

```text
EC2-1 (ELK Server)
 ├─ Elasticsearch
 ├─ Logstash
 └─ Kibana

EC2-2 (Client Server)
 └─ Filebeat (log shipper)
```

### Tools used:
   - Filebeat → sends logs from client server
   - Logstash → processes logs
   - Elasticsearch → stores logs
   - Kibana → dashboard

## Step 1 — Install Elasticsearch on ELK Server

1 - Install Java and Elasticsearch
```text
sudo apt update
sudo apt install openjdk-11-jdk -y
```

2 - Install Elasticsearch
```text
sudo apt install elasticsearch
```

3 - Start service
```text
sudo systemctl start elasticsearch
sudo systemctl enable elasticsearch
```

If display Elasticsearch “package not found” problem.
- Add the Elastic GPG Key
```text
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```
- Add the Elastic APT Repository
```text
echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
```
After install Elastic package

## Step 2 — Install Logstash

1 - Install Logstash
```text
sudo apt install logstash
```

2 - Create configuration
```text
sudo nano /etc/logstash/conf.d/logstash.conf
```
logstash.conf
```text
input {
  beats {
    port => 5044
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
  }
}
```
3 - Start Logstash
```text
sudo systemctl start logstash
```

## Step 3 — Install Kibana

1 - Install Kibana
```text
sudo apt install kibana
```
2 - Edit config
```text
sudo nano /etc/kibana/kibana.yml
```
3 - Change
```text
server.host: "0.0.0.0"
```
4 - Start service:
```text
sudo systemctl start kibana
sudo systemctl enable kibana
```
5 - Access from browser
```text
http://EC2_PUBLIC_IP:5601
```

## Step 4 — Install Filebeat on Client Server

1 - Install Filebeat
```text
sudo apt install filebeat
```
2 - Edit configuration:
```text
sudo nano /etc/filebeat/filebeat.yml
```
3 - Find
```text
output.elasticsearch
```
Disable it.
4 - Enable Logstash
```text
output.logstash:
  hosts: ["ELK_SERVER_IP:5044"]
```
5 - Start Filebeat:
```text
sudo systemctl start filebeat
```

## Step 5 — Create Kibana Dashboard

1 - Open
```text
http://ELK_SERVER_IP:5601
```
2 - Create enrolment token and its use for login Kibana first time
```text
sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```
3 - Kibana verification code get and enter for Kibana gui
```text
sudo /usr/share/kibana/bin/kibana --allow-root
```

![Cron Framework Architecture](kibanaimage.png)




