import logging
import argparse
import pandas
import requests


# Sample use:
# python Update.py --update --dry-run


class Update(object):
    def __init__(self, filename=None, dry_run=None):
        self.filename = filename
        self.dry_run = dry_run

    def update(self):
        persons = pandas.read_csv(self.filename, engine='python', encoding='utf-8')
        for index, person in persons.iterrows():
            payload = {'your-name': person['first_name'], 'your-email': person['email'],
                       'your-number': person['phone_number'], 'your-country': person['country']}
            logging.info('Getting person for {}'.format(payload))
            if not self.dry_run:
                response = requests.post(
                    'https://login.centrexsoftware.com/post/5d9a6b957c8d0b3ae0711a4e665194a81ac88560/'
                    , params=payload)
                assert 'Success' in response.content, 'Response is not ok!!'.format(response.content)
            else:
                logging.info('index={}'.format(index))
                logging.info('Not effecting database on dry run!')

        logging.info('Updating DataBase Done Successfully!')

    @classmethod
    def main(cls):
        parser = argparse.ArgumentParser()
        commands = parser.add_mutually_exclusive_group(required=True)
        commands.add_argument('--update', action='store_true')
        parser.add_argument('--csv', '--filename', default='leads.csv',
                            help='Custom input, by default leads.csv')
        parser.add_argument('--dry-run', action='store_true',
                            help='Parse the data but do not commit to the database.')
        args = parser.parse_args()
        data = cls(args.csv, args.dry_run)
        if args.update:
            data.update()
        elif args.insert:
            raise NotImplementedError()
        else:
            logging.info('Nothing to do.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Update.main()
