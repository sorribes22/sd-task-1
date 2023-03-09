class LoadBalancerService:
    def send_meteo_data(self, temperature, humidity):
        print('Data recived' + temperature + ' ' + humidity)
        return 'Done'

    def send_pollution_data(self, co2, timestamp):
        print('Data recived' + co2 + ' ' + timestamp)
        return 'Done'


lb_service = LoadBalancerService();
