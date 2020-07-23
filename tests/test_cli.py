import os
import json
import shutil

from pathlib import Path
from cli.main import *

from unittest import TestCase


class TestCLI(TestCase):

    config_data = {
        'pattern': [
            {
                'start': 0,
                'end': 1,
                'precision': 10,
            },
            {
                'start': 0,
                'end': 2,
                'precision': 10,
            },
            {
                'start': 0,
                'end': 3,
                'precision': 10,
            },
        ],
        'size': 5,
        'crossoverRate': 0.75,
        'mutationRate': 0.06,
        'elitism': 1,
        'maxGen': 100,
    }

    ga_data = {
        'population': [
            {
                "parameters": [0.0, 0.0, 0.0],
                "fitness": 1.0,
                "alive": True,
            },
            {
                "parameters": [0.0, 1.0, 2.0],
                "fitness": 1.0,
                "alive": True,
            },
            {
                "parameters": [0.5, 0.5, 1.5],
                "fitness": 1.0,
                "alive": True,
            },
            {
                "parameters": [0.1, 1.1, 2.1],
                "fitness": 1.0,
                "alive": True,
            },
            {
                "parameters": [0.2, 1.2, 2.2],
                "fitness": 1.0,
                "alive": True,
            }
        ],
        'offsprings': [],
        'generation': 0,
        'satisfied': False,
    }

    def setUp(self) -> None:
        self.cwd = Path(os.getcwd())
        if self.cwd == Path(os.path.dirname(__file__)):
            self.cwd = self.cwd.joinpath('..')

    def get_path(self, path):
        return self.cwd.joinpath(path)

    def test_load_config(self):
        self.assertDictEqual(load_config(self.get_path('examples/config_example.yml')), self.config_data)

    def test_load_input_file(self):
        self.assertDictEqual(load_input_file(self.get_path('examples/input_example.json')), self.ga_data)

    def test_load_input_file_from_dir(self):
        path = self.get_path('test_input/')
        path.mkdir()
        for i in range(10):
            path.joinpath(f'{i:03}.json').touch()
        with open(path.joinpath(f'010.json'), 'w') as file:
            json.dump(self.ga_data, file)
        self.assertDictEqual(load_input_file(path), self.ga_data)
        shutil.rmtree(path)

    def test_dump_output(self):
        path = self.get_path('test_output.json')
        dump_output(path, self.ga_data)
        self.assertTrue(path.is_file())
        self.assertDictEqual(load_input_file(path), self.ga_data)
        os.remove(path)

    def test_dump_output_to_dir(self):
        path = self.get_path('test_input/')
        path.mkdir()
        dump_output(path, self.ga_data)
        self.assertTrue(path.joinpath('000.json').exists())
        self.assertDictEqual(load_input_file(path.joinpath('000.json')), self.ga_data)
        shutil.rmtree(path)
