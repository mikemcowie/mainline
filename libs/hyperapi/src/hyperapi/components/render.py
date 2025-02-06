from hyperapi.components.base import Component


def render(component: Component):
    """Recursively build a component via
    all its children"""
    rendered = component.build()
    with rendered:
        for child in component.children:
            render(child)
    return rendered
