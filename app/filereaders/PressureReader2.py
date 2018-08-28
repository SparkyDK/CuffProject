import configparser
configparser_defaults = dict(pmax=970, painvalue=910, paintolerance=10, patm=750)
def read_config(filename):
    parser = configparser.ConfigParser(defaults=configparser_defaults)
    parser.read(filename)
    values = {}
    for key in parser['Presure Config']:
        values[key] = parser['Presure Config'][key]
    return values