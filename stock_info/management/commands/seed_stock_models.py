from django.core.management.base import BaseCommand, CommandError
from stock_info.models import Stock
class Command(BaseCommand):
    """
    This command is for seeding db with Stocks.

    1. Write arguments for stock csv
    2. Iterate through stock csv
    3. Insert each stocks data into the database.
    """
    help = 'The purpose of this command is to seed the stock models of a database with all of the required symbols'


    def handle(self, *args, **options):
        file_path = 'stock_seed_data/symbols_valid_meta.csv'
        print(file_path, "HI")
        with open(file_path) as file:

            for row in file:
                row = row.split(",")
                # destructure rows
                print(row, type(row), "ROW INFO")
                symbol,security_name,market_category  = row[1],row[2], row[4]
                print(symbol, security_name, market_category,"STOCK_INFO")
                new_stock = Stock(
                    ticker=symbol,
                    security_name=security_name,
                    market_category= market_category,
                    asset_class="STOCK"
                )
                new_stock.save()
                self.stdout.write(self.style.SUCCESS(f'{symbol} added to db'))



        