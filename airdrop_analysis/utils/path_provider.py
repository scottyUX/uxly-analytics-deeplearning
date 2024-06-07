import json
import os

from  utils.custom_keys import CustomKeys as ck


class PathProvider(object):
    
    def __init__(self, paths_json_path: str, path_prefix = ''):
        self.__path_prefix = path_prefix
        self.__sep = os.path.sep
        self.__paths = self.__read_paths(paths_json_path)

    def __read_paths(self, paths_json_path: str):
        json_path = self.__sep.join([self.__path_prefix, paths_json_path])
        with open(json_path, 'r') as file:
            self.__paths = json.loads(file.read())
        return self.__paths
    
    def __getitem__(self, key: str):
        if key not in self.__paths:
            raise Exception(f'Path {key} not found in paths.')
        return self.__paths[key]
    
    def get_api_keys_path(self):
        return self.__sep.join([self.__path_prefix, self[ck.API_KEYS_PATH]])