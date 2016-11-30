import hashlib
import sys
import threading
import argparse
import math

# Following is a pip package requirement
from clint.textui import progress

# Global variables (yay)
# Progress bar, instance of progress.Bar
bar = None
# The currently active threading.Timer instance
t = None
# The current IP address that is tested
i = 0
# Interval in seconds between each time the progress bar is updated
bar_interval = 0.0

def get_hash_function(name):
    """Given a string, return the hashlib function with that name."""
    return getattr(hashlib, name)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Hash a set of IP addresses,"
        " to test how long it takes.")
    parser.add_argument('--hash',
        choices=hashlib.algorithms_guaranteed,
        default="md5",
        help="The hash function to use. Defaults to md5.")
    parser.add_argument('--interval', '-i', type=float, default=1.0,
        help="Number of seconds to wait between each time the "
        "progress bar is updated.")
    parser.add_argument('bits', help="Number of bits to test. Defaults to "
        "32 (IPv4). Use this to test cases in which you might guess "
        "the subnet, or to test IPv6 (128 bits).", type=int, default=32,
        nargs="?")

    args = parser.parse_args()
    return parser, args

def print_progress():
    global t
    bar.show(i)
    t = threading.Timer(bar_interval, print_progress)
    t.start()

def main():
    global bar_interval
    global bar
    global i

    # Parse the user's arguments
    parser, args = parse_arguments()

    # Map the user's arguments to variables
    hash_function = args.hash
    num_bits = args.bits
    bar_interval = args.interval

    # Convert hash_function so it points to the function
    hash_function = get_hash_function(hash_function)

    upper_limit = 2**num_bits

    # Initialize the progress bar
    bar = progress.Bar(expected_size=upper_limit)
    try:
        # Start printing the progress bar (it will continue to update
        # at a fixed interval
        print_progress()

        # Actually generate the hashes.
        # We cannot use "for i in range(upper_limit)" since the
        # upper limit is above what range can handle (due to
        # memory consumption). Or maybe that was Python2?
        i = 0
        byteorder = sys.byteorder
        num_bytes = math.ceil(num_bits / 8)

        while i < upper_limit:
            # We don't store the hash anywhere, since that's not what we're testing
            hash_function(i.to_bytes(num_bytes, byteorder=byteorder)).hexdigest()
            i += 1

    finally:
        # Cancel the timer that's currently active
        t.cancel()

        # Ensure the progress bar has the correct value
        bar.show(i)
        # Print the final progress bar (shows as full, shows elapsed time)
        bar.done()

if __name__ == "__main__":
    main()
