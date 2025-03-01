import docker
import yaml
import argparse
import logging
import os
from colorama import Fore, Style
"""This file is used as a logging file that stores all the log data"""
# --- Logging Setup ---
logging.basicConfig(
    filename="docker_deploy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def display_banner():
        banner=f"""
________                 __      _________.__    .__
\______ \   ____   ____ |  | __ /   _____/|  |__ |__|_____
 |    |  \ /  _ \_/ ___\|  |/ / \_____  \ |  |  \|  \____ \
 |    `   (  <_> )  \___|    <  /        \|   Y  \  |  |_> >
/_______  /\____/ \___  >__|_ \/_______  /|___|  /__|   __/
        \/            \/     \/        \/      \/   |__|
        {Fore.GREEN}DockShip{Style.RESET_ALL} - A CLI Tool for Deploying and Managing Docker Containers and Services
                Version 1.0
                By: {Fore.RED}Aarav Saklani{Style.RESET_ALL}"""
        print(banner)
        print(f"Usage:{Fore.RED}Deploy a service command{Style.RESET_ALL} {Fore.GREEN} deploy [service_name] -c[config]{Style.RESET_ALL}")
        print(f"Usage:{Fore.RED} List Command{Style.RESET_ALL} {Fore.GREEN}-l[list] {Style.RESET_ALL}")
        print(f"Usage:{Fore.RED}Stop Command{Style.RESET_ALL} {Fore.GREEN}-s[stop] [service_name_or_id]{Style.RESET_ALL}")
        print(f"Usage:{Fore.RED}Remove Command{Style.RESET_ALL} {Fore.GREEN}-r [service_name_or_id] {Style.RESET_ALL}")
        print(f"Usage:{Fore.RED}See Status Command {Style.RESET_ALL} {Fore.GREEN}-st [service_name_or_id]{Style.RESET_ALL}")
        print(f"Usage:{Fore.RED} Pull Image Command {Style.RESET_ALL} {Fore.GREEN}-i [service_name_or_id]{Style.RESET_ALL}")
        print("-" * 50)

def deploy_service(service_name, config_file="config.yaml"):
    """Deploys a Docker service."""
    try:
        client = docker.from_env()

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file '{config_file}' not found.")

        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        service_config = config["services"].get(service_name)
        if not service_config:
            raise ValueError(f"Service '{service_name}' not found in config.")

        image_name = service_config["image"]
        try:
            client.images.get(image_name)  # Check if image exists locally
            logging.info(f"Image '{image_name}' found locally.")
        except docker.errors.APIError as e:
            logging.info(f"Pulling image '{image_name}'...")
            try:
                client.images.pull(image_name)
            except docker.errors.APIError as e:
                logging.error(f"Error pulling image '{image_name}': {e}")
                return False  # Indicate failure

        container_config = {
            "image": image_name,
            "detach": True,  # Run in detached mode
        }

        # Add ports, volumes, environment, networks if present
        for key in ["ports", "volumes", "environment", "networks"]:
            if service_config.get(key):
                container_config[key] = service_config[key]

        try:
            container = client.containers.run(**container_config)
            logging.info(
                f"Service '{service_name}' deployed (container ID: {container.id})"
            )
            return True  # Indicate success
        except docker.errors.APIError as e:
            logging.error(f"Error deploying service '{service_name}': {e}")
            return False  # Indicate failure

    except FileNotFoundError as e:
        logging.error(e)
        return False
    except ValueError as e:
        logging.error(e)
        return False
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML config: {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False


def list_services():
    """Lists deployed Docker services."""
    try:
        client = docker.from_env()
        containers = client.containers.list()
        if containers:
            print("Deployed Services:")
            for container in containers:
                print(
                    f"- {container.name} (ID: {container.id}, Status: {container.status})"
                )
        else:
            print("No services are currently deployed.")
        return True
    except Exception as e:
        logging.error(f"Error listing services: {e}")
        return False


def stop_service(service_name_or_id):
    """Stops a Docker service."""
    try:
        client = docker.from_env()
        try:  # Finding the container by both the name and ID
            container = client.containers.get(service_name_or_id)
        except docker.errors.NotFound:
                raise ValueError(f"Service '{service_name_or_id}' not found.")

        container.stop()
        print(f"Service '{service_name_or_id}' stopped.")
        return True
    except ValueError as e:
        logging.error(e)
        return False
    except Exception as e:
        logging.error(f"Error stopping service: {e}")
        return False


def remove_service(service_name_or_id):
    """Removes a Docker service."""
    try:
        client = docker.from_env()
        try:  #Finding the container by both name and ID.
            container = client.containers.get(service_name_or_id)
        except docker.errors.NotFound:
                raise ValueError(f"Service '{service_name_or_id}' not found.")

        container.remove()
        print(f"Service '{service_name_or_id}' removed.")
        return True
    except ValueError as e:
        logging.error(e)
        return False
    except Exception as e:
        logging.error(f"Error removing service: {e}")
        return False


def get_service_status(service_name_or_id):
    """Gets the status of a Docker service."""
    try:
        client = docker.from_env()
        try:  # Finding the container by both name and ID.
            container = client.containers.get(service_name_or_id)
        except docker.errors.NotFound:
                raise ValueError(f"Service '{service_name_or_id}' not found.")

        print(f"Service '{service_name_or_id}' status: {container.status}")
        return True
    except ValueError as e:
        logging.error(e)
        return False
    except Exception as e:
        logging.error(f"Error getting service status: {e}")
        return False


def pull_image(image_name):
    """Pulls a Docker image."""
    try:
        client = docker.from_env()
        print(f"Pulling image '{image_name}'...")
        client.images.pull(image_name)
        print(f"Image '{image_name}' pulled successfully.")
        return True
    except docker.errors.APIError as e:
        logging.error(f"Error pulling image '{image_name}': {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False


def main():
    display_banner()
    parser = argparse.ArgumentParser(description="Docker Deployment CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy a service")
    deploy_parser.add_argument("service_name", help="Name of the service to deploy")
    deploy_parser.add_argument(
        "-c", "--config", default="config.yaml", help="Path to the configuration file"
    )

    # List command
    subparsers.add_parser("-l", help="List deployed services")

    # Stop command
    stop_parser = subparsers.add_parser("-s", help="Stop a service")
    stop_parser.add_argument(
        "-sid", dest="service_name_or_id",required=True, help="Name or ID of the service to stop"
    )

    # Remove command
    remove_parser = subparsers.add_parser("-r", help="Remove a service")
    remove_parser.add_argument(
        "-sid", dest="service_name_or_id",required=True, help="Name or ID of the service to remove"
    )

    # Status command
    status_parser = subparsers.add_parser("-st", help="Get the status of a service")
    status_parser.add_argument(
        "-sid",dest="service_name_or_id",required=True, help="Name or ID of the service"
    )

    # Image command
    image_parser = subparsers.add_parser("-i", help="Pull a docker image")
    image_parser.add_argument("-img", dest="image_name",required=True, help="Name of the image")

    args = parser.parse_args()

    if args.command == "deploy":
        if deploy_service(args.service_name, args.config):
            exit(0)  # Success
        else:
            exit(1)  # Failure
    elif args.command == "list":
        if list_services():
            exit(0)
        else:
            exit(1)
    elif args.command == "stop":
        if stop_service(args.service_name_or_id):
            exit(0)
        else:
            exit(1)
    elif args.command == "remove":
        if remove_service(args.service_name_or_id):
            exit(0)
        else:
            exit(1)
    elif args.command == "status":
        if get_service_status(args.service_name_or_id):
            exit(0)
        else:
            exit(1)
    elif args.command == "pull image":
        if pull_image(args.image_name):
            exit(0)
        else:
            exit(1)

if __name__=="__main__":
        main()
