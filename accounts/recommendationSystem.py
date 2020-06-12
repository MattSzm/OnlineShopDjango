from django.conf import settings
from productsMaintain.models import Product


class RecommendationEngine:
    def __init__(self, request):
        self.session = request.session
        recommended = self.session.get(settings.RECOMMENDATION_SESSION_ID)
        if not recommended:
            recommended = []
        self.recommended = self.session[settings.RECOMMENDATION_SESSION_ID] = recommended

    def addSignle(self, product_id):
        if len(self.recommended) >= 3:
            self.recommended.pop(0)
        if not product_id in self.recommended:
            self.recommended.append(product_id)

    def clear(self):
        del self.session[settings.RECOMMENDATION_SESSION_ID]

    def __iter__(self):
        recommendedCopy = self.recommended.copy()
        for singleId in recommendedCopy:
            singleProduct = Product.objects.get(id=singleId)
            if singleProduct.available:
                yield singleProduct

    def removeSingle(self, product_id):
        if product_id in self.recommended:
            self.recommended.remove(product_id)

    @property
    def exist(self):
        if len(self.recommended)>0:
            return True
        return False