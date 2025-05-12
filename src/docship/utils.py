import subprocess  # pylint: disable=C0114

from .exceptions import DockshipException, NginxConfigError, NginxNotInstalled


def is_nginx_install() -> None:  # pylint: disable=C0116
    try:
        subprocess.run(
            ["nginx", "-v"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except FileNotFoundError as exc:
        raise NginxNotInstalled(
            "Nginx is not installed. Please install Nginx before running this script."
        ) from exc
    except Exception as exc:
        raise DockshipException(
            "An error occurred while checking if Nginx is installed. \
            This can be due to a permission error or execution error."
        ) from exc


def simple_template(  # pylint: disable=C0116
    server_name: str, app_server_address: str
) -> str:
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
""" % (
        server_name,
        app_server_address,
    )


def write_to_nginx_config(  # pylint: disable=C0116
    server_name: str, app_server_address: str
) -> None:
    try:
        subprocess.run(
            ["sudo", "tee", f"/etc/nginx/sites-available/{server_name}"],
            input=simple_template(server_name, app_server_address).encode(),
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise DockshipException(
            "An error occurred while writing to the Nginx configuration file.\
                This can be due to a permission error or execution error."
        ) from exc
    except Exception as exc:
        raise DockshipException(
            "An error occurred while writing to the Nginx configuration file.\
                  This can be due to a permission error or execution error."
        ) from exc


def check_nginx_configuration() -> None:  # pylint: disable=C0116
    try:
        subprocess.run(
            ["sudo", "nginx", "-t"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise NginxConfigError(
            "There is an error in the Nginx configuration. \
                Please check the configuration and try again."
        ) from exc
    except Exception as exc:
        raise DockshipException(
            "An error occurred while checking if Nginx is configured. \
                This can be due to a permission error or execution error."
        ) from exc


def create_symlink(server_name: str) -> None:  # pylint: disable=C0116
    try:
        subprocess.run(
            [
                "sudo",
                "ln",
                "-s",
                f"/etc/nginx/sites-available/{server_name}",
                f"/etc/nginx/sites-enabled/{server_name}",
            ],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise DockshipException(
            "An error occurred while creating a symlink.\
                This can be due to a permission error or execution error."
        ) from exc
    except Exception as exc:
        raise DockshipException(
            "An error occurred while creating a symlink.\
                This can be due to a permission error or execution error."
        ) from exc


def restart_nginx_using_systemctl() -> None:  # pylint: disable=C0116
    try:
        subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    except subprocess.CalledProcessError as exc:
        raise DockshipException(
            "An error occurred while restarting Nginx.\
                This can be due to a permission error or execution error."
        ) from exc
    except Exception as exc:
        raise DockshipException(
            "An error occurred while restarting Nginx.\
                This can be due to a permission error or execution error."
        ) from exc


def ssl_using_certbot(server_name: str) -> None:  # pylint: disable=C0116
    try:
        subprocess.run(["sudo", "certbot", "--nginx", "-d", server_name], check=True)
    except subprocess.CalledProcessError as exc:
        raise DockshipException(
            "An error occurred while setting up SSL using Certbot. \
                This can be due to a permission error or execution error."
        ) from exc
    except Exception as exc:
        raise DockshipException(
            "An error occurred while setting up SSL using Certbot. \
                This can be due to a permission error or execution error."
        ) from exc
