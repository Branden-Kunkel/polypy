# library to access API Data from 'polygon.io and then export that data
import re
import requests
import json
import yaml
import exceptions.exceptions as AuthEx
from datetime import datetime
import os.path as ospath
import toolkit 


class GetApiData():
    """class serves as an engine to access API data"""

    def generate_request_url2(self, base_url: str, options_ticker: str, ticker: str, date: str, request_parameters: dict) -> str:
        '''Generates and properly formats a request url for 'polygon.io' given parameters in configuration file'''

        try:
            ensure_value_exists = toolkit.validate_parameters_exist(base_url, options_ticker, ticker, date, request_parameters) 
            ensure_str_value = toolkit.validate_parameters_type(str, base_url, options_ticker, ticker, date)
            ensure_dict_value = toolkit.validate_parameters_type(dict, request_parameters)

            toolkit.verbose("Validating parameters for {}...".format(self.generate_request_url2.__name__))

            if ensure_value_exists == True:
                pass
            else:
                raise AuthEx.EmptyParameter(self.generate_request_url2.__name__)
            if ensure_str_value == True:
                pass 
            else:
                raise AuthEx.InvalidParameterType(ensure_str_value, str)
            if ensure_dict_value == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_dict_value, dict)
            
            toolkit.verbose("OK!\n")

            date_regex = re.compile("(?<=/)\{(?:date)\}")
            options_ticker_regex = re.compile("(?<=/)\{(?:optionsTicker)\}")
            ticker_regex = re.compile("(?<=/)\{(?:ticker)\}")

            url_buffer = re.sub(date_regex, date, base_url)
            url_buffer2 = re.sub(options_ticker_regex, options_ticker, url_buffer)
            url_buffer3 = re.sub(ticker_regex, ticker, url_buffer2)

            parameters_list = []
            endpoint_string = ""

            toolkit.verbose("Validating filters from 'request_parameters.yaml'...")

            for key, value in request_parameters.items():
                type_check = toolkit.validate_parameters_type(str, value)
                if value == None:
                    pass
                elif type_check != True:
                    print(AuthEx.ErrorMessage.req_params_yaml_err)
                    raise AuthEx.InvalidParameterType(type_check, str, self.generate_request_url2.__name__)
                else:
                    parameters_list.append(key + "=" + value)
            
            toolkit.verbose("OK!\n")

            endpoint_string = "&".join(parameters_list)

            request_url = url_buffer3 + endpoint_string    
            
            toolkit.verbose("Created request url for endpoint: {}\n".format(request_url))

            return request_url
    
        except AuthEx.EmptyParameter as err:
            print(err.error_msg())
            return None
        except AuthEx.InvalidParameterType as err:
            print(err.error_msg())
            return None
        except Exception as err:
            print(err.__cause__)
            print(err.with_traceback)
            print("AuthorError: This is an unexpected and unhandled error. Investigate immediately!")
            return None
            

    def request_data(self, url: str, api_key: str) -> dict:
        '''Makes a 'GET' API request to polygon.io'''

        try:
            ensure_value_exists = toolkit.validate_parameters_exist(url, api_key)
            ensure_str_type = toolkit.validate_parameters_type(str, url, api_key)

            toolkit.verbose("Validating parameters for {}...".format(self.request_data.__name__))
            
            if ensure_value_exists == True:
                pass
            else:
                raise AuthEx.EmptyParameter(self.request_data.__name__)
            if ensure_str_type == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_str_type, str, self.request_data.__name__)
            
            toolkit.verbose("OK!\n")
            
            toolkit.verbose("Sending 'GET' request to: {}".format(url))
            headers = {"Authorization" : api_key}
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                raise AuthEx.RequestStatusCodeError(response.reason, response.status_code)
            else:
                if response.content == None:
                    raise AuthEx.NoDataInResponse(url)
                else:
                    toolkit.verbose("Request successful!\n")
                    response_object = json.loads(response.content)
                    return response_object

        except AuthEx.EmptyParameter as err:
            print(err.error_msg())
            return None
        except AuthEx.InvalidParameterType as err:
            print(err.error_msg())
            return None
        except AuthEx.RequestStatusCodeError as err:
            print(err.error_msg())
            return None
        except AuthEx.NoDataInResponse as err:
            print(err.error_msg())
            return None
        


