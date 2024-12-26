import argparse
from .utils import *


def deploy(server_name, app_server_address):
    print(f"Deploying to server '{server_name}' at address '{app_server_address}'")

def main():
    parser = argparse.ArgumentParser(
        description="Dockership CLI for managing deployments."
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        required=True,
        help="Available commands",
    )

    # Deploy command parser
    deploy_parser = subparsers.add_parser(
        "deploy", help="Deploy an application to a server"
    )

    deploy_parser.add_argument(
        "--server_name",
        required=True,
        help="The name of the server where the application will be deployed",
    )

    deploy_parser.add_argument(
        "--app_server_address",
        required=True,
        help="The address of the application server",
    )

    args = parser.parse_args()

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

if __name__ == "__main__":
    main()
