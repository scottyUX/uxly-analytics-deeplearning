import json
import os

from  utils.custom_keys import CustomKeys as ck


class PathProvider(object):
    
    def __init__(self, paths_json_path: str, path_prefix = ''):
        self.__path_prefix = path_prefix
        self.__sep = os.path.sep
        self.__paths = self.__read_paths(paths_json_path)
        if self.__path_prefix != '':
            for key in self.__paths:
                self.__paths[key] = self.__sep.join(
                    [self.__path_prefix, self.__paths[key]],
                ).replace('/', self.__sep)

    def __read_paths(self, paths_json_path: str):
        if self.__path_prefix != '':
            paths_json_path = self.__sep.join(
                [self.__path_prefix, paths_json_path],
            )
        with open(paths_json_path, 'r') as file:
            self.__paths = json.loads(file.read())
        return self.__paths
    
    def __getitem__(self, key: str):
        if key not in self.__paths:
            raise Exception(f'Path {key} not found in paths.')
        return self.__paths[key]
    
    def get_api_keys_path(self):
        return self[ck.API_KEYS_PATH]
    
    def get_aws_access_key_path(self):
        return self[ck.AWS_ACCESS_KEYS_PATH]

    def get_claimers_path(self):
        return self[ck.CLAIMERS_PATH]

    def get_table_file_path(self):
        return self[ck.TABLES_FILE_PATH]
    
    def get_airdrop_table_path(self):
        return self[ck.AIRDROPS_DATABASE_PATH]
    
    def get_graph_html_path(self, graph_name: str):
        return self.__sep.join([
            self[ck.GRAPH_HTMLS_FOLDER_PATH].replace('/', self.__sep), 
            graph_name + '.html',
        ])