from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime

from vinegar_cellar.models import BarrelSet, Barrel, OperationType, Operation


class BarrelTests(APITestCase):

    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username,
                                        password=self.password)
        self.client.force_authenticate(user=self.user)

        for number in range(1, 3):
            BarrelSet.objects.create(id=number, year=(number+1991))

    def test_create_1(self):
        data = {
            'barrel_set': 1,
            'wood_type': 'Ciliegio',
            'capability': 40
        }
        response = self.client.post('/api/barrel/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 'BAR0101')

    def test_create_2(self):
        bar_set = BarrelSet.objects.get(pk=1)
        Barrel.objects.create(id='BAR0102', barrel_set=bar_set,
                              wood_type='Rovere', capability=70)
        data = {
            'barrel_set': 1,
            'wood_type': 'Ciliegio',
            'capability': 40
        }
        response = self.client.post('/api/barrel/', data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 'BAR0103')

    def test_get_set(self):
        bar_set = BarrelSet.objects.all()
        for i, wood in enumerate(['Ciliegio', 'Ginepro', 'Gelso']):
            id = 'BAR' + str(bar_set[0].id).zfill(2) + str(i).zfill(2)
            Barrel.objects.create(id=id, barrel_set=bar_set[0],
                                  wood_type=wood, capability=70)

        response = self.client.get('/api/barrel/set/{}/'.format(bar_set[0].id),
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        for i, wood in enumerate(['Ciliegio', 'Ginepro']):
            id = 'BAR' + str(bar_set[1].id).zfill(2) + str(i).zfill(2)
            Barrel.objects.create(id=id, barrel_set=bar_set[1],
                                  wood_type=wood, capability=70)

        response = self.client.get('/api/barrel/set/{}/'.format(bar_set[1].id),
                                   format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class OperationTests(APITestCase):

    def setUp(self):
        self.username = 'john_doe'
        self.password = 'foobar'
        self.user = User.objects.create(username=self.username,
                                        password=self.password)
        self.client.force_authenticate(user=self.user)

        for name in ['prelievo', 'rabbocco']:
            OperationType.objects.create(id=name, name=name, description="",
                                         schema=[])

        for number in range(1, 3):
            barset = BarrelSet.objects.create(id=number, year=(number+1991))
            for i, wood in enumerate(['Ciliegio', 'Ginepro', 'Gelso']):
                id = 'BAR' + str(number) + str(i)
                Barrel.objects.create(id=id, barrel_set=barset, wood_type=wood,
                                      capability=70)

    def test_set_get_1(self):
        response = self.client.get('/api/operation/prelievo/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get('/api/operation/rabbocco/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_set_get_2(self):
        barrels = Barrel.objects.all()
        for barrel in barrels:
            operation = OperationType.objects.get(name="prelievo")
            date = datetime.today().strftime('%Y-%m-%d')
            Operation.objects.create(type=operation, barrel=barrel,
                                     date=date, values={})

        for barrel in barrels[:2]:
            operation = OperationType.objects.get(name="rabbocco")
            date = datetime.today().strftime('%Y-%m-%d')

            Operation.objects.create(type=operation, barrel=barrel,
                                     date=date, values={})

        response = self.client.get('/api/operation/prelievo/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

        response = self.client.get('/api/operation/rabbocco/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_set_post(self):
        data = {
                "type": "rabbocco",
                "barrel": 'BAR11',
                "date": datetime.today().strftime('%Y-%m-%d'),
                "values": "{}"
                }
        response = self.client.post('/api/operation/prelievo/', data=data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 0)

        response = self.client.post('/api/operation/rabbocco/', data=data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operation.objects.count(), 1)

    def test_detail_get(self):
        operation = OperationType.objects.get(name="rabbocco")
        barrel = Barrel.objects.get(pk='BAR11')
        date = datetime.today().strftime('%Y-%m-%d')
        instance = Operation.objects.create(type=operation,
                                            barrel=barrel,
                                            date=date,
                                            values=[])
        response = self.client.get('/api/operation/rabbocco/{}/'.format(instance.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['barrel'], 'BAR11')
        self.assertEqual(response.data['date'], date)
        self.assertEqual(response.data['values'], [])

    def test_put(self):
        operation = OperationType.objects.get(name="rabbocco")
        barrel = Barrel.objects.get(pk='BAR11')
        date = datetime.today().strftime('%Y-%m-%d')
        instance = Operation.objects.create(type=operation,
                                            barrel=barrel,
                                            date=date,
                                            values=[])

        data = {
                "type": "rabbocco",
                "barrel": 'BAR11',
                "date": datetime.today().strftime('%Y-%m-%d'),
                "values": {'bar_dest': 3, 'quantity': 10}
                }
        response = self.client.put('/api/operation/rabbocco/{}/'.format(instance.id),
                                   data=data, format='json')

        updated_instance = Operation.objects.get(pk=instance.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_instance.type.name, data['type'])
        self.assertEqual(updated_instance.barrel.id, data['barrel'])
        self.assertEqual(str(updated_instance.date), data['date'])
        self.assertEqual(updated_instance.values, data['values'])

    def test_delete(self):
        barrel = Barrel.objects.get(pk='BAR11')
        operation = OperationType.objects.get(name="rabbocco")
        instance = Operation.objects.create(barrel=barrel,
                                            type=operation,
                                            date=datetime.today().strftime('%Y-%m-%d'),
                                            values=[])

        response = self.client.delete('/api/operation/rabbocco/{}/'.format(instance.id),
                                      format='json')

        operations = Operation.objects.filter(pk=instance.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(operations), 0)
