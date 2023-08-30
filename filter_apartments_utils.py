from consts import *
from get_functions import *

def filter_apartments(names_filter, apartments_filter, frames_filter, genders_filter, is_empty_beds_filter) -> List[Dict[str, int]]:
    '''
    This function is working like a funnel. It starts from all of the apartments and step by step substracting unwanted apartments.
    Eventually it will return the apartments according to the funnel.
    Notice that if a part in the funnel is None (means that the users didn't choose to filter this part) this part will be eliminated,
    so it basically it won't be part of the funnel/filter.
    The funnel works as follows:
        ------------------------------
                ALL APARTMENTS
        \                           /
         ---------------------------
                 NAME FILTER
          \                       /
           -----------------------
                 SPECIFIC APTS
            \                   /
             -------------------
                GENDER FILTER
              \               /
               ---------------
                 FRAME FILTER
                \           /
                 -----------
                  \       /
             FILTERED APARTMENTS

    @params: names_filter        -> List[str], 
             apartments_filter   -> List[str], 
             frames_filter       -> List[str], 
             genders_filter      -> List[str]

    Returns: Filtered apartments -> List[Dict[str, int]]
             Visual format: [{      
                                "apt_id":       int,
                                "rooms_in_apt": int,
                                "gender":       int,
                                "building_id":  int
                            }]
    '''
    # Get the all the apartments existed from db as the following type: "List[Dict[str, int]]".
    all_apartments_existed = get_apartments_data()

    # From now on we will cut off unwanted apartments.
    filtered_apartments = all_apartments_existed

    if names_filter:
        filtered_apartments = apartments_filtered_by_names(apartments=filtered_apartments, selected_names=names_filter)

    if apartments_filter:
        filtered_apartments = apartments_filtered_by_apartments(apartments=filtered_apartments, selected_apartments=apartments_filter)

    if frames_filter:
        filtered_apartments = apartments_filtered_by_frames(apartments=filtered_apartments, selected_frames=frames_filter)

    if genders_filter:
        filtered_apartments = apartments_filtered_by_genders(apartments=filtered_apartments, selected_genders=genders_filter)

    if is_empty_beds_filter == "כן":
        filtered_apartments = apartments_filtered_by_empty_beds(apartments=filtered_apartments)

    return filtered_apartments


def apartments_filtered_by_names(apartments, selected_names) -> List[Dict[str, int]]:
    '''
    This function will filter the given apartments by the given names parameter.
    How it will happen: The function will retrieve the wanted residents (by the names parameter) from the "residents" table.
                        After that it will retrieve the residents' apartment.
                        Then it will filter "apartments" list (list of dictionaries) by the apartments of the residents it gathered.
    @params: filter_apartments           -> List[Dict[str, int]],
             names                       -> List[str].
    Returns: List of filtered apartments -> List[Dict[str, int]].
    '''

    all_residents = get_residents_data()
    filtered_apartments = []
    residents_apartments = []

    # Iterate over the names given
    # Format of name: "12 - Israel Israeli - DevOps"
    for name in selected_names:
        # If name is equal to EMPTY_BED_TEXT continue
        if name == EMPTY_BED_TEXT:
            continue

        # Split the name to get the id of the current resident
        name_data = name.split(" - ")
        name_id = int(name_data[0])
        
        # Iterate over all the residents to retrieve the apartment of the resident.
        # Append it to residents_apartments
        for resident in all_residents:
            if name_id != resident['id']:
                continue

            # If the resident own an apartment (if his apt is not None), append apt to residents_apartments
            if resident["apartment"]:
                residents_apartments.append(resident['apartment'])

    # Iterate over the apartments parameter and check if the apartment id is in the residents_apartments which has been gathered before.
    # Append the apartment if so.
    for apartment in apartments:
        if apartment['apt_id'] in residents_apartments:
            filtered_apartments.append(apartment)

    # Please take into conclusion that filtered_apartments can be empty - []
    return filtered_apartments

        
