# -*- coding: utf-8 -*-

import click


@click.command(name='cpsc')
@click.argument('program', type=click.Path(exists=True))
@click.argument('test', type=click.Path(exists=True), nargs=-1)
def main(program, test):
    """Competitive Programming Sanity Checker"""
    click.echo("Program: {}".format(program))
    click.echo("Tests: {}".format(test))
