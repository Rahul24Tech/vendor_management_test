from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vendor, PurchaseOrder

class VendorTests(APITestCase):
    def setUp(self):
        self.vendor_data = {
            "name": "Vendor1",
            "contact_details": "Contact details",
            "address": "Vendor address",
            "vendor_code": "V001"
        }
        self.vendor = Vendor.objects.create(**self.vendor_data)

    def test_create_vendor(self):
        response = self.client.post(reverse('vendor-list'), self.vendor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_vendors(self):
        response = self.client.get(reverse('vendor-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_vendor(self):
        response = self.client.get(reverse('vendor-detail', args=[self.vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        updated_data = {
            "name": "Vendor1 Updated",
            "contact_details": "Updated contact details",
            "address": "Updated address",
            "vendor_code": "V001"
        }
        response = self.client.put(reverse('vendor-detail', args=[self.vendor.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.name, updated_data['name'])

    def test_delete_vendor(self):
        response = self.client.delete(reverse('vendor-detail', args=[self.vendor.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)

class PurchaseOrderTests(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Vendor1",
            contact_details="Contact details",
            address="Vendor address",
            vendor_code="V001"
        )
        self.po_data = {
            "po_number": "PO001",
            "vendor": self.vendor.id,
            "order_date": "2024-01-01T00:00:00Z",
            "delivery_date": "2024-02-01T00:00:00Z",
            "items": {"item1": 10, "item2": 20},
            "quantity": 30,
            "status": "pending",
            "issue_date": "2024-01-01T00:00:00Z"
        }
        self.purchase_order = PurchaseOrder.objects.create(**self.po_data)

    def test_create_purchase_order(self):
        response = self.client.post(reverse('purchaseorder-list'), self.po_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_purchase_orders(self):
        response = self.client.get(reverse('purchaseorder-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_purchase_order(self):
        response = self.client.get(reverse('purchaseorder-detail', args=[self.purchase_order.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        updated_data = {
            "po_number": "PO001",
            "vendor": self.vendor.id,
            "order_date": "2024-01-01T00:00:00Z",
            "delivery_date": "2024-02-01T00:00:00Z",
            "items": {"item1": 15, "item2": 25},
            "quantity": 40,
            "status": "completed",
            "issue_date": "2024-01-01T00:00:00Z"
        }
        response = self.client.put(reverse('purchaseorder-detail', args=[self.purchase_order.id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.purchase_order.refresh_from_db()
        self.assertEqual(self.purchase_order.status, updated_data['status'])

    def test_delete_purchase_order(self):
        response = self.client.delete(reverse('purchaseorder-detail', args=[self.purchase_order.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)