def apartments_filtered_by_apartments(apartments, selected_apartments) -> List[Dict[str, int]]:
    '''
    This function will filter the given apartments by the selected_apartments.
    It will iterate over the apartments list, check whether the selected apartment in the current iteration is in the apartments dict,
    if so, append it to the filtered_apartments list.
    @params: apartments                  -> List[Dict[str, int]],
             selected_apartments         -> List[str]
    Returns: List of filtered apartments -> List[Dict[str, int]].
    '''
    filtered_apartments = []

    for selected_apartment in selected_apartments:
        for apartment in apartments:
            if int(selected_apartment) == apartment['apt_id']:
                filtered_apartments.append(apartment)

    return filtered_apartments


def apartments_filtered_by_frames(apartments, selected_frames) -> List[Dict[str, int]]:
    '''
    This function will filter the given apartments by the selected frames.
    It will first iterate over all the residents and retrieve the residents apartment which their frame is in the selected_frames list.
    @params: apartments                  -> List[Dict[str, int]],
             selected_frames             -> List[str]
    Returns: List of filtered apartments -> List[Dict[str, int]].
    '''
    all_residents = get_residents_data()
    filtered_apartments = []
    residents_apartments = []

    # Format of selected_frames: List[str]
    # Iterate over all the residents to retrieve the frame/association of the resident.
    for resident in all_residents:
        # Get the frame of the current resident
        resident_frame = resident['association']

        # If the resident's frame doesn't match to the selected frames, continue
        if resident_frame not in selected_frames:
            continue

        # If the resident own an apartment (if his apt is not None), append apt to residents_apartments
        if resident["apartment"]:
            residents_apartments.append(resident['apartment'])

    # Iterate over the apartments parameter and check if the apartment id is in the residents_apartments which has been gathered before.
    # Append the apartment if so.
    for apartment in apartments:
        if apartment['apt_id'] in residents_apartments:
            filtered_apartments.append(apartment)

    return filtered_apartments


def apartments_filtered_by_genders(apartments, selected_genders) -> List[Dict[str, int]]:
    '''
    This function will filter the given apartments by the selected genders.
    It will iterate over the selected genders, check whether the selected gender is in one of the apartments,
    if so, append it to the filtered_apartments list.
    @params: apartments                  -> List[Dict[str, int]],
             selected_genders            -> List[str].
    Returns: List of filtered apartments -> List[Dict[str, int]].
    '''
    filtered_apartments = []

    for selected_gender in selected_genders:
        for apt in apartments:
            if selected_gender == apt['gender']:
                filtered_apartments.append(apt)

    return filtered_apartments


def apartments_filtered_by_empty_beds(apartments):
    '''
    This function will filter the given apartments by empty beds, 
    so if there is an empty bed in the apartment count this apartment in the filtered apartments list.
    @params: apartments                  -> List[Dict[str, int]].
    Returns: List of filtered apartments -> List[Dict[str, int]].
    '''
    all_bunk_beds = get_bunk_beds()
    all_aminach_beds = get_aminach_beds()
    filtered_apartments = []
    empty_beds_apartments = []

    # Iterate over all the bunk beds to retrieve the apartment of the resident who is name is equal to EMPTY_BED_TEXT.
    # Append it to filtered_apartments
    for bunk_bed in all_bunk_beds:
        if EMPTY_BED_TEXT in [bunk_bed['person2'], bunk_bed['person1']]:
            empty_beds_apartments.append(bunk_bed['apt_id'])
    
    for aminach_bed in all_aminach_beds:
        if EMPTY_BED_TEXT == aminach_bed['person1']:
            empty_beds_apartments.append(aminach_bed['apt_id'])

    # Iterate over the apartments parameter and check if the apartment id is in the empty_beds_apartments which has been gathered before.
    # Append the apartment if so.
    for apartment in apartments:
        if apartment['apt_id'] in empty_beds_apartments:
            filtered_apartments.append(apartment)

    return filtered_apartments
    
