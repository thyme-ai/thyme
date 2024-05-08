from datetime import datetime

def get_easy_read_time(datetime_str):
    # Define the format string to match the input datetime string
    input_format_str = "%Y-%m-%dT%H:%M:%S%z"

    # Parse the string into a datetime object
    if type(datetime_str) is str:
        datetime_obj = datetime.strptime(datetime_str, input_format_str)
    else: 
        datetime_obj = datetime_str

    # Format the datetime object into the desired string format
    output_format_str = "%I:%M %p on %m/%d/%Y"
    formatted_datetime_str = datetime_obj.strftime(output_format_str)

    return formatted_datetime_str