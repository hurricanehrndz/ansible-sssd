Ansible Role SSSD
========

[![Build Status](https://travis-ci.org/Turgon37/ansible-sssd.svg?branch=master)](https://travis-ci.org/Turgon37/ansible-sssd)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-Turgon37.sssd-blue.svg)](https://galaxy.ansible.com/Turgon37/sssd/)

## Description

:grey_exclamation: Before using this role, please know that all my Ansible roles are fully written and accustomed to my IT infrastructure. So, even if they are as generic as possible they will not necessarily fill your needs, I advice you to carrefully analyse what they do and evaluate their capability to be installed securely on your servers.

This roles configures SSSD authentication service backend.

## Requirements

Require Ansible >= 2.4

### Dependencies

If you use the zabbix monitoring profile you will need the role [ansible-zabbix-agent](https://github.com/Turgon37/ansible-zabbix-agent)

## OS Family

This role is available for Debian and CentOS

## Features

At this day the role can be used to :

  * install sssd
  * configure service and domains
  * monitoring items for
    * Zabbix
  * [local facts](#facts)

## Configuration

### Server

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in table below. To see default values please refer to this file.

| Name                           | Types/Values   | Description                                                                              |
| -------------------------------|----------------| ---------------------------------------------------------------------------------------- |
| `sssd__domains`                | List of string | List of domains to declare in sssd                                                       |
| `sssd__services`               | List of string | List of services to enable                                                               |
| `sssd__services_settings`      | Dict of dict   | Each key is a service name, and each value is a dict of option that apply on that service|
| `sssd__service_nss_settings`   | Dict of string | Specific settings that apply on nss service                                              |
| `sssd__service_pam_settings`   | Dict of string | Specific settings that apply on pam service                                              |
| `sssd__service_sudo_settings`  | Dict of string | Specific settings that apply on sudo service                                             |
| `sssd__service_autofs_settings | Dict of string | Specific settings that apply on autofs service                                           |
| `sssd__service_ssh_settings`   | Dict of string | Specific settings that apply on ssh service                                              |
| `sssd__service_pac_settings`   | Dict of string | Specific settings that apply on pac service                                              |
| `sssd__service_ifp_settings`   | Dict of string | Specific settings that apply on ifp service                                              |
| `sssd__filter_users`           |                | Exclude theses users from sss fetchs                                                     |
| `sssd__filter_groups`          |                | Exclude theses groups from sss fetchs                                                    |

* Using service settings

The multiple ways to declare services settings allow you to set them from multiple sources.
The final set of options that will be applied is the results of the merge of the following dicts in this respective order :

* the global defaults sssd__services_settings_default
* the global user settings sssd__services_settings
* the specific defaults sssd__services_[service_name]_settings_default
* the specific user settings sssd__services_[service_name]_settings_default

The multiple way to declare


## Facts

By default the local fact are installed and expose the following variables :

* ```ansible_local.sssd.version_full```
* ```ansible_local.sssd.version_major```


## Example

### Playbook

Use it in a playbook as follows:

```yaml
- hosts: all
  roles:
    - turgon37.openvpn
```

### Inventory