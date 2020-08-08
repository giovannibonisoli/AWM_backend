from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime

from vinegar_cellar.models import BarrelSet, Barrel, OperationType, Operation


class OperationTests(APITestCase):

    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username,
                                        password=self.password)
        self.client.force_authenticate(user=self.user)

        for name in ['prelievo', 'rabbocco']:
            OperationType.objects.create(name=name, schema=[])

        for year in range(1992, 1994):
            barset = BarrelSet.objects.create(year=year)

            for wood in ['Ciliegio', 'Ginepro', 'Gelso']:
                Barrel.objects.create(barrel_set=barset, wood_type=wood,
                                      capability=70)

    def test_set_get_1(self):
        response = self.client.get('/api/operations/prelievo/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get('/api/operations/rabbocco/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_set_get_2(self):
        for i in range(1, 4):
            operation = OperationType.objects.get(name="prelievo")
            barrel = Barrel.objects.get(pk=i)
            date = datetime.today().strftime('%Y-%m-%d')

            Operation.objects.create(type=operation, barrel=barrel,
                                     date=date, values={})

        for i in range(5, 7):
            operation = OperationType.objects.get(name="rabbocco")
            barrel = Barrel.objects.get(pk=i)
            date = datetime.today().strftime('%Y-%m-%d')

            Operation.objects.create(type=operation, barrel=barrel,
                                     date=date, values={})

        response = self.client.get('/api/operations/prelievo/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        response = self.client.get('/api/operations/rabbocco/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_set_post(self):
        data = {
                "type": "rabbocco",
                "barrel": 1,
                "date": datetime.today().strftime('%Y-%m-%d'),
                "values": "{}"
                }
        response = self.client.post('/api/operations/prelievo/', data=data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 0)

        response = self.client.post('/api/operations/rabbocco/', data=data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Operation.objects.count(), 1)

    def test_detail_get(self):
        operation = OperationType.objects.get(name="rabbocco")
        barrel = Barrel.objects.get(pk=1)
        date = datetime.today().strftime('%Y-%m-%d')
        instance = Operation.objects.create(type=operation,
                                            barrel=barrel,
                                            date=date,
                                            values={})
        response = self.client.get('/api/operations/rabbocco/' + str(instance.id) + '/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['barrel'], 1)
        self.assertEqual(response.data['date'], date)
        self.assertEqual(response.data['values'], '{}')

    def test_detail_put(self):
        operation = OperationType.objects.get(name="rabbocco")
        barrel = Barrel.objects.get(pk=1)
        date = datetime.today().strftime('%Y-%m-%d')
        instance = Operation.objects.create(type=operation,
                                            barrel=barrel,
                                            date=date,
                                            values={})

        data = {
                "type": "rabbocco",
                "barrel": 1,
                "date": datetime.today().strftime('%Y-%m-%d'),
                "values": "{'bar_dest': 3, 'quantity': 10}"
                }

        response = self.client.put('/api/operations/rabbocco/' + str(instance.id) + '/',
                                   data=data, format='json')

        instance = Operation.objects.get(pk=instance.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(instance.type.name, data['type'])
        self.assertEqual(instance.barrel.id, data['barrel'])
        self.assertEqual(str(instance.date), data['date'])
        self.assertEqual(instance.values, data['values'])
