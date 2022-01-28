import xml.etree.ElementTree as eTree

matrix_separator = ';'
array_separator = ','


def is_number(string):
    try:
        float(string)
    except ValueError:
        return False
    return True


def load_spt_file(filename, cp, r):

    tree = eTree.parse(filename)
    root = tree.getroot()
    for item in root.findall('variable'):
        component = item.find('component').text
        instance = item.find('instance').text
        varname = item.find('varname').text
        value = item.find('value').text
        if varname == 'wf_data':
            continue
        if component is None or instance is None or varname is None:
            raise Exception('Invalid SolarPILOT script file')
        name = f'{component}.{instance}.{varname}'
        # No value
        # TODO: Not sure what to do here
        if value is None:
            pass
            # cp.data_set_string(r, name, '')
        # Numeric value
        elif is_number(value) and varname not in ['weekday_sched', 'weekend_sched']:
            cp.data_set_number(r, name, float(value))
        # Matrix
        elif value.find(matrix_separator) > 0:
            if value[-1] == matrix_separator:
                value = value[:-1]
            matrix = []
            for row in value.split(matrix_separator):
                array = [float(element) if is_number(element) else None for element in row.split(array_separator)]
                if None in array:
                    continue
                matrix.append(array)
            cp.data_set_matrix(r, name, matrix)
        # Array
        elif value.find(array_separator) > 0:
            array = [float(element) if is_number(element) else None for element in value.split(array_separator)]
            if None in array:
                continue
            cp.data_set_array(r, name, array)
        # Boolean value
        elif value.lower() in ['true', 'false']:
            cp.data_set_number(r, name, 1 if value.lower() == 'true' else 0)
        # String
        else:
            cp.data_set_string(r, name, value)

    return True
