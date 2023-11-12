from atproto import Client

BLUESKY_EMAIL = environ['BLUESKY_EMAIL']
BLUESKY_PASSWORD = environ['BLUESKY_PASSWORD']


def main():
    client = Client()
    client.login(BLUESKY_EMAIL, BLUESKY_PASSWORD)

    client.send_post(text='Hello World from Python!')


if __name__ == '__main__':
    main()
