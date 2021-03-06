#!/usr/bin/python

import argparse
import socket
import threading


def connection_scan(target_ip, target_port):
    try:
        conn_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_socket.connect((target_ip, target_port))
        conn_socket.send(b"banner_query\r\n")
        results = conn_socket.recv(100)
        print("[.] {}/tcp open".format(target_port))
        print("[.] {}".format(str(results)))
    except OSError:
        print("[!] {}/tcp closed".format(target_port))
    finally:
        conn_socket.close()


def port_scan(target, port_num):
    try:
        target_ip = socket.gethostbyname(target)
    except OSError:
        print("[!] cannot resolve {}, unknown host".format(target))
        return

    try:
        target_name = socket.gethostbyaddr(target_ip)
        print("[.] scan results for {}".format(target_name[0]))
    except OSError:
        print("[.] scan results for {}".format(target_ip))

    t = threading.Thread(target=connection_scan, args=(target, int(port_num)))
    t.start()


def argument_parser():
    parser = argparse.ArgumentParser(description="TCP port scanner")
    parser.add_argument("-o", "--host", nargs="?", help="host ip address")
    parser.add_argument("-p", "--ports", nargs="?", help="comma seperated port list")

    var_args = vars(parser.parse_args())
    return var_args


if __name__ == "__main__":
    try:
        user_args = argument_parser()
        host = user_args["host"]
        port_list = user_args["ports"].split(",")
        for port in port_list:
            port_scan(host, port)
    except AttributeError:
        print("Error, provide cmd line args")
