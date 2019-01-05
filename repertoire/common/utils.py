def get_formatted_datetime():
    from datetime import datetime
    from repertoire.common.types import Constants
    return datetime.utcnow().strftime(Constants.FORMAT_DATE_TIME)