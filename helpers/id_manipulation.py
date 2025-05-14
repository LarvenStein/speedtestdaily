import random

def randomize_test_id(test_id):
    return int(test_id) + random.randint(10, 150)

def generate_image_url(test_id):
    return f"https://speedtest.net/result/{test_id}.png"

def generate_test_url(test_id):
    return f"https://speedtest.net/result/{test_id}.html"