import re


def endpoint(cls_=None, base_class=None, base_url=None):
    """Decorator for automatically constructing urls from a base_url and defined resources."""

    def wrap(cls):
        return _process_class(cls, base_class, base_url)

    if cls_ is None:
        # Decorator is called as @endpoint with parens.
        return wrap
    # Decorator is called as @endpoint without parens.
    return wrap(cls_)


def _process_class(cls, base_class, base_url):
    if base_url is None:
        raise RuntimeError(
            "A decorated endpoint must define a base_url as @endpoint(base_url='http://foo.com')."
        )
    else:
        base_url = base_url.rstrip("/")

    if base_class is not None:
        # remove the base url from the base class.
        pattern = r"(?:https://|http://)?[^/]*(.*)"
        regex = re.compile(pattern)
        for name, value in base_class.__dict__.items():
            if name.startswith("_"):
                # Ignore any private or class attributes.
                continue
            setattr(cls, name, ''.join(regex.match(value).groups()))

    for name, value in cls.__dict__.items():
        if name.startswith("_"):
            # Ignore any private or class attributes.
            continue
        new_value = str(value).lstrip("/")
        resource = f"{base_url}/{new_value}"
        setattr(cls, name, resource)
    return cls