from atproto import Client


def main():
    client = Client()
    client.login('ttaships.bsky.social', 'uppv-3brz-zy6d-e7op')

    client.send_post(text='Hello World from Python!')


if __name__ == '__main__':
    main()
