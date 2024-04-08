import json
import os
import argparse
import sys
import re
import yaml
import logging


def flattened_items(items, prefix=''):
    result = []
    for item in items:
        if 'item' in item:
            name = item['name'][0].upper() + item['name'][1:]
            p = prefix + name.replace(' ', '').replace('-', '') + '.'
            result.extend(
                flattened_items(item['item'], p))
        else:
            result.extend([(prefix.rstrip('.'), item)])
    return result


def generate_from_postman(file_path, logger, root_dir):
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    with open(file_path, 'r', encoding='utf-8') as f:
        postman = json.load(f)
    version_regex = re.compile(r'^v\d(?:\.\d+)?$')
    endpoints = {
        'scheme': 'https',
        'domain': 'vandar.io',
        'subdomains': {},
    }
    items = flattened_items(postman['item'])

    for label, endpoint in items:
        name = endpoint['name'].split('\n')[0].lower().replace(' ', '_').replace('-', '_')
        request = endpoint['request']
        method = request['method']
        host = request['url']['host']
        if len(host) < 2:
            logger.error(f"Invalid host: {host} for endpoint {name} in {label}; skipping")
            continue
        if host[-1] != 'io' or host[-2] != 'vandar':
            logger.error(f"Invalid host: {host} for endpoint {name} in {label}; skipping")
            continue
        subdomain = '.'.join(host[:-2]) if len(host) > 2 else '@'
        endpoints['subdomains'][subdomain] = endpoints['subdomains'].get(subdomain, {})
        path = request['url']['path']
        if not path:
            logger.error(f"Invalid path: {path} for endpoint {name} in {label}; skipping")
            continue
        version = '@'
        for part in path:
            if version_regex.match(part):
                version = part
                break
        if version == '@':
            logger.warning(f"Version not found in path: {path} for endpoint {name} in {label}")
        endpoints['subdomains'][subdomain][version] = endpoints['subdomains'][subdomain].get(version, {})

        scheme = request['url']['protocol']
        if scheme != 'https':
            logger.error(f"Invalid or unsecure scheme: {scheme} for endpoint {name} in {label}; skipping")
            continue
        partial_path = '/'.join(path).replace('{{', '{').replace('}}', '}')
        full_path = f"{scheme}://{subdomain}.vandar.io/{partial_path}"
        name = f"{label}.{name}"
        if name in endpoints['subdomains'][subdomain][version]:
            logger.error(f"Duplicate endpoint: {name} in {label}; skipping")
            continue
        endpoints['subdomains'][subdomain][version][name] = {
            'method': method,
            'path': partial_path,
            'full_path': full_path,
            'label': label,
        }
    with open(os.path.join(root_dir, "vandarpy", "endpoints.yaml"), 'w', encoding='utf-8') as f:
        yaml.dump(endpoints, f)


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.propagate = False
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser = argparse.ArgumentParser()
    mutually_exclusive_group = parser.add_mutually_exclusive_group(required=True)

    mutually_exclusive_group.add_argument(
        "--list", action="store_true", help="List all available endpoints"
    )
    mutually_exclusive_group.add_argument(
        "--get",
        type=str,
        help="Get the endpoint details by label",
        metavar="LABEL",
    )
    mutually_exclusive_group.add_argument(
        "--from-postman",
        type=str,
        help="Get the endpoint details by file path",
        metavar="FILE",
    )
    args = parser.parse_args()
    if args.list or args.get:
        label = args.get if args.get else None
        with open(os.path.join(root_dir, "vandarpy", "endpoints.yaml"), 'r') as f:
            data = yaml.safe_load(f)

        results = []
        for subdomain, versions in data['subdomains'].items():
            for version, endpoints in versions.items():
                for name, endpoint in endpoints.items():
                    if label and not endpoint['label'].startswith(label):
                        continue
                    results.append(
                        (
                            endpoint['label'],
                            f"{name}: {endpoint['method']} {data['scheme']}://{subdomain}.vandar.io/{endpoint['path']}"
                        )
                    )
        results.sort(key=lambda x: x[0])
        for label, endpoint in results:
            print(f"{endpoint}")
    elif args.from_postman:
        logger.info("Generating endpoints from postman file: %s", args.from_postman)
        generate_from_postman(args.from_postman, logger, root_dir)
        logger.info("Endpoints generated successfully")


if __name__ == '__main__':
    main()
