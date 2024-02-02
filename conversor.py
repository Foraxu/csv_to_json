import json, csv

DATA_FILE = 'data.csv'
TEMP_FILE = 'tempfile.csv'
DATA_JSON = 'data.json'

class CsvToJson:
    def __init__(self):
        self.csv_formatted_dict = None
        self.lines_written = 0
        self.run_num = 0

    def saveCSVtoDict(self, csv_file: str):
        self.run_num += 1
        formatted_dict = {}

        with open(csv_file, 'r') as data:
            _dict = csv.DictReader(data)
        # Behind the scenes, at least at the point I know already, the action of looping through an obj using the for loop, calls a "next" function per loop.
        # The number of items in the dict obj have the possibility to overpass the number of times the "next" function can be called. 
        # Thus, if this happens, "passDataRemaining" creates a new file called "tempfile.csv" that stores only the data that was not managed yet, and call
            # this function again passing the new created file as the argument of this method.
            while True:
                
                try:
                    item = next(_dict)
                except:
                    if self.run_num == 1:
                        self.passDataRemaining(csv_file)
                    else:
                        break
                else:
                    try:
                        formatted_dict[item['word']]
                    except:
                        version = 1
                        formatted_dict[item['word']] = {
                            'version': {
                                version: {
                                    'type': item['pos'],
                                    'definition': item['def']
                                }
                            }
                        }
                    else: 
                        version += 1
                        formatted_dict[item['word']]['version'][version] = {
                            'type': item['pos'],
                            'definition': item['def']
                        }

                self.lines_written += 1

        self.csv_formatted_dict = formatted_dict
        return
    
    def passDataRemaining(self, file):

        with open(file, 'r') as file:
            lines = file.readlines()
            
            times = 0

        with open(TEMP_FILE, 'w') as output:

            for line in lines:
                if times == 0 or times >= self.lines_written:
                    print(times)
                    output.write(line)
                    times += 1
                else:
                    times += 1

        self.saveCSVtoDict(TEMP_FILE)

    
    def sendDictToJson(self, file, _dict):
        # Creates a .json file with a given name and save the dict content inside of the file

        try:
            with open(file, 'r+') as new_file:
                json.dump(_dict, new_file, indent=4)
        except:
            with open(file, 'w') as new_file:
                pass
            self.sendDictToJson(file, _dict)
        return

butter = CsvToJson()

butter.saveCSVtoDict(DATA_FILE)

butter.sendDictToJson(DATA_JSON, butter.csv_formatted_dict)
