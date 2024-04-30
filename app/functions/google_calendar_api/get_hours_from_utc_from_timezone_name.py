import pytz

SECONDS_PER_HOUR = 3600

# Converts timezone name (e.g. "America/Los_Angeles") 
# into an offset in hours from Coordinated Universal Time, or UTC, (e.g. 7 hours)
def get_hours_from_utc_from_timezone_name(timezone_name):
    # Get the timezone object
    timezone = pytz.timezone(timezone_name)
    
    # Get the current UTC offset for the timezone
    utc_offset = timezone.utcoffset(pytz.datetime.datetime.now())
    
    # Convert the offset to hours
    hours_from_utc = utc_offset.total_seconds() / SECONDS_PER_HOUR
    return hours_from_utc