# Containerized File Sharing Platform
CloudTransfer is a lightweight, containerized file-sharing platform inspired by services like WeTransfer. It allows users to upload individual files or entire folders through a web interface and receive a direct download link. The system is designed with DevOps principles in mind - it is modular, scalable, observable, and easy to deploy.

## Key Features:
* File and folder upload via a simple web interface
* Automatic folder zipping on the server side
* Unique download link generation per upload
* Real-time monitoring using Prometheus and Grafana
* Horizontal scalability using docker-compose up --scale
* Fault-tolerant routing through NGINX reverse proxy

## Architecture Overview

Frontend: Static HTML/JS/CSS interface for file/folder upload

Backend: Flask API handling uploads, downloads, and exposing Prometheus metrics

Storage: Shared Docker volume to persist uploaded files

NGINX Proxy: Load balancer that routes traffic to backend replicas based on container metadata

Prometheus: Collects metrics (uploads, downloads, file sizes)

Grafana: Visualizes collected metrics via pre-configured dashboards

## Technologies Used

* Python 3.11
* Flask

* HTML5, CSS3, JavaScript
* Docker

* Docker Compose

* NGINX (jwilder/nginx-proxy)
* Prometheus

* Grafana

## Project structure
  ```
  cloud_transfer/
  ├── backend/ │
  ├── app.py
  │ └── templates/
  │ └── download.html
  ├── frontend/
  │  ├── index_front.html
  │ └── script.js
  ├── prometheus/
  │ └── prometheus.yml
  ├──  grafana/
  │ └── provisioning/
  │ ├── datasources/
  │ │ └── prometheus.yml
  │ └── dashboards/
  │ └── cloudtransfer.json
  ├── uploads/
  ├── docker-compose.yml
  ├── nginx-custom.conf
  └── README.md
  ```

## Deployment
### To launch the platform with n backend replicas:
 ``  docker-compose up --scale backend=n ``

 ### To stop the platform:
 `` docker-compose down``

Open http://localhost to start using the app

Grafana dashboard is available at http://localhost:3000

Prometheus dashboard is available at http://localhost:9090




