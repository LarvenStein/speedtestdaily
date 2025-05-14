import speedtest

def get_speedtest_id():

    servers = []

    s = speedtest.Speedtest()
    
    s.get_servers(servers)
    s.get_best_server()
    
    s.download()
    s.upload()
    
    return get_id_from_share(s.results.share())

def get_id_from_share(share_url):
    image_name = share_url.split('/')[4]

    id = image_name.split('.')[0]

    return id