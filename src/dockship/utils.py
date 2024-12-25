import subprocess
from exceptions import NginxNotInstalled, NginxConfigError

def simple_template(server_name: str, app_server_address: str) -> str:
    return """
server {
    listen 80;
    listen [::]:80;

    server_name %s;
        
    location / {
        proxy_pass %s;
        include proxy_params;
    }
}  
""" % (server_name, app_server_address)

def is_nginx_install() -> None:
    try:
        subprocess.run(["nginx", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise NginxNotInstalled("Nginx is not installed. Please install Nginx before running this script.")
    except Exception:
        raise Exception("An error occurred while checking if Nginx is installed. This can be due to a permission error or execution error.")

def check_nginx_configured() -> None:
    try:
        subprocess.run(["nginx", "-t"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise NginxConfigError("There is an error in the Nginx configuration. Please check the configuration and try again.")
    except Exception:
        raise Exception("An error occurred while checking if Nginx is configured. This can be due to a permission error or execution error.")