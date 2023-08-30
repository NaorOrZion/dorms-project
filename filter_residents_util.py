from consts import *
from get_functions import *

def filter_residents(names_filter, 
                    frames_filter,
                    genders_filter,
                    services_filter,
                    beersheva_filter,
                    apartments_filter):
    '''
    This function is working like a funnel. It starts from all of the residents and step by step substracting unwanted residents.
    Eventually it will return the residents according to the funnel.
    Notice that if a part in the funnel is None (means that the users didn't choose to filter this part) this part will be eliminated,
    so it basically won't be part of the funnel/filter.
    The funnel works as follows:
        ------------------------------
                ALL RESIDENTS
        \                           /
         ---------------------------
                 FRAME FILTER
          \                       /
           -----------------------
                 GENDER FILTER
            \                   /
             -------------------
                SERVICE FILTER
              \               /
               ---------------
               BEERSHEVA FILTER
                \           /
                 -----------
                 APTS FILTER
                  \       /
                   -------
              FILTERED RESIDENTS

    @params: names_filter        -> List[str], 
             frames_filter       -> List[str], 
             genders_filter      -> List[str],
             services_filter     -> List[str],
             beersheva_filter    -> List[str],
             apartments_filter   -> List[str]

    Returns: Filtered residents  -> List[Dict[str, int/str]]
             Visual format: [{      
                                "id":           int,
                                "full_name":    str,
                                "association":  str,
                                "gender":       str,
                                "service":      str,
                                "beersheva":    str,
                                "taz":          str,
                                "apartment":    int
                            }]
    '''

    # Get the all the apartments existed from db as the following type: "List[Dict[str, int/str]]".
    all_residents_existed = get_residents_data()

    # From now on we will cut off unwanted residents.
    filtered_residents = all_residents_existed

    if names_filter:
        filtered_residents = residents_filtered_by_names(residents=filtered_residents, selected_names=names_filter)

    if frames_filter:
        filtered_residents = residents_filtered_by_frames(residents=filtered_residents, selected_frames=frames_filter)

    if genders_filter:
        filtered_residents = residents_filtered_by_genders(residents=filtered_residents, selected_genders=genders_filter)

    if services_filter:
        filtered_residents = reresidents_filtered_by_services(residents=filtered_residents, selected_services=services_filter)

    if beersheva_filter:
        filtered_residents = reresidents_filtered_by_beersheva(residents=filtered_residents, selected_beersheva=beersheva_filter)

    if apartments_filter:
        filtered_residents = residents_filtered_by_apartments(residents=filtered_residents, selected_apartments=apartments_filter)

    return filtered_residents


def residents_filtered_by_names(residents, selected_names):
    '''
    This function will filter the given residents by the given names parameter.
    How it will happen: The function will use the "selected_names" parameter 
                        then it will filter "residents" list (list of dictionaries) by the names of the residents.
    @params: residents                    -> List[Dict[str, int/str]],
             selected_names               -> List[str].
    Returns: List of filtered residents   -> List[Dict[str, int/str]].
    '''
    filtered_residents = []

    # Iterate over the names given
    # Format of name: "12 - Israel Israeli - DevOps"
    for name in selected_names:
        # If name is equal to EMPTY_BED_TEXT continue
        if name == EMPTY_BED_TEXT:
            continue

        # Split the name to get the id of the current resident
        name_data = name.split(" - ")
        name_id = int(name_data[0])
        
        # Iterate over all the residents to retrieve the wanted resident.
        # Append it to filtered_residents
        for resident in residents:
            if name_id == resident['id']:
                filtered_residents.append(resident)

    # Please take into conclusion that filtered_residents can be empty - []
    return filtered_residents


def residents_filtered_by_frames(residents, selected_frames):
    '''
    This function will filter the given residents by the given frames parameter.
    How it will happen: The function will use the "selected_frames" parameter 
                        then it will filter "residents" list (list of dictionaries) by the frames/assocciations of the residents.
    @params: residents                    -> List[Dict[str, int/str]],
             selected_frames              -> List[str].
    Returns: List of filtered residents   -> List[Dict[str, int/str]].
    '''
    filtered_residents = []

    # Iterate over all the residents to retrieve the frame/association of the resident.
    for resident in residents:
        # Get the frame of the current resident
        resident_frame = resident['association']

        # If the resident's frame match the selected frames, append it to filtered_residents.
        if resident_frame in selected_frames:
            filtered_residents.append(resident)

    return filtered_residents


def residents_filtered_by_genders(residents, selected_genders):
    '''
    This function will filter the given residents by the given genders parameter.
    How it will happen: The function will use the "selected_genders" parameter 
                        then it will filter "residents" list (list of dictionaries) by the genders of the residents.
    @params: residents                    -> List[Dict[str, int/str]],
             selected_genders             -> List[str].
    Returns: List of filtered residents   -> List[Dict[str, int/str]].
    '''
    filtered_residents = []

    # Iterate over all the residents to retrieve the gender of the resident.
    for resident in residents:
        # Get the gender of the current resident
        resident_gender = resident['gender']

        # If the resident's gender match the selected genders, append it to filtered_residents.
        if resident_gender in selected_genders:
            filtered_residents.append(resident)

    return filtered_residents


def reresidents_filtered_by_services(residents, selected_services):
    '''
    This function will filter the given residents by the given services parameter.
    How it will happen: The function will use the "selected_services" parameter 
                        then it will filter "residents" list (list of dictionaries) by the services of the residents.
    @params: residents                    -> List[Dict[str, int/str]],
             selected_services            -> List[str].
    Returns: List of filtered residents   -> List[Dict[str, int/str]].
    '''
    filtered_residents = []

    # Iterate over all the residents to retrieve the service of the resident.
    for resident in residents:
        # Get the gender of the current resident
        resident_service = resident['service']

        # If the resident's service match the selected services, append it to filtered_residents.
        if resident_service in selected_services:
            filtered_residents.append(resident)

    return filtered_residents


def reresidents_filtered_by_beersheva(residents, selected_beersheva):
    '''
    This function will filter the given residents by the given selected beersheva parameter.
    How it will happen: The function will use the "selected_beersheva" parameter 
                        then it will filter "residents" list (list of dictionaries) by the is_beersheva of the residents.
    @params: residents                    -> List[Dict[str, int/str]],
             selected_beersheva           -> List[str].
    Returns: List of filtered residents   -> List[Dict[str, int/str]].
    '''
    filtered_residents = []

    # Iterate over all the residents to retrieve the is_beersheva of the resident.
    for resident in residents:
        # Get the gender of the current resident
        resident_beersheva = resident['beersheva']

        # If the resident's is_beersheva match the selected beersheva options, append it to filtered_residents.
        if resident_beersheva in selected_beersheva:
            filtered_residents.append(resident)

    return filtered_residents


def residents_filtered_by_apartments(residents, selected_apartments):
    '''
    This function will filter the given residents by the given selected apartments parameter.
    How it will happen: The function will filter the "residents" list (list of dictionaries) by the selected_apartments of the residents.
    @params: residents                    -> List[Dict[str, int/str]],
             selected_apartments          -> List[str].
    Returns: List of filtered residents   -> List[Dict[str, int/str]].
    '''
    filtered_residents = []

    # Iterate over all the residents to retrieve the is_beersheva of the resident.
    for resident in residents:
        # Get the apartment of the current resident
        resident_apt = str(resident['apartment'])

        # If the resident's apartment match the selected apartments, append it to filtered_residents.
        if resident_apt in selected_apartments:
            filtered_residents.append(resident)

    return filtered_residents