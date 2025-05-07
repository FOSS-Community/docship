import argparse

from . import __version__
from .utils import (
    check_nginx_configuration,
    create_symlink,
    is_nginx_install,
    restart_nginx_using_systemctl,
    ssl_using_certbot,
    write_to_nginx_config,
)


def deploy(server_name, app_server_address):
    print(f"Deploying to server '{server_name}' at address '{app_server_address}'")


def main():
    parser = argparse.ArgumentParser(
        description="Dockership CLI for managing deployments."
    )

    parser.add_argument(
        "--version",
        "-v",
        help="to get the current version of dockship",
        action="store_true",
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        help="Available commands",
    )

    # Deploy command parser
    deploy_parser = subparsers.add_parser(
        "deploy", help="Deploy an application to a server"
    )

    deploy_parser.add_argument(
        "--name",
        "-n",
        required=True,
        help="The name of the server where the application will be deployed, ex. api.example.com",
    )

    deploy_parser.add_argument(
        "--address",
        "-a",
        required=True,
        help="The address of the application server, ex. http://localhost:8000",
    )

    args = parser.parse_args()

    if args.version:
        print(f"dockship: {__version__}")
        return

    if args.command == "deploy":
        print("Deploying...")
        print("Checking if Nginx is installed...")
        is_nginx_install()
        print("Writing to Nginx configuration...")
        write_to_nginx_config(args.server_name, args.app_server_address)
        print("Checking Nginx configuration...")
        check_nginx_configuration()
        print("Creating symlink...")
        create_symlink(args.server_name)
        print("Restarting Nginx...")
        restart_nginx_using_systemctl()
        print("Generating SSL certificate using Certbot...")
        ssl_using_certbot(args.server_name)
        print("SSL certificate generated successfully!")
        print("Deployment successful!")
        return


if __name__ == "__main__":
    main()
