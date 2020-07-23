import yaml
import json
import os
import click

from typing import Optional
from ga.algorithms import GAPassive


def load_config(path) -> Optional[dict]:
    if os.path.isfile(path):
        with open(path) as file:
            return yaml.safe_load(file)
    return None


def load_input_file(path) -> Optional[dict]:
    if os.path.isfile(path):
        with open(path) as file:
            return json.load(file)
    elif os.path.isdir(path) and os.path.exists(path):
        files = sorted([os.path.join(path, f) for f in os.listdir(path)])
        files = [f for f in files if os.path.isfile(f)]
        if len(files) <= 0:
            return None
        with open(files[-1]) as file:
            return json.load(file)
    return None


def dump_output(path, obj: dict) -> Optional[str]:
    if os.path.isdir(path) and os.path.exists(path):
        filename = os.path.join(path, '%03d.json' % obj.get('generation'))
        with open(filename, 'w') as file:
            json.dump(obj, file, indent=2)
        return filename
    elif os.path.exists(os.path.dirname(os.path.abspath(path))):
        with open(path, 'w') as file:
            json.dump(obj, file, indent=2)
        return path
    return None


def evolve(config_data: dict, input_data: Optional[dict] = None) -> dict:
    if input_data is None:
        ga = GAPassive.from_dict(config_data)
        click.echo('No input data, initial population generated.')
    else:
        ga = GAPassive.from_dict(config_data, input_data)
        click.echo('Input data accepted.')
        click.echo(f'Current generation: {ga.generation}')
        click.echo('Evolving...')
        ga.evolve()
        click.echo(f'Number of offsprings generated: {len(ga.offsprings)}')
    return ga.serialize()
