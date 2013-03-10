# Bitrade

A <strike>highly-concurrent, fault-tolerant, malicious-user-proof,</strike> Python-based bitcoin trading server.

Eat this, Mt.Gox - now how you gonna act?

## Usage

Easiest way, run all processes using [foreman](https://github.com/ddollar/foreman):

```bash
$ foreman start -f Procfile.dev
```

or the Python-equivalent [honcho](https://github.com/nickstenning/honcho):

```bash
$ honcho start -f Procfile.dev
```

Test client available on [http://127.0.0.1:9000](http://127.0.0.1:9000).

## Automated Test Simulation

WIP :)
