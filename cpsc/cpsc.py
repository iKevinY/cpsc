# -*- coding: utf-8 -*-

import glob
import math
import difflib
from subprocess import PIPE, Popen
from collections import defaultdict

try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

import click


def print_diff(seqm):
    """Based on http://stackoverflow.com/a/788780"""
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            click.echo(seqm.a[a0:a1], nl=False)
        elif opcode == 'insert':
            click.secho(seqm.b[b0:b1], fg='green', nl=False, bold=True)
        elif opcode == 'delete':
            click.secho(seqm.a[a0:a1], fg='red', nl=False, bold=True)
        elif opcode == 'replace':
            click.secho(seqm.a[a0:a1], fg='red', nl=False, bold=True)
            click.secho(seqm.b[b0:b1], fg='green', nl=False, bold=True)

    click.echo()


@click.command(name='cpsc')
@click.argument('program', type=click.Path(exists=True))
@click.argument('test_prefix')
def main(program, test_prefix):
    """Competitive Programming Sanity Checker"""
    tests = defaultdict(list)

    for filename in glob.glob(test_prefix + '*'):
        tests[filename.split('.')[0]].append(filename)

    for filenames in tests.values():
        if len(filenames) == 2:
            in_f, out_f = sorted(filenames)
            click.secho("{} / {}".format(in_f, out_f), bold=True)

            # TODO: Determine interpreter to call (or just run binary)
            cmd = ('python', program, in_f)

            with open(in_f) as inp:
                proc = Popen(cmd, stdin=PIPE, stdout=PIPE)
                stdout = proc.communicate(input=inp.read().encode())[0]

            # Convert bytes to string if on Python 3
            stdout = stdout.decode().split('\n')

            with open(out_f) as out:
                expected = out.read().split('\n')

            # Add line numbers to output
            lines = max(len(stdout), len(expected))
            padding = int(math.log10(lines)) + 1

            for line_no, (a, b) in enumerate(zip_longest(stdout, expected, fillvalue=''), start=1):
                # Skip double-newlines
                if not a and not b:
                    continue

                click.secho("{: >{pad}} | ".format(line_no, pad=padding), nl=False, bold=True)
                sm = difflib.SequenceMatcher(None, a, b)
                print_diff(sm)
