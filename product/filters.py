import django_filters
from product.models import Product

class ProductFilter(django_filters.FilterSet):
    # min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='price from')
    # max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='price up to')
    # created_after = django_filters.DateFilter(field_name='created', lookup_expr='gte', label='تاریخ از')
    # created_before = django_filters.DateFilter(field_name='created', lookup_expr='lte', label='تاریخ تا')

    # class Meta:
    #     model = Product
    #     fields = ['min_price', 'max_price', 'created_after', 'created_before', 'rating', 'order_by']



    Choices_1 = (
        ('cheap', 'filter by cheapest'),
        ('expensive', 'filter by expensive')
    )

    Choices_2 = (
        ('oldest', 'oldest'),
        ('newest', 'newest')
    )

    Choices_3 = (
        ('more rating', 'more rating'),
        ('least rating', 'least rating')
    )

    unit_price = django_filters.ChoiceFilter(method='price_filter', choices=Choices_1, label='price')
    create = django_filters.ChoiceFilter(method='created_filter', choices=Choices_2, label='creatd')
    ratingg = django_filters.ChoiceFilter(method='rating_filter', choices=Choices_3, label='rating')


    def price_filter(self, queryset, name, value):
        data = 'price' if value == 'filter by cheapest' else '-price'
        return queryset.order_by(data)
    
    def created_filter(self, queryset, name, value):
        data = 'created' if value == 'oldest' else '-created'
        return queryset.order_by(data)
    
    def rating_filter(self, queryset, name, value):
        data = 'rating' if value == 'more rating' else '-rating'
        return queryset.order_by(data)
    