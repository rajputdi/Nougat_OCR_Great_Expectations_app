import base64
import json


def convert_config_to_html(config):
    """
    Convert the expectations configuration to a prettified HTML string.
    """
    formatted_json = json.dumps(config, indent=4)
    html_content = f"<pre>{formatted_json}</pre>"
    return html_content


def generate_download_link(content, filename="data.html", text="Download"):
    """
    Generate a link to download the given content.
    """
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64,{b64}" download="{filename}">{text}</a>'
    return href
