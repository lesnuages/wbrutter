#coding : utf-8

import sys
import requests
import argparse
import concurrent.futures

def parse_args(cli_args):
    parser = argparse.ArgumentParser(description='Web Application brutter.')
    parser.add_argument('target', type=str, metavar='target', help='Target IP address or hostname.')
    parser.add_argument('dict', metavar='dict', type=str, help='Dictionnary file. One url per line.')
    return parser.parse_args()

def parse_dict(dict_filename):
    data = None
    with open(dict_filename, 'r') as dict_file:
        data = dict_file.read()
    urls = [url for url in data.split('\n') if url != '']
    return urls

def scan_url(full_url):
    resp = requests.get(full_url)
    return resp.status_code

def scan_all(host,urls):
    urls = ['http://%s/%s/' % (host,url) for url in urls]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(scan_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                resp_code = future.result()
            except Exception as exc:
                print('%s url generated an exception : %s' % (url, exc))
            else:
                if resp_code != 404:
                    print('%s \t\t [%d] ' % (url, resp_code))

if __name__ == '__main__':
    args = parse_args(sys.argv)
    urls = parse_dict(args.dict)
    scan_all(args.target, urls)
