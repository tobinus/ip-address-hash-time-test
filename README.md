# IP Address Hashtable Generation Time Test

See how long time it takes to create a rainbow table for hashed IP
addresses, assuming the same salt is used for each IP address, in a language 
not at all suited for the task.

## Usage

1. Clone the repo.
2. Move into the repo.
3. Create a virtual environment.
4. Enter the virtual environment.
5. Install the required packages (using requirements.txt)
6. Run `python test_hash.py --help` for usage instructions for
   the script.

A progress bar will pop up and estimate how much time is left.
Use that estimation to your advantage, and cancel the program when
you've noted it down (there is no point to wait it out).
Once the program is done running, you can see how many IP addresses
were hashed, and how long it took to hash them.

## Is this a hacking program?

Even though one hash is generated per IP address, it is not
saved anywhere, and even if it was, this solution would be
highly inefficient. Salt and multithreading is not supported.
It is therefore of no use to a hacker.

This software is not meant to be used to create rainbow tables
of IP addresses. It is just meant to be an eye-opener to anyone who
wants to anomynize the IP addresses of visitors (which the
Norwegian law requires, for instance). See the example below.

Any use of this program for malicious purposes is neither supported nor approved
by the author.

## What does the result tell me?

This implementation is done in Python3, which has 3 big impacts
on the result: 

1. Python3 is interpreted and therefore slower than
   Java and C++
2. It will not use machine acceleration (GPU cards can
   be especially useful in speeding up some hash algorithms).
3. It is single-threaded. 

All those factors make the program slower
than what a hacker can achieve with more efficient solutions.

What this means, is that you can draw the following conclusions
depending on how long it took:

<dl>
<dt>It took too little time</dt>
<dd>A faster solution will take even less time, so you know
for a fact that the IP addresses aren't anonymized well enough.</dd>
<dt>It took enough or more than enough time</dt>
<dd>You <i>cannot</i> conclude that it is slow enough.
For all you know, the hacker may have solutions that are
ten times, if not a hundred times faster.</dd>
</dl>

## Example

The university I attend, NTNU, has an IPv4 range of
`129.241.0.0/16`. This means that the first 16 bits are part of the prefix,
while the (32-16=16) rightmost bits are the ones that change.

Say you're creating a service for users who are likely to be at NTNU
(and therefore having an IP address from NTNU), and you want to anonymize the
IP addresses. Browsing the net, you discover [mod_anonstats](http://bug.st/mod_anonstats),
an Apache module for hashing the IP addresses. Inspecting the source, you see that it uses
MD5, so we can see how fast a rainbow table can be created by running:

```sh
(venv)$ python test_hash.py --hash md5 16
[################################] 65536/65536 - 00:00:00
```

As you can see, less than one second was spent to create the hashes (assuming the
same salt is used for them all). What this means, is that with the drawn solution,
you would be able to obtain the IP address of anyone with an IP address from NTNU.
Thus, it is a bad solution for the situation described, since the IP addresses are
not anonymous at all.

What about IPv6? If we assume everyone's on the same subnet, there are 64 bits that
change between different IP addresses on that subnet. Creating a rainbow table would
then take:

```sh
(venv)$ python test_hash.py --hash md5 64
[################################] 10316722/18446744073709551616 - 00:00:19
...
KeyboardInterrupt
```

Here, I terminated the process after 19 seconds (using CTRL-C), and it hardly
got to hash anything at all. Thus, we can conclude that we do not know anything.

As like everything in security, you need to make it so that the cost
outweights the benefit for the attacker, so you'll need to figure out how an IP
address might be of benefit for him or her, and how far he or she is willing to go
to recover it. Consult Google for some estimates on how many hashes can be done on
a high-end set up instead of using this software :P

## Why create this?

I was curious whether MD5 was good enough, and didn't bother finding a good query
for Google. That's all.
