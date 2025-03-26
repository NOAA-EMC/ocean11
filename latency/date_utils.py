import logging
# import os
# import sys 
# import shutil
import re
from datetime import datetime, timedelta


def extract_first_date(filename, logger=None):
    if logger is None:
        logger = logging.getLogger(__name__)
    logger.debug(f"Extracting date from {filename}")

    # Define regex patterns for each date format
    patterns = [
        r'(\d{8}T\d{6})',      # YYYYMMDDThhmmss
        r'(\d{14}0)',          # YYYYMMDDHHmmss0
        r'(\d{14})',           # YYYYMMDDHHmmss
        r'(\d{7})'             # YYYYDDD (Julian date)
    ]

    # print(f">>>>>>>>>>>>>>>>>>> {type(filename)} length = {len(filename)}")
    # if isinstance(filename, list):
        # filename = filename[0] 

    # Loop through patterns to find the first valid date
    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            date_str = match.group(1)
            # print("date_str = ", date_str)
            # print("len date_str = ", len(date_str))
            try:
                if len(date_str) == 15:
                    if (date_str[8] == 'T'):
                        try:
                            return datetime.strptime(date_str, '%Y%m%dT%H%M%S')
                        except ValueError:
                           continue
                    else:
                        try:
                            return datetime.strptime(date_str, '%Y%m%d%H%M%S0')
                        except ValueError:
                           continue
                elif len(date_str) == 14:   # YYYYMMDDHHmmss
                    try:
                        return datetime.strptime(date_str, '%Y%m%d%H%M%S')
                    except ValueError:
                       continue
                elif len(date_str) == 7:   # YYYYDDD
                    year = int(date_str[:4])
                    julian_day = int(date_str[4:])
                    if not (0 <= year <= 9999):
                        logger.warning(f'In filename {filename}  YYYY = {year} is not a valid year')
                        return None
                    if not is_julian_date(year, julian_day):
                        logger.warning(f'In filename {filename}  YYYY = {year} DDD = {julian_day} is not a valid julian date')
                        return None
                    return datetime(year, 1, 1) + timedelta(days=julian_day - 1)
            except ValueError:
                logger.debug(f'In filename {filename},  >>>>>  {year} {julian_day}')
                logger.warning(f'In filename {filename},  {date_str} is not a recognized date format')
                continue

    # Return None if no valid date is found
    return None
