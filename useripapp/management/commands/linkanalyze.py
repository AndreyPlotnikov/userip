import time
from django.conf import settings
from django.core.management.base import BaseCommand

from useripapp.models import process_matches

class Command(BaseCommand):



    def add_arguments(self, parser):
        parser.add_argument('--max-iter', type=int, dest='max_iter')
        parser.add_argument('--max-rows', type=int, dest='max_rows',
                            default=settings.LINK_ANALYZE_MAX_SOURCE_ROWS)


    def handle(self, *args, **options):
        t0 = time.time()
        max_rows = options.get('max_rows')
        max_iter = options.get('max_iter')
        counter = 0
        while True:
            batch_start = time.time()
            result = process_matches(max_rows)
            if result is None:
                self.stdout.write('Another analyze process is running. Exiting...')
                break;
            self.stdout.write('Batch complete - n: {}; source rows: {}; inserts: {}; updates: {}; time: {:.2f}'.format(
                counter, result['source_rows'], result['num_inserts'], result['num_updates'], time.time() - batch_start
            ))
            counter += 1
            if result['complete']:
                break
            if max_iter and counter >= max_iter:
                break
        self.stdout.write('Analyze complete - time: {:.2f}'.format(
            (time.time() - t0)
        ))
