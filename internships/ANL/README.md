## Ansible-Based NVIDIA Jetson Nano Edge Deployment

Complete automation solution for deploying and managing NVIDIA Jetson Nano edge devices at scale using Ansible. This project provides production-ready infrastructure-as-code for environment setup, dependency management, CI/CD automation, monitoring, and fleet management.

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Deployment Workflows](#deployment-workflows)
- [Monitoring and Logging](#monitoring-and-logging)
- [Fleet Management](#fleet-management)
- [Failure Recovery](#failure-recovery)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Capabilities

- **Automated Environment Setup**: One-command deployment of complete Jetson Nano environment
- **Dependency Management**: Controlled installation and version management of system packages, Python libraries, and CUDA dependencies
- **CI/CD Automation**: Jenkins/GitLab CI integration for continuous deployment
- **Monitoring & Logging**: Centralized logging with Prometheus, Grafana, and ELK stack support
- **Fleet Management**: Scale from single device to hundreds of edge nodes
- **Reproducibility**: Idempotent playbooks ensure consistent deployments
- **Failure Recovery**: Automated rollback and health check mechanisms
- **Production Ready**: Battle-tested configurations with security hardening

### Key Benefits

- Reduce deployment time from hours to minutes
- Ensure consistency across all edge devices
- Enable rapid rollback on deployment failures
- Centralize configuration management
- Automate routine maintenance tasks
- Scale effortlessly from 1 to 1000+ devices

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Control Node (Ansible)                    │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  Playbooks │  │  Inventory  │  │  Configuration Vars  │ │
│  └────────────┘  └─────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ SSH/Ansible
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Edge Device Fleet                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Jetson Nano  │  │ Jetson Nano  │  │ Jetson Nano  │ ...  │
│  │   Device 1   │  │   Device 2   │  │   Device N   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Metrics/Logs
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Monitoring & Logging Stack                      │
│  ┌───────────┐  ┌──────────┐  ┌────────────┐               │
│  │ Prometheus│  │ Grafana  │  │ ELK Stack  │               │
│  └───────────┘  └──────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Control Node Requirements

- **Operating System**: Ubuntu 20.04/22.04, RHEL 8+, or macOS
- **Ansible**: Version 2.10 or higher
- **Python**: 3.8+
- **SSH Access**: Passwordless SSH configured to all Jetson Nano devices
- **Network**: Connectivity to all target devices

### Target Device Requirements

- **Hardware**: NVIDIA Jetson Nano (2GB or 4GB model)
- **OS**: JetPack 4.6+ or Ubuntu 18.04/20.04 for Jetson
- **Network**: Static IP or reliable DHCP reservation
- **Storage**: Minimum 32GB SD card (64GB+ recommended)
- **SSH**: OpenSSH server enabled

### Installation on Control Node

```bash
# Install Ansible
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install -y ansible

# Verify installation
ansible --version

# Install required Python packages
pip3 install netaddr jinja2 jmespath

# Install Ansible Galaxy collections
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.posix
```

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/jetson-nano-ansible.git
cd jetson-nano-ansible
```

### 2. Configure Inventory

Edit `inventory/hosts.yml`:

```yaml
all:
  children:
    jetson_nano:
      hosts:
        jetson-01:
          ansible_host: 192.168.1.101
        jetson-02:
          ansible_host: 192.168.1.102
      vars:
        ansible_user: nvidia
        ansible_python_interpreter: /usr/bin/python3
```

### 3. Configure Variables

Edit `group_vars/jetson_nano.yml`:

```yaml
# System Configuration
jetson_hostname_prefix: "jetson-edge"
timezone: "America/New_York"

# Application Settings
app_version: "1.0.0"
deployment_user: "nvidia"
deployment_path: "/opt/edge-app"

# Monitoring
enable_monitoring: true
prometheus_port: 9090
```

### 4. Test Connectivity

```bash
ansible jetson_nano -i inventory/hosts.yml -m ping
```

### 5. Run Full Deployment

```bash
ansible-playbook -i inventory/hosts.yml playbooks/site.yml
```

## Project Structure

```
jetson-nano-ansible/
├── ansible.cfg                 # Ansible configuration
├── inventory/
│   ├── hosts.yml              # Device inventory
│   ├── group_vars/
│   │   ├── all.yml           # Global variables
│   │   └── jetson_nano.yml   # Jetson-specific vars
│   └── host_vars/            # Per-device variables
│       └── jetson-01.yml
├── playbooks/
│   ├── site.yml              # Main deployment playbook
│   ├── setup.yml             # Initial setup
│   ├── deploy.yml            # Application deployment
│   ├── monitoring.yml        # Monitoring setup
│   ├── update.yml            # Update existing deployment
│   └── rollback.yml          # Rollback mechanism
├── roles/
│   ├── common/               # Common system configuration
│   ├── jetson_setup/         # Jetson-specific setup
│   ├── docker/               # Docker installation
│   ├── cuda/                 # CUDA/cuDNN setup
│   ├── application/          # Application deployment
│   ├── monitoring/           # Monitoring agents
│   └── logging/              # Logging configuration
├── templates/                # Jinja2 templates
├── files/                    # Static files
├── scripts/                  # Helper scripts
├── docs/                     # Additional documentation
└── README.md                 # This file
```

## Configuration

### Global Configuration (ansible.cfg)

```ini
[defaults]
inventory = inventory/hosts.yml
remote_user = nvidia
host_key_checking = False
retry_files_enabled = False
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 3600

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
pipelining = True
```

### Environment-Specific Variables

Create environment-specific variable files:

**group_vars/development.yml**:
```yaml
environment: development
log_level: debug
enable_debug_tools: true
```

**group_vars/production.yml**:
```yaml
environment: production
log_level: info
enable_debug_tools: false
security_hardening: true
```

### Sensitive Variables (Ansible Vault)

```bash
# Create encrypted vault file
ansible-vault create group_vars/vault.yml

# Add sensitive data
---
vault_ssh_private_key: "{{ lookup('file', '~/.ssh/id_rsa') }}"
vault_api_token: "your-secret-token"
vault_db_password: "super-secret-password"

# Edit vault
ansible-vault edit group_vars/vault.yml

# Use vault in playbooks
ansible-playbook playbooks/site.yml --ask-vault-pass
```

## Deployment Workflows

### Initial Device Setup

```bash
# Complete first-time setup
ansible-playbook -i inventory/hosts.yml playbooks/setup.yml

# Setup specific components
ansible-playbook -i inventory/hosts.yml playbooks/setup.yml --tags "system,docker"
```

### Application Deployment

```bash
# Deploy application
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml

# Deploy to specific host
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --limit jetson-01

# Deploy specific version
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -e "app_version=2.0.0"
```

### Update Existing Deployment

```bash
# Update all devices
ansible-playbook -i inventory/hosts.yml playbooks/update.yml

# Update with zero-downtime
ansible-playbook -i inventory/hosts.yml playbooks/update.yml -e "rolling_update=true"
```

### Rollback

```bash
# Rollback to previous version
ansible-playbook -i inventory/hosts.yml playbooks/rollback.yml

# Rollback to specific version
ansible-playbook -i inventory/hosts.yml playbooks/rollback.yml -e "rollback_version=1.5.0"
```

## Monitoring and Logging

### Monitoring Stack Setup

```bash
# Deploy monitoring agents
ansible-playbook -i inventory/hosts.yml playbooks/monitoring.yml

# Components installed:
# - Node Exporter (system metrics)
# - cAdvisor (container metrics)
# - Filebeat (log shipping)
# - Custom Jetson metrics exporter
```

### Prometheus Configuration

```yaml
# prometheus.yml (auto-generated)
scrape_configs:
  - job_name: 'jetson-nodes'
    static_configs:
      - targets: 
        - 'jetson-01:9100'
        - 'jetson-02:9100'
    
  - job_name: 'jetson-containers'
    static_configs:
      - targets:
        - 'jetson-01:8080'
        - 'jetson-02:8080'
```

### Grafana Dashboards

Pre-configured dashboards available:
- Jetson System Overview
- GPU/CPU Utilization
- Memory and Thermal Monitoring
- Container Performance
- Application Metrics

### Log Aggregation

```bash
# View logs from all devices
ansible jetson_nano -i inventory/hosts.yml -m shell -a "journalctl -u edge-app --since '1 hour ago'"

# Centralized logging with ELK
# Logs automatically shipped to Elasticsearch
# Access Kibana: http://your-elk-server:5601
```

## Fleet Management

### Inventory Management

**Dynamic Inventory Example**:

```python
#!/usr/bin/env python3
# inventory/dynamic_inventory.py

import json
import requests

def get_inventory():
    # Fetch from your device management API
    response = requests.get('https://api.example.com/devices')
    devices = response.json()
    
    inventory = {
        'jetson_nano': {
            'hosts': [],
            'vars': {}
        }
    }
    
    for device in devices:
        inventory['jetson_nano']['hosts'].append(device['hostname'])
    
    return inventory

if __name__ == '__main__':
    print(json.dumps(get_inventory(), indent=2))
```

### Fleet-Wide Operations

```bash
# Update all devices
ansible-playbook -i inventory/hosts.yml playbooks/update.yml

# Staged rollout (10% at a time)
ansible-playbook -i inventory/hosts.yml playbooks/update.yml -e "serial=10%"

# Reboot all devices
ansible jetson_nano -i inventory/hosts.yml -m reboot -a "reboot_timeout=300"

# Check fleet health
ansible jetson_nano -i inventory/hosts.yml -m shell -a "uptime && nvidia-smi"
```

### Grouping and Targeting

```yaml
# inventory/hosts.yml
all:
  children:
    jetson_nano:
      children:
        production:
          hosts:
            jetson-prod-01:
            jetson-prod-02:
        staging:
          hosts:
            jetson-stage-01:
        datacenter_a:
          hosts:
            jetson-dc-a-01:
            jetson-dc-a-02:
```

```bash
# Target specific groups
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --limit production
ansible-playbook -i inventory/hosts.yml playbooks/update.yml --limit datacenter_a
```

## Failure Recovery

### Health Checks

```yaml
# roles/application/tasks/health_check.yml
- name: Wait for application to be healthy
  uri:
    url: "http://{{ ansible_host }}:8000/health"
    status_code: 200
  register: health_check
  until: health_check.status == 200
  retries: 30
  delay: 10
```

### Automatic Rollback

```yaml
# playbooks/deploy.yml
- name: Deploy application
  hosts: jetson_nano
  serial: 1
  tasks:
    - block:
        - name: Deploy new version
          include_role:
            name: application
            
        - name: Health check
          include_tasks: health_check.yml
          
      rescue:
        - name: Rollback on failure
          include_role:
            name: application
          vars:
            app_version: "{{ previous_version }}"
            
        - name: Send failure notification
          slack:
            token: "{{ slack_token }}"
            msg: "Deployment failed on {{ inventory_hostname }}, rolled back"
```

### Backup and Restore

```bash
# Backup current state
ansible-playbook -i inventory/hosts.yml playbooks/backup.yml

# Restore from backup
ansible-playbook -i inventory/hosts.yml playbooks/restore.yml -e "backup_date=2024-01-15"
```

## CI/CD Integration

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['staging', 'production'],
            description: 'Target environment'
        )
        string(
            name: 'VERSION',
            defaultValue: 'latest',
            description: 'Application version to deploy'
        )
    }
    
    stages {
        stage('Validate') {
            steps {
                sh '''
                    ansible-playbook -i inventory/hosts.yml \
                    playbooks/validate.yml \
                    --limit ${ENVIRONMENT}
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    ansible-playbook -i inventory/hosts.yml \
                    playbooks/deploy.yml \
                    --limit ${ENVIRONMENT} \
                    -e "app_version=${VERSION}"
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                sh '''
                    ansible-playbook -i inventory/hosts.yml \
                    playbooks/health_check.yml \
                    --limit ${ENVIRONMENT}
                '''
            }
        }
    }
    
    post {
        failure {
            sh '''
                ansible-playbook -i inventory/hosts.yml \
                playbooks/rollback.yml \
                --limit ${ENVIRONMENT}
            '''
        }
    }
}
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - deploy
  - verify

variables:
  ANSIBLE_FORCE_COLOR: "true"

validate:
  stage: validate
  script:
    - ansible-playbook -i inventory/hosts.yml playbooks/validate.yml --syntax-check
    - ansible-lint playbooks/

deploy_staging:
  stage: deploy
  script:
    - ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --limit staging
  only:
    - develop

deploy_production:
  stage: deploy
  script:
    - ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --limit production
  only:
    - main
  when: manual

verify:
  stage: verify
  script:
    - ansible-playbook -i inventory/hosts.yml playbooks/health_check.yml
```

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Jetson Fleet

on:
  push:
    branches: [ main ]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install Ansible
        run: |
          pip install ansible
          ansible-galaxy collection install community.general
          
      - name: Deploy
        env:
          ANSIBLE_VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
        run: |
          echo "$ANSIBLE_VAULT_PASSWORD" > .vault_pass
          ansible-playbook -i inventory/hosts.yml \
            playbooks/deploy.yml \
            --limit ${{ inputs.environment || 'staging' }} \
            --vault-password-file .vault_pass
```

## Troubleshooting

### Common Issues

**SSH Connection Failures**:
```bash
# Test SSH connection
ssh nvidia@192.168.1.101

# Verify SSH key
ansible jetson_nano -i inventory/hosts.yml -m ping

# Debug connection
ansible jetson_nano -i inventory/hosts.yml -m ping -vvv
```

**Permission Errors**:
```bash
# Check sudo access
ansible jetson_nano -i inventory/hosts.yml -m shell -a "whoami" --become

# Configure passwordless sudo on Jetson
echo "nvidia ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/nvidia
```

**Slow Playbook Execution**:
```bash
# Enable pipelining and fact caching (already in ansible.cfg)
# Use serial execution for large fleets
ansible-playbook playbooks/deploy.yml -e "serial=5"
```

**Module Not Found**:
```bash
# Install missing collections
ansible-galaxy collection install community.general ansible.posix

# List installed collections
ansible-galaxy collection list
```

### Debug Mode

```bash
# Run with maximum verbosity
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml -vvvv

# Run specific tasks with debug
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --start-at-task="Deploy application"

# Check facts gathered from device
ansible jetson-01 -m setup
```

### Validation and Testing

```bash
# Syntax check
ansible-playbook playbooks/site.yml --syntax-check

# Dry run (check mode)
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --check

# Lint playbooks
ansible-lint playbooks/

# Run specific role tests
molecule test -s jetson_setup
```

## Best Practices

### Security

1. **Use Ansible Vault** for sensitive data
2. **Implement SSH key-based authentication** (no passwords)
3. **Enable security hardening** role in production
4. **Regularly update** all dependencies
5. **Restrict sudo access** to required commands only

### Performance

1. **Enable fact caching** to reduce gathering time
2. **Use pipelining** for faster SSH operations
3. **Implement serial execution** for large fleets
4. **Minimize tasks** in frequently-run playbooks
5. **Use async tasks** for long-running operations

### Reliability

1. **Always implement health checks** after deployments
2. **Use handlers** for service restarts
3. **Implement rollback mechanisms** for critical updates
4. **Test in staging** before production deployment
5. **Monitor playbook execution** times and failures

### Maintainability

1. **Use roles** for reusable components
2. **Keep playbooks simple** and focused
3. **Document variables** and their purposes
4. **Version control everything**
5. **Use descriptive task names**

### Testing Strategy

```bash
# Local testing with Vagrant
vagrant up
ansible-playbook -i .vagrant/provisioners/ansible/inventory playbooks/site.yml

# Staging deployment
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --limit staging

# Production deployment
ansible-playbook -i inventory/hosts.yml playbooks/deploy.yml --limit production
```

## Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/jetson-nano-ansible.git
cd jetson-nano-ansible

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linting
ansible-lint playbooks/
yamllint .
```


## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/jetson-nano-ansible/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/jetson-nano-ansible/discussions)

## Acknowledgments

- NVIDIA for Jetson platform
- Ansible community for excellent automation tools
- Contributors and users of this project
