from datetime import date
#  Takes in an input of format MM-DD-YYYY and returns
#  a date value. Throws execption if input is invalid
#  unless it doesn't quite fill the gaps between dashes
#  cuz then it doesn't really matter
def import_mmddyyyy(date_str : str) -> date:
    split_date: list[str] = date_str.split("-")
    if len(split_date) != 3 :
        raise ValueError(f"couldn't determine date from string {date_str}")
    
    for index in range(len(split_date)):
        split_date[index] = int(split_date[index])
    
    if split_date[0] < 1 or split_date[0] > 12:
        raise ValueError(f"invalid month of {split_date[0]}; must be >= 1 and <= 12")
    if split_date[1] < 1 or split_date[1] > 31:
        raise ValueError(f"invalid day of {split_date[1]}; must be >= 1 and <= 31")
    if split_date[2] < 0:
        # idk how one would even call this you know
        raise ValueError(f"invalid year of {split_date[2]}; must be >= 0")

    if not float(split_date[0]).is_integer():
        ValueError(f"invalid month of {split_date[0]}; must be integer")
    if not float(split_date[1]).is_integer():
        ValueError(f"invalid day of {split_date[1]}; must be integer")
    if not float(split_date[2]).is_integer():
        ValueError(f"invalid year of {split_date[2]}; must be integer")
    return date(split_date[2], split_date[0], split_date[1])