from django.contrib import admin

from .models import Offer, OffersMicroserviceToken, Product

admin.site.register(Offer)
admin.site.register(Product)
admin.site.register(OffersMicroserviceToken)
