# import numpy as np
from core import models
from core.models import  UnemploymentByAgeGroup,GrowthRateByAgeEducation,\
                        UnemploymentByIndustry,UnemploymentByOccupation,\
                        Pricing,EmploymentDurationByAgeGroup,User,\
                        PraisParameterCap,HikesByEducation
from django.core.exceptions import FieldError
import math

class Prais:
    #class variables
    number_of_records = 0

    def __init__(self):
        # #following variables will be defined by user

        Prais.number_of_records+=1
    def GetPraisFixedPara(self):
        """This method returns ISA fixed paramters"""
        isa_para = PraisParameterCap.objects.all().order_by('-updated_date')[0]
        return isa_para

    def GetGrowthRate(self,age,degree,profession,industry):
        """
        This method predicts growth rate based on age degree, profession,
        industry.
        """
        try:
            growth_rate = GrowthRateByAgeEducation.objects.values_list(
                                                    degree,flat=True).get(age=age)
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

        return unemployment_start_list,unemployment_months_list

    def GetHikeByEducation(self,degree):
        """This method returns the list of targeted return pricing for
        respective term"""
        try:
            hike = GetHikeByEducation.objectsvalues_list('hike',
                                                flat=True).get(degree=degree)

        except FieldError:
            raise Exception("Please check spelling of degree entered")

        except :
            raise Exception("Please check spelling of degree entered")

        return hike

    def GetQuote(self,funding_amount,current_income,term,age,growth_rate,hike,unemployment_start_list,unemployment_months_list,targeted_return):
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
        # Inistialized blank results dictionary
        isa_result={}
        #Method variable initialization
        # Get all the fixed parameters for an ISA
        para = self.GetPraisFixedPara()
        processing_fee = float(para.isa_processing_fee)
        servicing_fee = float(para.isa_servicing_fee)
        sales_charge = float(para.isa_sales_charge)
        minimum_self_equity_perc = float(para.minimum_self_equity_perc)
        max_minimum_self_equity = float(para.max_minimum_self_equity)
        income_lower_limit = float(para.annual_lower_income)
        processing_fee_cap = float(para.isa_processing_fee_cap)
        buyout_servicing_fee = float(para.buyout_servicing_fee)
        isp_age_factor = float(para.isp_age_factor)
        servicing_fee = float(para.isa_servicing_fee)

        # Calculate minimum self equity amount required
        min_self_equity = funding_amount * minimum_self_equity_perc
        if min_self_equity > max_minimum_self_equity:
            min_self_equity = max_minimum_self_equity
        isa_result['min_self_equity'] = min_self_equity

        # Calculate ISA processing fee
        isa_processing_fee = funding_amount * processing_fee
        if isa_processing_fee > processing_fee_cap:
            isa_processing_fee = processing_fee_cap
        isa_result['processing_fee'] = isa_processing_fee
        # If uneemployment list is empty due to term size and candidate age,
        # following setup will avoid list index error

        len_unemp_list = len(unemployment_start_list)
        if len_unemp_list == 0:
            unemployment_months_list.append(0)
            unemployment_start_list.append(0)

        # Add formula to get a baseline result and compute from there.
        # i=1 => 1/10000
        isp_start=100
        for isp_int in range(isp_start,2000,1):
            isp = isp_int/10000
            income = current_income
            term_month = term * 12
            # min_self_equity_amount = min_self_equity
            isa_processing_fee_amount = isa_processing_fee
            #Sum initiation with zero
            self_equity = 0
            self_equity_perc = 0
            sum_self_equity = 0
            sum_income_share = 0
            sum_servicing_fee = 0
            sum_incubation_amount = 0
            incubation_months = 0
            # Method counters
            count = 1
            i=1
            unemp_no = 0
            while i <= term_month+1:
                # Unemployment month count and  seeting elligible income 0
                if (i >= unemployment_start_list[unemp_no]) \
                    and (i < unemployment_start_list[unemp_no] \
                        + unemployment_months_list[unemp_no]):

                        if i == unemployment_start_list[unemp_no]:
                            income_temp = income

                        income = 0
                        term_month += 1

                # Income raise/hike after new employment
                if i == unemployment_start_list[unemp_no] \
                    + unemployment_months_list[unemp_no]:
                    income = income_temp * (1 + hike)
                    count=1

                # Annual income growth
                if count==13:
                    income=income * (1 + growth_rate)
                    count=1

                monthly_income=round(income/12,2)

                # Set monthly income zero if income drops below lower limit
                if monthly_income <= income_lower_limit/12:
                    monthly_income = 0
                    term_month += 1

                # calculate monthly income shares
                income_share = round(monthly_income * isp,2)

                # Substract processing fee 1st from  income share agreement
                if isa_processing_fee_amount > income_share:
                    isa_processing_fee_amount -= income_share
                    income_share = 0
                    term_month +=1
                else:
                    income_share -= isa_processing_fee_amount
                    isa_processing_fee = 0

                servicing_fee_share = round(income_share * servicing_fee,2)
                net_income_share = round(income_share - servicing_fee_share,2)


                if i==1:
                    isa_result['first_payment']=income_share


                # Calculate incubation months and self equity share
                if sum_incubation_amount < min_self_equity:
                    sum_incubation_amount += net_income_share
                    self_equity_perc = sum_incubation_amount / funding_amount
                    term_month += 1
                    incubation_months +=1
                else:
                    # Calculate self equity share once incuabtion is finished
                    self_equity = round(net_income_share * self_equity_perc,2)

                #Sum of shares
                sum_income_share = round(sum_income_share + income_share,2)
                sum_self_equity = round(sum_self_equity + self_equity,2)
                sum_servicing_fee = round(sum_servicing_fee + servicing_fee_share,2)
                count += 1
                i += 1

            sum_investor_share = sum_income_share - sum_self_equity - sum_servicing_fee
            cagr = (sum_investor_share / (funding_amount * (1+sales_charge)))**(12/term_month)-1

            if cagr >= targeted_return:
                break


        isa_result['last_payment']=income_share
        isa_result['total_payment']=sum_income_share
        isa_result['cashback']=sum_self_equity
        isa_result['term']=term
        isa_result['incubation_months']=incubation_months
        isa_result['income_share']=isp
        isa_result['self_equity_perc_by_incubation']=round(self_equity_perc,4)

        # final check if isp * term not crosses multiplication factor (2.5)
        if isp_age_factor <= isp * term:
            isa_result['error'] = 'Quote crosses ISA Age multiple'
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

            if term + age < 60:

                targeted_cagr = GetTargetedReturn(term)

                unemployment_start_list,unemployment_months_list = self.GetUnemploymentLists(age,
                                                    term,method="Median",industry="NA",profession="NA")
                quote_for_term = self.GetQuote(funding_amount,current_income,growth_rate,
                                                term,age,targeted_return,hike,
                                                unemployment_start_list,
                                                unemployment_months_list)

                if (not 'error' in quote_for_term) and (age + term != age_limit):
                    qoute_dict[term] = quote_for_term

        return quote_dict
