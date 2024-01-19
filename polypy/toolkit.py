import yaml
from datetime import datetime
import exceptions.exceptions as AuthEx


def validate_parameters_exist(*params) -> bool: 
    '''Returns a boolean denoting status of conditional check and the parameter at fault given a False return value'''
    if params == None:
        return False
    else:
        for arg in params:
            if arg == None:
                return False 
            else:
                continue
    return True
    

def validate_parameters_type(exp_type: type, *params ) -> bool:
    '''Returns a boolean denoting status of conditional check and the parameter at fault given a False return value'''

    if params == None:
        return False
    else:
        for arg in params:
            if arg == None:
                pass
            elif type(arg) == exp_type:
                continue
            else:
                return False
    return True


def unix_to_date(unix_timestamp: int) -> str:
    try:
        if validate_parameters_exist(unix_timestamp) == True:
            if validate_parameters_type(int, unix_timestamp) == True: 
                unit_conv = float(unix_timestamp / 1000)
                date_conv = str(datetime.utcfromtimestamp(unit_conv))
                return date_conv
            else:
                raise AuthEx.InvalidParameterType(unix_timestamp, float, unix_to_date.__name__)
        else:
            raise AuthEx.EmptyParameter(unix_to_date.__name__)
    except AuthEx.EmptyParameter as err:
        print(err.error_msg())
        return None
    except AuthEx.InvalidParameterType as err:
        print(err.error_msg())
        return None  


def settings() -> dict:
    '''loads the program's settings file into a python dict'''

    try:

        with open("file_paths.yaml") as paths_file:
            paths = yaml.safe_load(paths_file)
            settings_file_path = paths["program_files"]["settings"]

        with open(settings_file_path, mode='r') as settings_file:
            settings = yaml.safe_load(settings_file)
            return settings
        
    except FileNotFoundError as err:
        print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
        return None
    except FileExistsError as err:
        print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
        return None
    

def req_params() -> dict:
    '''loads the program's request parameters file into a python dict'''

    try:

        with open("file_paths.yaml") as paths_file:
            paths = yaml.safe_load(paths_file)
            request_file_path = paths["api_files"]["request_parameters"]

        with open(request_file_path, mode='r') as req_param_file:
            request_parameters = yaml.safe_load(req_param_file)
            return request_parameters
        
    except FileNotFoundError as err:
        print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
        return None
    except FileExistsError as err:
        print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
        return None
    

def file_paths() -> dict:
    '''loads the local file_paths.yaml configuration file into a python dict'''

    try:
        
        with open("file_paths.yaml") as paths_file:
            paths = yaml.safe_load(paths_file)
            return paths
        
    except FileNotFoundError as err:
        print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
        return None
    except FileExistsError as err:
        print("FileNotFoundError: Could not open <File: {}>. 1. Check to make sure that the file exists.\n2. That the file is in the program's working directory.\n".format(err.filename))
        return None
    

def verbose(method: str, obj_in_question: str, object_from: str, fp_to = str) -> None:
    '''For printing verbose program actions'''

    try:

        methods_list = ["get", "write", "sort"]

        if validate_parameters_exist(method, obj_in_question, object_from) == True:
            if validate_parameters_type(str, method, obj_in_question, object_from) == True:
                if method in methods_list:
                    if method == methods_list[0]:
                        print("\nGetting {} from {}.\n".format(obj_in_question, object_from))
                        return
                    elif method == methods_list[1]:
                        print("\nWriting {} from {} to {}.\n".format(obj_in_question, object_from, fp_to))
                        return
                    else:
                        print("\nSorting {} from {}.\n".format(obj_in_question, object_from))
                        return
                else:
                    raise AuthEx.InvalidParameter(method, verbose.__name__)
            else:
                raise AuthEx.InvalidParameterType("None", str, verbose.__name__)
        else:
            raise AuthEx.EmptyParameter(verbose.__name__)

    except AuthEx.InvalidParameter as err:
        print(err.error_msg())
        return 
    except AuthEx.InvalidParameterType as err:
        print(err.error_msg())
        return
    except AuthEx.EmptyParameter as err:
        print(err.error_msg())
        return