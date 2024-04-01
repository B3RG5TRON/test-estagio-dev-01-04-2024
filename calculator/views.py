from django.shortcuts import render, redirect
from .models import Consumer

def list_consumers(request):
    consumers = Consumer.objects.all()  # Fetch all consumers
    savings_data = []
    for consumer in consumers:
        monthly_savings = (consumer.distributor_tax * consumer.consumption * (1 - consumer.discount_rule.discount_value)
                          - consumer.distributor_tax * consumer.consumption)
        annual_savings = monthly_savings * 12
        applied_discount = consumer.discount_rule.discount
        coverage = consumer.discount_rule.coverage
        savings_data.append({
            'monthly_savings': round(monthly_savings, 2),
            'annual_savings': round(annual_savings, 2),
            'applied_discount': applied_discount,
            'coverage': coverage
        })

    context = {'consumers': consumers, 'savings_data': savings_data}
    return render(request, 'calculator/list.html', context)



