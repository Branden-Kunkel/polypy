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

            p_group1 = [base_url, options_ticker, ticker, date, request_parameters]
            p_group2 = [base_url, options_ticker, ticker, date]
            p_group3 = [request_parameters]

            for parameter in p_group1:
                validate = toolkit.validate_parameters_exist(parameter)
                if validate == True:
                    pass
                else:
                    raise AuthEx.EmptyParameter(self.generate_request_url2.__name__)
            for parameter in p_group2:
                validate = toolkit.validate_parameters_type(str, parameter)
                if validate == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, str, self.generate_request_url2.__name__)
            for parameter in p_group3:
                validate = toolkit.validate_parameters_type(dict, parameter)
                if validate == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, dict, self.generate_request_url2.__name__)
                                
            date_regex = re.compile("(?<=/)\{(?:date)\}")
            options_ticker_regex = re.compile("(?<=/)\{(?:optionsTicker)\}")
            ticker_regex = re.compile("(?<=/)\{(?:ticker)\}")

            url_buffer = re.sub(date_regex, date, base_url)
            url_buffer2 = re.sub(options_ticker_regex, options_ticker, url_buffer)
            url_buffer3 = re.sub(ticker_regex, ticker, url_buffer2)

            parameters_list = []
            endpoint_string = ""
    
            for key, value in request_parameters.items():
                p_check = toolkit.validate_parameters_type(str, value)
                if value == None:
                    pass
                elif p_check == False:
                    raise AuthEx.InvalidParameterType(value, str, self.generate_request_url2.__name__)
                else:
                    parameters_list.append(key + "=" + value)

            endpoint_string = "&".join(parameters_list)

            request_url = url_buffer3 + endpoint_string    
            
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

        p_group1 = [url, api_key]

        try:

            for parameter in p_group1:
                p_check1 = toolkit.validate_parameters_exist(parameter)
                if p_check1 == True:
                    pass
                else:
                    raise AuthEx.EmptyParameter(self.request_data.__name__)
            for parameter in p_group1:
                p_check2 = toolkit.validate_parameters_type(str, parameter)
                if p_check2 == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, str, self.request_data.__name__)
            
            headers = {"Authorization" : api_key}
            response = requests.get(url, headers=headers)

            status = response.status_code
            reason = response.reason

            if status != 200:
                raise AuthEx.RequestStatusCodeError(reason, response.status_code)
            else:
                if response.content == None:
                    raise AuthEx.NoDataInResponse(url)
                else:
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
            p_group1 = [data_object, request_url]
            p_group2 = [data_object]
            p_group3 = [request_url]

            for parameter in p_group1:
                check = toolkit.validate_parameters_exist(parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.EmptyParameter(self.sort_api_data.__name__)
            for parameter in p_group2:
                check = toolkit.validate_parameters_type(dict, parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, dict, self.sort_api_data.__name__)
            for parameter in p_group3:
                check = toolkit.validate_parameters_type(str, parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, str, self.sort_api_data.__name__)

            timestamp_object = datetime.now()
            timestamp = str(timestamp_object)
            data = data_object

            data.update({"auto": {}})
            data["auto"]["auto_timestamp"] = timestamp 
            data["auto"]["auto_url"] = request_url 

            for dict_entry in data["results"]["values"]:
                for key in dict_entry:
                    if key == "timestamp":
                        dict_entry[key] = toolkit.unix_to_date(dict_entry[key])

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



    def write_yaml(self, write_file_dir: str, data_object: dict, filename: str) -> None:
        '''Writes a dictionary data object (ex. api response) to a .yaml file'''

        try:        
            p_group1 = [write_file_dir, data_object, filename]
            p_group2 = [write_file_dir, filename]
            p_group3 = [data_object]

            for parameter in p_group1:
                check = toolkit.validate_parameters_exist(parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.EmptyParameter(self.write_yaml.__name__)
            for parameter in p_group2:
                check = toolkit.validate_parameters_type(str, parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, str, self.write_yaml.__name__)
            for parameter in p_group3:
                check = toolkit.validate_parameters_type(dict, parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, dict, self.write_yaml.__name__)
                
            split_ext = ospath.splitext(filename)
            file_ext = split_ext[1].lower()
            if file_ext != ".yaml":
                file_ext = ".yaml"
                filename = split_ext[0] + file_ext
            elif file_ext == None:
                filename = filename + ".yaml"
            else:
                pass

            write_directory = write_file_dir
            full_path = write_directory + filename

            with open(full_path, mode='a+') as write_file:
                yaml.safe_dump(data_object, write_file, explicit_start=True)

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
            p_group1 = [write_file_dir, data_object, filename]
            p_group2 = [write_file_dir, filename]
            p_group3 = [data_object]

            for parameter in p_group1:
                check = toolkit.validate_parameters_exist(parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.EmptyParameter(self.write_json.__name__)
            for parameter in p_group2:
                check = toolkit.validate_parameters_type(str, parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, str, self.write_json.__name__)
            for parameter in p_group3:
                check = toolkit.validate_parameters_type(dict, parameter)
                if check == True:
                    pass
                else:
                    raise AuthEx.InvalidParameterType(parameter, dict, self.write_json.__name__)

            split_ext = ospath.splitext(filename)
            file_ext = split_ext[1].lower()
            if file_ext != ".json":
                file_ext = ".json"
                filename = split_ext[0] + file_ext
            elif file_ext == None:
                filename = filename + ".json"
            else:
                pass

            write_directory = write_file_dir
            full_path = write_directory + filename

            with open(full_path, mode='a+') as write_file:
                json.dump(data_object, write_file, indent=4)

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