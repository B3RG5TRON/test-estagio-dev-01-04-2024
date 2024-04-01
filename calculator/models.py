from django.db import models


class Consumer(models.Model):
    name = models.CharField("Nome do Consumidor", max_length=128)
    document = models.CharField("Documento(CPF/CNPJ)", max_length=14, unique=True)
    zip_code = models.CharField("CEP", max_length=8, null=True, blank=True)
    city = models.CharField("Cidade", max_length=128)
    state = models.CharField("Estado", max_length=128)
    consumption = models.IntegerField("Consumo(kWh)", blank=True, null=True)
    distributor_tax = models.FloatField(
        "Tarifa da Distribuidora", blank=True, null=True
    )
    discount_rule = models.ForeignKey(DiscountRules, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def calculate_savings(self):
        if not self.consumption or not self.distributor_tax or not self.discount_rule:
                return 0, 0, 0, 0

        average_consumption = self.consumption / 3

  # Get discount rule details
        discount_rule = self.discount_rule
        discount_value = discount_rule.discount
        coverage = discount_rule.coverage

  # Apply additional logic based on consumption range and consumer type
        if self.consumer_type == Consumer.RESIDENTIAL:
            if average_consumption < 10000:
                discount_value = 0.18
            elif average_consumption <= 20000:
                discount_value = 0.22
            else:
                discount_value = 0.25
        elif self.consumer_type == Consumer.COMMERCIAL:
            if average_consumption < 10000:
                discount_value = 0.16
            elif average_consumption <= 20000:
                discount_value = 0.18
            else:
                discount_value = 0.22
        else:
            if average_consumption < 10000:
                discount_value = 0.12
            elif average_consumption <= 20000:
                discount_value = 0.15
            else:
                discount_value = 0.18

        monthly_savings = self.distributor_tax * average_consumption * discount_value / 100
        annual_savings = monthly_savings * 12

        return round(annual_savings, 2), round(monthly_savings, 2), discount_value, coverage


# TODO: Create the model DiscountRules below
from django.db import models

class DiscountRules(models.Model):
    consumer_type = models.CharField(max_length=20)
    consumption_range = models.PositiveIntegerField()
    coverage = models.FloatField()
    discount = models.FloatField()

    def __str__(self):
        return f"{self.get_consumer_type_display()} - {self.consumption_range_min} - {self.consumption_range_max if self.consumption_range_max else 'Unlimited'}"

"""Fields:
-> Consumer type  
-> Consumption range
-> Cover value
-> Discount value
The first three fields should be a select with the values provided in the table
defined in the readme of the repository. Discount should be numerical
"""

# TODO: You must populate the consumer table with the data provided in the file consumers.xlsx
#  and associate each one with the correct discount rule
import pandas as pd
def populate_consumers_and_discount_rules(file_path):
    """
    Populates consumers from the provided Excel file and creates corresponding DiscountRules.

    Args:
        file_path (str): Path to the Excel file (consumers.xlsx).
    """
    data = pd.read_excel(file_path)

    for index, row in data.iterrows():

        # Determine discount rule details based on consumer type and average consumption
        coverage = 0
        discount_value = 0

  
        if row['tipo'] == "Residencial":
                if row['Consumo(kWh)'] < 10000:
                    discount_value = 0.18
                    coverage = 0.9
                elif row['Consumo(kWh)'] <= 20000:
                    discount_value = 0.22
                    coverage = 0.95
                else:
                    discount_value = 0.25
                    coverage = 0.99
        elif row['tipo'] == "Comercial":
                if row['Consumo(kWh)'] < 10000:
                    discount_value = 0.16
                    coverage = 0.9
                elif row['Consumo(kWh)'] <= 20000:
                    discount_value = 0.18
                    coverage = 0.95
                else:
                    discount_value = 0.22
                    coverage = 0.99
        else:
                if row['Consumo(kWh)'] < 10000:
                    discount_value = 0.12
                    coverage = 0.9
                elif row['Consumo(kWh)'] <= 20000:
                    discount_value = 0.15
                    coverage = 0.95
                else:
                    discount_value = 0.18
                    coverage = 0.99
    

        monthly_savings = row['Tarifa da Distribuidora'] * row['Consumo(kWh)'] * (1 - discount_value) - row['Tarifa da Distribuidora'] * row['Consumo(kWh)']
    

        # Create DiscountRules object
        discount_rule = DiscountRules.objects.create(
            consumer_type=row['tipo'],
            consumption_range= row['Consumo(kWh)'],  
            coverage=coverage,
            discount=discount_value,
        )
        consumer = Consumer.objects.create(
            name=row['nome'],
            document=row['Documento'],
            city=row['cidade'],
            state=row['estado'],
            consumption=row['Consumo(kWh)'],
            tipo=row['tipo'],
            distributor_tax=row['Tarifa da Distribuidora'],
            discount_rule = discount_rule
        )
    