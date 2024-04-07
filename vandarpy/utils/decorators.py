import os.path
import re
import yaml


def endpoint(cls_=None, label: str = None, include_children: bool = False, aliases: dict = None):
    """Decorator for automatically constructing urls from a base_url and defined resources."""

    def wrap(cls):
        return _process_class(cls, label, include_children, aliases)

    if cls_ is None:
        # Decorator is called as @endpoint with parens.
        return wrap
    # Decorator is called as @endpoint without parens.
    return wrap(cls_)


def _process_class(cls, label: str, include_children: bool, aliases: dict = None):
    if label is None:
        raise RuntimeError(
            "A decorated endpoint must define a label as @endpoint(label='Business')."
        )
    if not include_children:
        label_pattern = re.compile(r"^{name}$".format(name=label), re.IGNORECASE)
    else:
        label_pattern = re.compile(r"^{name}.*$".format(name=label), re.IGNORECASE)

    endpoints_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "endpoints.yaml")
    with open(endpoints_path, "r") as file:
        endpoints = yaml.safe_load(file)

    for subdomain, versions in endpoints['subdomains'].items():
        for version, resources in versions.items():
            for resource, data in resources.items():
                if label_pattern.match(data['label']):
                    url = data['full_path']
                    name = resource if aliases is None or resource not in aliases else aliases[resource]
                    setattr(cls, name, url)
    return cls
