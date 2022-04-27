from django.contrib import admin

from .models import Offer, Product, OffersMicroserviceToken

admin.site.register(Offer)
admin.site.register(Product)
admin.site.register(OffersMicroserviceToken)