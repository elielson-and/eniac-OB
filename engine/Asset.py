

class Asset:
    def __init__(self, api) -> None:
        self.api = api


    def get_available_digital_assets(self):
        digital_assets = []
        assets = self.api.get_all_profit()
        
        # for asset in assets:
        #     asset_info = self.api.get_instrument_info(asset)
        #     if asset_info['digital']:
        #         digital_assets.append(asset)
        # print(digital_assets)



    def get_available_binary_assets():
        pass
        # Maybe later