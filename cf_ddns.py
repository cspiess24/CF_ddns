"""
Simple script to update CloudFlare DNS entry.
Schedule the script to run at a desired interval.
This will only update CloudFlare in the event your IP address has changed.
"""
import logging
from requests import get
from requests.exceptions import RequestException
import CloudFlare


def get_public_ip():
    try:
        ip = get('https://api.ipify.org').text
        logging.info('My public IP address is: {}'.format(ip))
    except RequestException as error:
        exit(error)

    return ip


def check_ip(cf, dns_name, ip_address, record_type, zone_id):
    params = {
        'name': dns_name,
        'type': record_type
    }

    try:
        dns_record = cf.zones.dns_records.get(zone_id, params=params)
        logging.debug(dns_record)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones/dns_records %s - %d %s - api call failed' % (dns_name, e, e))

    old_ip_address = dns_record[0]['content']

    if ip_address == old_ip_address:
        return False
    return dns_record[0]


def update_record(cf, dns_record, dns_name, record_type, ip_address, zone_id):
    dns_record_id = dns_record['id']
    dns_record = {
        'name': dns_name,
        'type': record_type,
        'content': ip_address
    }

    try:
        dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit('/zones.dns_records.put {} - {} {} - api call failed'.format(dns_name, e, e))
    logging.info('UPDATED: {} -> {}'.format(dns_name, ip_address))


def main():
    email = ''
    api_key = ''
    zone_id = ''
    dns_name = ''
    record_type = 'A'

    cf = CloudFlare.CloudFlare(email=email, token=api_key)

    ip_address = get_public_ip()

    dns_record = check_ip(cf, dns_name, ip_address, record_type, zone_id)

    if dns_record:
        update_record(cf, dns_record, dns_name, record_type, ip_address, zone_id)


if __name__ == '__main__':
    main()
