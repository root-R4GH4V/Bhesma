import argparse
import concurrent.futures
import os
import subprocess

# color codes
RED = '\033[91m'
GREEN = '\033[92m'
ENDC = '\033[0m'

def run_command(url):
    if not url.strip():
        return
    command = f"curl -s {url} | grep -oh '\"\\/[^\"<>]*\"' | sed -e 's/^\"//' -e 's/\"$//' | sort -u"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(f"Error occurred for {url}: {error}")
    else:
        endpoints = output.decode("utf-8").split("\n")
        endpoints = list(filter(lambda e: e not in ["/", "//"], endpoints))
        print(f"\nURLs for {RED}{url.strip()}{ENDC}:")
        for endpoint in endpoints:
            if endpoint:
                print(f"{GREEN}{endpoint}{ENDC}")
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="Input file containing URLs", required=True)
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use", default=20)
    args = parser.parse_args()

    with open(args.file) as f:
        urls = f.readlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(run_command, url.strip()))
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error occurred: {e}")
