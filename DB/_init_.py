from DB import IChroma

if __name__ == '__main__':
    IChroma.create_client()
    # IChroma.clean_db()
    IChroma.init()
    print("DB inited ")