class ExportApiData():
    """class serves as an engine to export api data"""

    def sort_api_data(self, data_object: dict, request_url: str) -> dict:
        '''changes certain values to be human readable and adds program stamp(s) to an API response from polygon.io'''
        try:
            ensure_values_exist = toolkit.validate_parameters_exist(data_object, request_url)
            ensure_str_type = toolkit.validate_parameters_type(str, request_url)
            ensure_dict_type = toolkit.validate_parameters_type(dict, data_object)

            toolkit.verbose("Validating parameters for {}...".format(self.sort_api_data.__name__))

            if ensure_values_exist == True:
                pass
            else:
                raise AuthEx.EmptyParameter(self.sort_api_data.__name__)
            if ensure_str_type == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_str_type, str, self.sort_api_data.__name__)
            if ensure_dict_type == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_dict_type, dict, self.sort_api_data.__name__)

            toolkit.verbose("OK!\n")

            timestamp_object = datetime.now()
            timestamp = str(timestamp_object)
            data = data_object

            toolkit.verbose("Adding program metadata...\n")

            data.update({"auto": {}})
            data["auto"]["auto_timestamp"] = timestamp 
            data["auto"]["auto_url"] = request_url 

            values_dict = data["results"]["values"]

            toolkit.verbose("Converting UNIX timestamps to datetime...")
            
            for entry in values_dict:
                for key in entry:
                    if key == "timestamp":
                        entry[key] = toolkit.unix_to_date(entry[key])

            toolkit.verbose("Success!\n")
            return data

        except AuthEx.EmptyParameter as err:
            print(err.error_msg())
            return None
        except AuthEx.InvalidParameterType as err:
            print(err.error_msg())
            return None
        except KeyError as err:
            if "values" in err.args:
                print("Warning: No values found in response!")
                return data
            else:
                print("UNHANDLED ERROR!")
                return None
        except TypeError as err:
            return data



    def write_yaml(self, write_file_dir: str, data_object: dict, filename: str) -> None:
        '''Writes a dictionary data object (ex. api response) to a .yaml file'''

        try:        
            ensure_values_exist = toolkit.validate_parameters_exist(write_file_dir, data_object, filename)
            ensure_str_type = toolkit.validate_parameters_type(str, write_file_dir, filename)
            ensure_dict_type = toolkit.validate_parameters_type(dict, data_object)

            toolkit.verbose("Validating parameters for {}...".format(self.write_yaml.__name__))

            if ensure_values_exist == True:
                pass
            else:
                raise AuthEx.EmptyParameter(self.write_yaml.__name__)
            if ensure_str_type == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_str_type, str, self.write_yaml.__name__)
            if ensure_dict_type == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_dict_type, dict, self.write_yaml.__name__)
            
            toolkit.verbose("OK!\n")
            toolkit.verbose("Validating file extension...")

            split_ext = ospath.splitext(filename)
            file_ext = split_ext[1].lower()
            if file_ext != ".yaml":
                file_ext = ".yaml"
                filename = split_ext[0] + file_ext
            elif file_ext == None:
                filename = filename + ".yaml"
            else:
                pass

            toolkit.verbose("OK!\n")

            write_directory = write_file_dir
            full_path = write_directory + filename

            toolkit.verbose("Opening {} for writing...".format(full_path))
            
            with open(full_path, mode='a+') as write_file:
                yaml.safe_dump(data_object, write_file, explicit_start=True)

            toolkit.verbose("Successfully wrote data to file: {}\n".format(full_path))
            return
        
        except AuthEx.EmptyParameter as err:
            print(err.error_msg())
            return None
        except AuthEx.InvalidParameterType as err:
            print(err.error_msg())
            return None
        except FileNotFoundError as err:
            print("\nFileNotFoundError: {}\n".format(err.__cause__))
            return None
        
        

    def write_json(self, write_file_dir: str, data_object: dict, filename: str) -> None:
        '''Writes a dictionary data object (api response)to a .json file'''

        try:        
            ensure_values_exist = toolkit.validate_parameters_exist(write_file_dir, data_object, filename)
            ensure_str_type = toolkit.validate_parameters_type(str, write_file_dir, filename)
            ensure_dict_type = toolkit.validate_parameters_type(dict, data_object)

            toolkit.verbose("Validating parameters for {}...".format(self.write_json.__name__))

            if ensure_values_exist == True:
                pass
            else:
                raise AuthEx.EmptyParameter(self.write_json.__name__)
            if ensure_str_type == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_str_type, str, self.write_json.__name__)
            if ensure_dict_type == True:
                pass
            else:
                raise AuthEx.InvalidParameterType(ensure_dict_type, dict, self.write_json.__name__)

            toolkit.verbose("OK!\n")
            toolkit.verbose("Validating file extension...")

            split_ext = ospath.splitext(filename)
            file_ext = split_ext[1].lower()
            if file_ext != ".json":
                file_ext = ".json"
                filename = split_ext[0] + file_ext
            elif file_ext == None:
                filename = filename + ".json"
            else:
                pass

            toolkit.verbose("OK!\n")

            write_directory = write_file_dir
            full_path = write_directory + filename

            toolkit.verbose("Opening {} for writing...".format(full_path))

            with open(full_path, mode='a+') as write_file:
                json.dump(data_object, write_file, indent=4)

            toolkit.verbose("Successfully wrote data to file: {}\n".format(full_path))
            return
        
        except AuthEx.EmptyParameter as err:
            print(err.error_msg())
            return None
        except AuthEx.InvalidParameterType as err:
            print(err.error_msg())
            return None
        except FileNotFoundError as err:
            print("Error!: Invalid file directory specified in 'file_paths.yaml'[api_parameters][api_export].\n Could not write file.\n")
            return None