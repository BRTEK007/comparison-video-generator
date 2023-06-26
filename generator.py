import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='path to the config file', required=True)

    args = parser.parse_args()

    print(args.config)

if __name__ == '__main__':
    main()