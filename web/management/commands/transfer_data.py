from django.core.management.base import BaseCommand
from web.models import WebFarsl, WebMcust, WebPcust
from django.db import transaction

class Command(BaseCommand):
    help = 'Transfers data from MySQL to PostgreSQL'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data transfer...'))
        
        try:
            with transaction.atomic():
                # 1. Transfer WebFarsl
                self.stdout.write('Transferring WebFarsl...')
                farsl_count = 0
                for obj in WebFarsl.objects.using('mysql').all():
                    WebFarsl.objects.using('default').create(
                        fid=obj.fid,
                        fname=obj.fname
                    )
                    farsl_count += 1
                
                # 2. Transfer WebMcust
                self.stdout.write('Transferring WebMcust...')
                mcust_count = 0
                for obj in WebMcust.objects.using('mysql').all():
                    WebMcust.objects.using('default').create(
                        fid=obj.fid,
                        fname=obj.fname,
                        fpassword=obj.fpassword
                    )
                    mcust_count += 1
                
                # 3. Transfer WebPcust (handles foreign keys)
                self.stdout.write('Transferring WebPcust...')
                pcust_count = 0
                for obj in WebPcust.objects.using('mysql').all():
                    WebPcust.objects.using('default').create(
                        fauto=obj.fauto,
                        fcust_id=obj.fcust_id,  # preserves FK relationship
                        fsl_id=obj.fsl_id,       # preserves FK relationship
                        fdoc=obj.fdoc,
                        fsdate=obj.fsdate,
                        frem=obj.frem,
                        fsdr=obj.fsdr,
                        fscr=obj.fscr,
                        fsbal=obj.fsbal
                    )
                    pcust_count += 1
                
                self.stdout.write(self.style.SUCCESS(
                    f'Successfully transferred: '
                    f'{farsl_count} WebFarsl, '
                    f'{mcust_count} WebMcust, '
                    f'{pcust_count} WebPcust records'
                ))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Transfer failed: {str(e)}'))
            raise