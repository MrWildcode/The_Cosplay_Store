from django.db.models import Avg

from store.models import UserProductRelation


def set_rating(product_object):
   aggregated_rating = UserProductRelation.objects.filter(product=product_object).aggregate(
       rating=Avg('rate')).get('rating')

   product_object.rating = aggregated_rating
   product_object.save()