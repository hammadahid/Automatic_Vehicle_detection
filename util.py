import string
import easyocr
import sys


video_test = '/home/sare/Vehicle_Detection/videos/tests.mp4'



# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

# Mapping dictionaries for character conversion
dict_char_to_int = {'O': '0',
                    'I': '1',
                    'J': '3',
                    'A': '4',
                    'G': '6',
                    'S': '5'}

dict_int_to_char = {'0': 'O',
                    '1': 'I',
                    '3': 'J',
                    '4': 'A',
                    '6': 'G',
                    '5': 'S'}


def write_csv(results, output_path):
    """
    Write the results to a CSV file.

    Args:
        results (dict): Dictionary containing the results.
        output_path (str): Path to the output CSV file.
    """
    with open(output_path, 'w') as f:
        f.write('{},{},{},{},{},{},{},{},{},{}\n'.format('frame_nmr', 'vehicle_type','vehicle_score', 'car_id', 'timestamp', 'car_bbox',
                                                'license_plate_bbox', 'license_plate_bbox_score', 'license_number',
                                                'license_number_score'))

        for frame_nmr in results.keys():
            for car_id in results[frame_nmr].keys():
                #print(results[frame_nmr][car_id])
                if 'vehicle' in results[frame_nmr][car_id].keys() and \
                   'license_plate' in results[frame_nmr][car_id].keys() and \
                   'current_time' in results[frame_nmr][car_id].keys() and \
                   'text' in results[frame_nmr][car_id]['license_plate'].keys():
                    f.write('{},{},{},{},{},{},{},{},{},{}\n'.format(frame_nmr,
                                                            results[frame_nmr][car_id]['Vehicle_type'],
                                                            results[frame_nmr][car_id]['Vehicle_score'],
                                                            car_id,
                                                            results[frame_nmr][car_id]['current_time'],
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['vehicle']['bbox'][0],
                                                                results[frame_nmr][car_id]['vehicle']['bbox'][1],
                                                                results[frame_nmr][car_id]['vehicle']['bbox'][2],
                                                                results[frame_nmr][car_id]['vehicle']['bbox'][3]),
                                                            '[{} {} {} {}]'.format(
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][0],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][1],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][2],
                                                                results[frame_nmr][car_id]['license_plate']['bbox'][3]),
                                                            results[frame_nmr][car_id]['license_plate']['bbox_score'],
                                                            results[frame_nmr][car_id]['license_plate']['text'],
                                                            results[frame_nmr][car_id]['license_plate']['text_score'])
                            )
        f.close()


def format_1(text):
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in string.ascii_uppercase or text[2] in dict_int_to_char.keys()) and \
       (text[3] == " " )and \
       (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[4] in dict_char_to_int.keys()) and \
       (text[5] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[5] in dict_char_to_int.keys()) and \
       (text[6] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[6] in dict_char_to_int.keys()) and \
       (text[7] in string.ascii_uppercase or text[7] in dict_int_to_char.keys()) and \
       (text[8] in string.ascii_uppercase or text[8] in dict_int_to_char.keys()):
        return True
    else:
        return False


def format_2(text):
    if (text[0] in string.ascii_uppercase or text[0] in dict_int_to_char.keys()) and \
       (text[1] in string.ascii_uppercase or text[1] in dict_int_to_char.keys()) and \
       (text[2] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[2] in dict_char_to_int.keys()) and \
       (text[3] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[3] in dict_char_to_int.keys()) and \
       (text[4] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or text[4] in dict_char_to_int.keys()) and \
       (text[5] == " " )and \
       (text[6] in string.ascii_uppercase or text[6] in dict_int_to_char.keys()) and \
       (text[7] in string.ascii_uppercase or text[7] in dict_int_to_char.keys()) and \
       (text[8] in string.ascii_uppercase or text[8] in dict_int_to_char.keys()):
        return True
    else:
        return False


def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.

    Args:
        text (str): License plate text.

    Returns:
        bool: True if the license plate complies with the format, False otherwise.
    """

    result = [False, 0]

    #print("len of text is {}",len(text))
    if len(text) < 9:
        return 0


    if format_1(text):
        result[0] = True
        result[1] = 1
    elif format_2(text):
        result[0] = True
        result[1] = 2

    return 1

def format_license(text, format_type):
    """
    Format the license plate text by converting characters using the mapping dictionaries.

    Args:
        text (str): License plate text.

    Returns:
        str: Formatted license plate text.
    """
    #print("The lenght of text is {}", len(text))
    if (format_type == 0):
        return -1

    license_plate_ = ''

    mapping_1 = {0: dict_int_to_char, 1: dict_int_to_char, 2: dict_int_to_char, 3: dict_int_to_char, 7: dict_int_to_char,
                 4: dict_char_to_int, 5: dict_char_to_int, 6: dict_char_to_int , 8: dict_char_to_int}

    mapping_2 = {0: dict_int_to_char, 1: dict_int_to_char, 5: dict_int_to_char, 6: dict_int_to_char, 7: dict_int_to_char,
               2: dict_char_to_int, 3: dict_char_to_int, 4: dict_char_to_int, 8: dict_char_to_int}

    if (format_type == 1):
        mapping = mapping_1
    else:
        mapping = mapping_2

    for j in [0, 1, 2, 3, 4, 5, 6,7,8]:
        if text[j] in mapping[j].keys():
            license_plate_ += mapping[j][text[j]]
        else:
            license_plate_ += text[j]

    return license_plate_


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.

    Args:
        license_plate_crop (PIL.Image.Image): Cropped image containing the license plate.

    Returns:
        tuple: Tuple containing the formatted license plate text and its confidence score.
    """

    detections = reader.readtext(license_plate_crop)

    for detection in detections:
        bbox, text, score = detection

        # #print("first {}",len(text))

        #print("License Plate Before format: {}", text)
        if license_complies_format(text) == True:

            # formatted_text = format_license(text, license_complies_format(text)[1]), score
            formatted_text = format_license(text, 1)
            #print("License Plate After format: {}", formatted_text)

            return formatted_text,score

    return None, None


def get_vehicle(license_plate, vehicle_track_ids):
    """
    Retrieve the vehicle coordinates and ID based on the license plate coordinates.

    Args:
        license_plate (tuple): Tuple containing the coordinates of the license plate (x1, y1, x2, y2, score, class_id).
        vehicle_track_ids (list): List of vehicle track IDs and their corresponding coordinates.

    Returns:
        tuple: Tuple containing the vehicle coordinates (x1, y1, x2, y2) and ID.
    """
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1
