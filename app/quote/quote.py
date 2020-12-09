# import numpy as np

from core.models import GrowthRateByAgeEducation, UnemploymentByAgeGroup,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup,User,
                        GetHikeByEducation
from django.core.exceptions import FieldError
import math
class Prais:
    #class variables
    number_of_records=0
    growth_rate=0.04
    lower_threshold=2000
    upper_cap=2
    servicing_fee_perc=0.05

    job_loss_from=0
    job_loss_months=0


    intermediate_income_change_perc = 0
    month_of_income_change=0

    def __init__(self):
        #following variables will be defined by user
        Prais.number_of_records+=1


    def GetGrowthRate(self,age,degree,profession,industry):
        """
        This method predicts growth rate based on age degree, profession,
        industry.
        """
        try:
            growth_rate = GrowthRateByAgeEducation.objects.values_list(degree,
                                                        flat=True).get(age=age)

        except FieldError:
            return "NA"

        except :
            return "NA"

        return growth_rate

    def GetTargetedReturn(self,term):
        """This method returns the list of targeted return pricing for
        respective term"""
        try:
            targeted_return = Pricing.objectsvalues_list(targeted_cagr,
                                                        flat=True).get(term=term)

        except FieldError:
            return ["NA"]

        except :
            return ["NA"]

        return targeted_return

    def GetEmploymentDuration(self,age):
        """
        The method returns the employment duartion for the age supplied.
        Assumption-New employment starts at the age supplied.
        """
        try:
            age=int(age)
            # Find age group category
            if age>=65:
                age_group="65 and above"
            elif age>=55:
                age_group="55-64"
            elif age>=45:
                age_group="45-54"
            elif age>=35:
                age_group="35-44"
            elif age>=25:

                age_group="25-34"
            else:
                age_group="20-24"
            # Check if agegroup category exist and
            employment_duration = EmploymentDurationByAgeGroup.objects.values_list(
                                'duration',flat=True).get(age_group=age_group)
        except :
            raise Exception("Error- please check data type of age.")
        return employment_duration

    def GetUemploymentByAgeGroup(self,age,method):
        """The method returns the possible average unemployment duration for the
            respective agegroup.
        """
        try:
            age=int(age)
            # Find age group category
            if age>=65:
                age_group="65 and above"
            elif age>=55:
                age_group="55-64"
            elif age>=45:
                age_group="45-54"
            elif age>=35:
                age_group="35-44"
            elif age>=25:
                age_group="25-34"
            else:
                age_group="20-24"
            # selected method of unemployment duration value
            if method=="Mean":
                duration="mean_duration"
            else:
                duration="median_duration"
            # Check if agegroup category exist and
            unemployment_duration = UnemploymentByAgeGroup.objects.values_list(
                                    duration,flat=True).get(age_group=age_group)
        except :
            return "Error- please check data type of age."
        return float(unemployment_duration)

    def GetUnemploymentLists(self,age,term,method="Median",industry="NA",profession="NA"):
        """
        The method returns the list of number of unemployed months after every
        unemployment start month.
        Assumption- New employment starts after end of unemployment months.
        Values
        databy(Depreicated):"ByAge" (by defualt),"OverallAvg","ByIndustry"
                            ,"ByProfession".
        method:"Median" (By default), "Mean".
        """

        unemployment_start_list=[]
        unemployment_months_list=[]
        term=int(term)*12 # convert term year to no. months
        age=age
        i=0 # i represent number of a term month count
        # calculate 1st mployemnt duartion in months
        # print(age)
        while i<= term:

            employment_dur = int(round(self.GetEmploymentDuration(age),0)*12)
            i = i + employment_dur
            # check if i is less than total term months. if yes append lists
            if i<=term:
                unemployment_start_list.append(i+1)
                age = age + math.floor(employment_dur/12)

                unemployment_dur = int(math.ceil(self.GetUemploymentByAgeGroup(
                                                        age,method)/4))
                i = i + unemployment_dur
                # age = age+ math.floor(unemployment_dur/12)
                unemployment_months_list.append(unemployment_dur)
                term = term+unemployment_dur
    # except:
    #         return ['NA'],['NA'],'NA'

        return unemployment_start_list,unemployment_months_list,term

    def GetHikeByEducation(self,degree):
        """This method returns the list of targeted return pricing for
        respective term"""
        try:
            hike = GetHikeByEducation.objectsvalues_list('hike',
                                                flat=True).get(degree=degree)

        except FieldError:
            raise Exception(Please check spelling of degree entered)

        except :
            raise Exception(Please check spelling of degree entered)

        return hike

    def GetQuote(self,funding_amount,current_income,growth_rate,
                                    unemployment_start_list,term_month,age,
                                    unemployment_months_list,targeted_return):
        """
        This method figures out best ISA rate for given ISA term and growth_rate.
        funding_amount: Amount to be refinance.
        current_income: Starting income of a candidate.
        growth_rate: Predicted Income growth rate.
        unemployment_start_month_list: List comparising of Starting month of
                                        predicted unemployment .
        unemployment_number_of_month_list: List comparising of number of months
                                            of predicted unemployment .
        term: ISA term (in years)
        targeted_return: The CAGR rate for given term.
        """
        #Method variable initialization
        income=current_income

        incubation_month=0
        self_equity_perc=0

        if self_equity_amount != 0:
            incubation_month=1
            self_equity_perc=self_equity_amount/loan_balance

        term_month=term_month+incubation_month+self.job_loss_months

        #Method Counters
        count=1
        self_equity=0
        sum_self_equity=0
        sum_income_share=0
        sum_servicing_fee=0
        isa_result={}
        for i in range(1,term_month+1,1):

            if i == self.month_of_income_change:
                if i < self.job_loss_from or i > self.job_loss_to:
                    income = income * (1 + self.intermediate_income_change_perc)
                    count=1

            if count==13:
                income=income * (1 + self.growth_rate)
                count=1

            monthly_income=round(income/12,2)

            if i >= self.job_loss_from and i <= self.job_loss_to:
                monthly_income=0
                count=1
            if monthly_income<=self.lower_threshold:
                monthly_income=0

            income_share = round(monthly_income * isa_rate,2)
            servicing_fee = round(income_share * self.servicing_fee_perc,2)
            net_income_share = round(income_share - servicing_fee,2)
            if i==1:
                isa_result['1st_payment']=income_share

            if i > incubation_month:
                self_equity = round(net_income_share * self_equity_perc,2)

            #Sum of shares
            sum_income_share = round(sum_income_share + income_share,2)
            sum_self_equity = round(sum_self_equity + self_equity,2)
            sum_servicing_fee = round(sum_servicing_fee+servicing_fee,2)
            # print('i={}'.format(i) +' '+'income_share={}'.format(income_share)+' '+'servicing_fee={}'.format(servicing_fee)+' '+'net_income_share={}'.format(net_income_share)+' '+'self_equity={}'.format(self_equity))
            count+=1

        net_amount_shared=sum_income_share - sum_self_equity +self_equity_amount
        apr=np.rate(term_month,net_amount_shared/term_month,-loan_balance,0)*12
        isa_result['last_payment']=income_share
        isa_result['total_payment']=sum_income_share+self_equity_amount
        isa_result['cashback']=sum_self_equity
        isa_result['net_payment']=net_amount_shared
        isa_result['apr']=apr

        return isa_result

    def Quotes(self,funding_amount,current_income,age,degree,industry="NA",profession="NA",method="Median"):
        """This method returns quotes for all possible terms.
            method determins if data used for unemployment is Mean or Median.
        """
        #Initiate quote dictionary
        quote_dict={}
        age_limit = 60
        growth_rate = self.GetGrowthRate(age,degree,profession,industry)
        hike = self.GetHikeByEducation(degree)
        terms_list = [5,7,10,12,15]

        for term in term_list:

            targeted_cagr = GetTargetedReturn(term)

            unemployment_start_list,unemployment_months_list,term_month = self.GetUnemploymentLists(age,
                                                term,method="Median",industry="NA",profession="NA")
            quote_for_term = self.GetQuote(funding_amount,current_income,growth_rate,
                                            unemployment_start_list,term_month,age,
                                            unemployment_months_list,targeted_return)

            if (not 'error' in quote_for_term) and (age + term != age_limit):
                qoute_dict[term] = quote_for_term

        return quote_dict
