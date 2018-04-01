# CloudFlare Dynamic DNS updater

This is a simple script to update an A record with CloudFlare.

## Getting Started

You will need to install the Cloudflare python wrapper. 

```
pip install cloudflare
```

Download the cf_ddns.py file and update the settings below for your environment.

## Settings

**Email:** Your CloudFlare email address

**API KEY:** API Key found under your profile

**Zone ID:** You can find directions for getting the Zone ID [here](https://api.cloudflare.com/#getting-started-resource-ids)

**DNS Name:** The FQDN that you would like updated. 