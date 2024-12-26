import subprocess
from exceptions import NginxNotInstalled, NginxConfigError

def is_nginx_install() -> None:
    try:
        subprocess.run(["nginx", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        raise NginxNotInstalled("Nginx is not installed. Please install Nginx before running this script.")
    except Exception:
        raise Exception("An error occurred while checking if Nginx is installed. This can be due to a permission error or execution error.")


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

def write_to_nginx_config(server_name: str, app_server_address: str) -> None:
    try:
        subprocess.run(
            ["sudo", "tee", f"/etc/nginx/sites-available/{server_name}"],
            input=simple_template(server_name, app_server_address).encode(),
            check=True
        )
    except subprocess.CalledProcessError:
        raise Exception("An error occurred while writing to the Nginx configuration file. This can be due to a permission error or execution error.")
    except Exception:
        raise Exception("An error occurred while writing to the Nginx configuration file. This can be due to a permission error or execution error.")

def check_nginx_configuration() -> None:
    try:
        subprocess.run(["sudo", "nginx", "-t"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise NginxConfigError("There is an error in the Nginx configuration. Please check the configuration and try again.")
    except Exception:
        raise Exception("An error occurred while checking if Nginx is configured. This can be due to a permission error or execution error.")

def create_symlink(server_name: str) -> None:
    try:
        subprocess.run(["sudo","ln", "-s", f"/etc/nginx/sites-available/{server_name}", f"/etc/nginx/sites-enabled/{server_name}"], check=True)
    except subprocess.CalledProcessError:
        raise Exception("An error occurred while creating a symlink. This can be due to a permission error or execution error.")
    except Exception:
        raise Exception("An error occurred while creating a symlink. This can be due to a permission error or execution error.")

def restart_nginx_using_systemctl() -> None:
    try:
        subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    except subprocess.CalledProcessError:
        raise Exception("An error occurred while restarting Nginx. This can be due to a permission error or execution error.")
    except Exception:
        raise Exception("An error occurred while restarting Nginx. This can be due to a permission error or execution error.")
    
def ssl_using_certbot(server_name: str) -> None:
    try:
        subprocess.run(["sudo", "certbot", "--nginx", "-d", server_name], check=True)
    except subprocess.CalledProcessError:
        raise Exception("An error occurred while setting up SSL using Certbot. This can be due to a permission error or execution error.")
    except Exception:
        raise Exception("An error occurred while setting up SSL using Certbot. This can be due to a permission error or execution error.")