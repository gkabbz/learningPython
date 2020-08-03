import json
#https://developer.rhino3d.com/guides/rhinopython/python-xml-json/

dict = { "office":
    {"medical": [
      { "room-number": 100,
        "use": "reception",
        "sq-ft": 50,
        "price": 75
      },
      { "room-number": 101,
        "use": "waiting",
        "sq-ft": 250,
        "price": 75
      },
      { "room-number": 102,
        "use": "examination",
        "sq-ft": 125,
        "price": 150
      },
      { "room-number": 103,
        "use": "examination",
        "sq-ft": 125,
        "price": 150
      },
      { "room-number": 104,
        "use": "office",
        "sq-ft": 150,
        "price": 100
      }
    ],
    "parking": {
      "location": "premium",
      "style": "covered",
      "price": 750
    }
  }
}

print(type(dict))

# Json is a string representation of a dictionary


#TODO: 1. Saving json to a file
# Use dump to save json to a file
sample_json_file = '/Users/gkaberere/spark-warehouse/leanPlum/testABTestPull/sample_json_data.json'

def save_json_to_file(json_string):
    with open(sample_json_file,'w') as file:
        json.dump(json_string, file)

# Run Function Below
#save_json_to_file(dict)


#TODO: 2. Reading json from a file directly results in string object
#If you read the json file directly without using the json module you get a string type

def read_json_from_file_direct(file_name):
    with open(file_name, 'r') as file:
        read_data = file.read()
    return read_data

#Run Function Below
##read_data = read_json_from_file_direct(sample_json_file)

# A json file stores data as a string
##print(read_data)
##print(type(read_data))


#TODO: 3. If you have a string object, converting it back to a dict is simple using the json module
def convert_string_to_dict(string_variable):
    json_dict = json.loads(string_variable)
    return json_dict

##json_dict = convert_string_to_dict(read_data)
##print(json_dict)
##print(type(json_dict))


#TODO: 4. However, you can avoid all of that by reading a file using the json module - json loads
def read_json_from_file_with_json_module(file_name):
    with open(file_name, 'r') as file:
        read_data = json.load(file)
    return read_data

##json_dict = read_json_from_file_with_json_module(sample_json_file)
##print(json_dict)
##print(type(json_dict))


#TODO: 5. Question is raised however, when do you use json.load vs json.loads or json.dump vs json.dumps?
# dumps() = Encoding to json objects
# dump() = Encoding string when you are writing to a file
# loads() = Decoding a string to json object
# load() = Decoding when reading from a json file

#So in TODO:2 Above the variable would then be converted to an object using loads after
read_data = read_json_from_file_direct(sample_json_file)
##print(type(read_data))

# Convert the read_data variable to a dict using the json loads
read_data_conv = json.loads(read_data)
##print(type(read_data_conv))

# You end up with the same result as using the json.load directly in the file open as in 4 above
read_data_json_load = read_json_from_file_with_json_module(sample_json_file)
##print(type(read_data_json_load))

#TODO: 6. Creating a new line delimited json file

# New line delimited json (NDJSON) is a convenient format for storing and streaming structured data that may be
# processed one record at a time. It works well with unix-style text processing tools and shell pipelines.
# Each line is separated with '\n'
# The most common value will be objects or arrays but any json value is permitted

# So at times you'll have a json file but to be able to load it into bigquery specifically, you need to convert it
# to a newline delimited json

json_dict = dict

from io import StringIO

#Convert dict to string

json_dict = json.dumps(json_dict['office']['medical'])
##print(type(json_dict))
##print(json_dict)

# Convert the json into a stream

json_dict_stream = StringIO(json_dict)
##print(type(json_dict_stream))

result = [json.dumps(record) for record in json.load(json_dict_stream)]
new_line_delimited_result = '\n'.join(result)
##print(new_line_delimited_result)

# In this example, going in to the medical room level allows us to create a new line delimited json.
# This is because at that level the rooms are stored in a list. i.e. they are key-value pairs stored in a list as part
# of the dictionary

# What if you want to convert the entire dictionary? How do you replicate this setup to allow you to create a whole
# newline on the whole dictionary?

json_dict_full = dict
##print(json_dict_full)
##print(type(json_dict_full))

json_dict_full_json = json.dumps(json_dict_full)
##print(type(json_dict_full_json))
##print(json_dict_full_json)

# We want to make the adjustment when the dict is still a dict / object so that when we convert it to json it's in the
# format we need it to be

adjusted_json_dict_full = []
adjusted_json_dict_full.append(json_dict_full)
##print('Step 1')
##print(adjusted_json_dict_full)
##print(type(adjusted_json_dict_full))

# Now the dictionary is stored as a list. We can now follow the same method as above to convert to newline
adjusted_json_dict_full_json = json.dumps(adjusted_json_dict_full)
##print('Step 2')
##print(type(adjusted_json_dict_full_json))
##print(adjusted_json_dict_full_json)

adjusted_json_dict_stream = StringIO(adjusted_json_dict_full_json)
result2 = [json.dumps(record) for record in json.load(adjusted_json_dict_stream)]
new_line_delimited_result_2 = '\n'.join(result)
##print('this is the newline')
##print(new_line_delimited_result_2)

# So this seems to work but it works up to the same level as we'd seen before where it only returns the office room numbers
# I want the whole thing. I think I need to adjust the dict itself. Lets test

dict_v2 = {"office":[{"medical": [
      { "room_number": 100,
        "use": "reception",
        "sq_ft": 50,
        "price": 75
      },
      { "room_number": 101,
        "use": "waiting",
        "sq_ft": 250,
        "price": 75
      },
      { "room_number": 102,
        "use": "examination",
        "sq_ft": 125,
        "price": 150
      },
      { "room_number": 103,
        "use": "examination",
        "sq_ft": 125,
        "price": 150
      },
      { "room_number": 104,
        "use": "office",
        "sq_ft": 150,
        "price": 100
      }]},
    {"parking": {
      "location": "premium",
      "style": "covered",
      "price": 750
    }}]}
##print(type(dict_v2))


adjusted_dict2_full = []
adjusted_dict2_full.append(dict_v2)
print('Step 1')
##print(adjusted_dict2_full)
print(type(adjusted_dict2_full))

# Now the dictionary is stored as a list. We can now follow the same method as above to convert to newline
adjusted_dict2_full_json = json.dumps(adjusted_dict2_full)
##print('Step 2')
##print(type(adjusted_dict2_full_json))
##print(adjusted_dict2_full_json)

adjusted_dict2_stream = StringIO(adjusted_dict2_full_json)
result3 = [json.dumps(record) for record in json.load(adjusted_dict2_stream)]
new_line_delimited_result_3 = '\n'.join(result3)
##print('this is the newline')
##print(new_line_delimited_result_3)

save_test_newline = '/Users/gkaberere/spark-warehouse/leanPlum/testABTestPull/sample_newline_json_v3.json'

##with open(save_test_newline, 'w') as file:
##    file.write(new_line_delimited_result_3)




