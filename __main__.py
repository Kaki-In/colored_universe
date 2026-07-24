#!/usr/bin/python3

from colors_control.objects import ColoredDevicesManager
from colors_control.configuration import MainConfiguration

import sys
import argparse
import pathlib
import subprocess
import threading
import time 

DEFAULT_CONF_DIR = str(pathlib.Path.home() / ".colored_universe")

def main(args: list[str]):
    parser = argparse.ArgumentParser(description="Colored Universe CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    run_parser = subparsers.add_parser("run", aliases=['r'], help="runs the server")
    run_parser.add_argument("--background", '-b', default=False, action="store_true", required=False, help="launch and run silently in background")
    run_parser.add_argument("--force", '-f', default=False, action="store_true", required=False, help="forces launches, even if the service is supposed to be running")
    
    subparsers.add_parser("stop", aliases=['s'], help="stops the server")
    subparsers.add_parser("status", aliases=['st'], help="returns the status of the server")
    subparsers.add_parser("error", aliases='e', help="returns the error if applicable")
    
    parser.add_argument("--conf-directory", '-d', default=DEFAULT_CONF_DIR, required=False, help=f"the configuration directory (defaults to {DEFAULT_CONF_DIR})")
    
    parsed_args = parser.parse_args(args[1:])
    
    configuration = MainConfiguration(parsed_args.conf_directory)
    match(parsed_args.command):
        case 'run':
            if not parsed_args.force:
                
                if configuration.status_control.get_content()['is_running']:
                   print("The service is already running. If you're sure that it is not, please use the -f flag.")
                   return 400
            
            if parsed_args.background:
                subprocess.Popen(["python", sys.argv[0], '-d', parsed_args.conf_directory, 'run'] + (['-f'] if parsed_args.force else []), start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            else:
                manager = ColoredDevicesManager(configuration)
                
                return manager.main()
                
        case 'stop':
            configuration.status_control.requires_for_stop = True
            
            try:
                while configuration.status_control.requires_for_stop:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                configuration.status_control.requires_for_stop = False
                
            return 0
    
        case 'status':
            data = configuration.status_control.get_content()
            
            print("running" if data['is_running'] else ("error" if data['stopped_error'] else "stopped"))
        
        case 'error':
            data = configuration.status_control.get_content()
            
            if data['stopped_error'] is not None:
                print(data['stopped_error'])
        
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

