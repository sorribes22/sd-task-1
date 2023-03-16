class LoadBalancerService:
    def send_meteo_data(self, temperature, humidity):
        print(f'Data recived: tmp={str(temperature)} hum={str(humidity)}')
        return 'Done'

    def send_pollution_data(self, co2):
        print(f'Data recived: co2={str(co2)}')
        return 'Done'


lb_service = LoadBalancerService()
