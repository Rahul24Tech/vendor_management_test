from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from drf_yasg.utils import swagger_auto_schema
from django.db import models
from drf_yasg import openapi

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a vendor's performance metrics",
        responses={200: openapi.Response('Vendor performance metrics', VendorSerializer)}
    )
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(data)

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.update_vendor_metrics(response.data['vendor'])
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.update_vendor_metrics(response.data['vendor'])
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        vendor_id = instance.vendor_id
        response = super().destroy(request, *args, **kwargs)
        self.update_vendor_metrics(vendor_id)
        return response

    def update_vendor_metrics(self, vendor_id):
        vendor = Vendor.objects.get(id=vendor_id)
        pos = PurchaseOrder.objects.filter(vendor=vendor)

        if pos.exists():
            completed_pos = pos.filter(status='completed')
            on_time_deliveries = completed_pos.filter(delivery_date__lte=models.F('delivery_date')).count()
            on_time_delivery_rate = on_time_deliveries / completed_pos.count() if completed_pos.exists() else 0

            quality_ratings = completed_pos.filter(quality_rating__isnull=False).values_list('quality_rating', flat=True)
            quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

            response_times = pos.filter(acknowledgment_date__isnull=False).annotate(
                response_time=models.ExpressionWrapper(
                    models.F('acknowledgment_date') - models.F('issue_date'),
                    output_field=models.DurationField()
                )
            ).values_list('response_time', flat=True)
            average_response_time = sum(response_times, timedelta()) / len(response_times) if response_times else timedelta()

            fulfillment_rate = completed_pos.count() / pos.count() if pos.exists() else 0

            vendor.on_time_delivery_rate = on_time_delivery_rate
            vendor.quality_rating_avg = quality_rating_avg
            vendor.average_response_time = average_response_time.total_seconds() / 3600 if response_times else 0
            vendor.fulfillment_rate = fulfillment_rate
            vendor.save()
