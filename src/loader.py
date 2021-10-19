import pandas as pd


def string_to_decimal_array(s):
    from decimal import Decimal
    return eval(s)


class SnapshotsLoader:

    @staticmethod
    def get_snapshots(filename):
        df = pd.read_csv(filename,
                         converters={'ask_prices': string_to_decimal_array,
                                     'bid_prices': string_to_decimal_array,
                                     'ask_amounts': string_to_decimal_array,
                                     'bid_amounts': string_to_decimal_array,
                                     'date': pd.to_datetime})
        df['best_ask'] = df.ask_prices.apply(lambda x: x[0])
        df['best_bid'] = df.bid_prices.apply(lambda x: x[0])
        print(f'Successfully loaded {len(df)} snapshots!')
        return df
