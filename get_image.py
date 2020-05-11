from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
import sys
from getpass import getpass

username = input("username:")
passward = getpass("passward:")

api = SentinelAPI(username, passward)


def filter():

    print()
    print('Setting sensing period')
    start = input('From?  (yyyymmdd)  ')
    end = input('To?    (yyyymmdd)  ')
    orbit = input('Orbit?   (A or D)         ')

    return(start, end, orbit)


def open_hub(start, end, path):

    footprint = geojson_to_wkt(read_geojson('./study_area.geojson'))
    data = api.query(area=footprint, date=(start, end),
                     producttype='GRD', area_relation='Contains')
    data_df = api.to_dataframe(data)
    if "A" in path:
        data_df_o = data_df[data_df['orbitdirection'] == 'ASCENDING']
    else:
        data_df_o = data_df[data_df['orbitdirection'] == 'DESCENDING']
    data_df_D_sort = data_df_o.sort_values(by='summary').reset_index(drop=True)

    print(data_df_D_sort[['summary', 'orbitdirection']])
    inp = input('Do you want to download? [y/n] ')
    if inp in ['y', 'ye', 'yes']:
        uuid = data_df_D_sort[['uuid']].as_matrix()
    else:
        sys.exit()

    for uuid in uuid:
        api.download(uuid[0], directory_path=path+'1-row_data/')
