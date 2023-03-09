class LoadBalancerService:
    def send_meteo_data(self, temperature, humidity, timestamp):
        print('Data recived' + temperature + ' ' + humidity + ' ' + timestamp)
        return 'Done'

    def send_pollution_data(self, co2, timestamp):
        print('Data recived' + co2 + ' ' + timestamp)
        return 'Done'


lb_service = LoadBalancerService();
