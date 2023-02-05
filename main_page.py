import streamlit as st
from PIL import Image
import pandas as pd
st.set_page_config(page_title="Aasaan Checkout Price Calculator", page_icon=":tada:", layout="wide")

#Load Assets
#aasaan_logo = Image.open("../Images/aasaan_logo.png")

#---Functions---
#Prepaid Aasaan Price Calculation
def aasaan_prepaid(plan):
    if plan == 'Quarterly':
        return 60000
    elif plan =="Half-yearly":
        return 50000
    elif plan=="Yearly":
        return 35000

#Postpaid Aasaan Base Percentage Price Calculation
class AasaanPostPaidBasePriceCalculation:
    def __init__(self,txn_details,base_details,no_of_slabs):
       self.txn_details = txn_details
       self.base_details = base_details  
       self.no_of_slabs = no_of_slabs  
    
    def aasaan_postpaid_base_price(self):
        price = float(self.txn_details[0])*float(self.base_details[0])
        if(int(self.no_of_slabs)>1):
            for i in range(1, int(self.no_of_slabs)):
                price = price + (float(self.txn_details[i])-float(self.txn_details[i-1]))*float(self.base_details[i])
        price = 12*price
        return price 
        
            

#Postpaid Aasaan Base Price Price Calculation
class AasaanPostPaidBasePercCalculation:
    def __init__(self,txn_details,base_details,aov,no_of_slabs):
       self.txn_details = txn_details
       self.base_details = base_details  
       self.aov = aov
       self.no_of_slabs = no_of_slabs  
    
    def aasaan_postpaid_base_perc(self):
        price = float(self.txn_details[0])*float(self.base_details[0])*0.01*float(self.aov)
        if(int(self.no_of_slabs)>1):
            for i in range(1, int(self.no_of_slabs)):
                price = price + (int(self.txn_details[i])-int(self.txn_details[i-1]))*float(self.base_details[i])*0.01*float(self.aov)
        price = 12*price
        return price


class CompetitorPriceCalculation:
    def __init__(self, txn, AOV):
        self.txn = txn
        self.AOV = AOV

    #Xpresslane Price Calculation
    def xpresslane_price(self):
        xpresslane_txn_perc = 0.8
        return round(12*self.txn*self.AOV*xpresslane_txn_perc*0.01,2)

    #Nimbl Price Calculation
    def nimbl_price(self):
        nimbl_txn_perc = 2.1
        return rounnd(12*self.txn*self.AOV*nimbl_txn_perc*0.01, 2)

    #GoKwik Price Calculation
    def gokwik_price(self):
        gokwik_txn_perc = 2.3
        min_gaurantee_fee = 15000
        return round(12*max(min_gaurantee_fee, self.txn*self.AOV*gokwik_txn_perc*0.01),2)

    #Shopflo Price Calculation
    def shopflo_price(self):
        installation_fee = 10000
        monthly_fee = 8223
        shopflo_slab1_txn_perc = 2.5
        shopflo_slab2_txn_perc = 1
        shopflo_slab3_txn_perc = 0.5
        shopflo_slab1 = 500000
        shopflo_slab2 = 6000000
        if self.txn*self.AOV <= shopflo_slab1:
            return round(installation_fee + 12*self.txn*self.AOV*shopflo_slab1_txn_perc*0.01, 2)
        if self.txn*self.AOV > shopflo_slab1 and self.txn*self.AOV <= shopflo_slab2:
            return round(installation_fee + 12*(shopflo_slab1*self.AOV*shopflo_slab1_txn_perc*0.01 + self.txn - shopflo_slab1)*self.AOV*shopflo_slab2_txn_perc*0.01 + 8*monthly_fee,2)
        if self.txn*self.AOV > shopflo_slab2:
            return round(installation_fee + 12*(shopflo_slab1*self.AOV*shopflo_slab1_txn_perc*0.01 + shopflo_slab2*self.AOV*shopflo_slab2_txn_perc*0.01 + (self.txn - shopflo_slab2)*self.AOV*shopflo_slab3_txn_perc*0.01 + 8*monthly_fee), 2) 


#---Function to get comp. dictionary---
def comp_price_dict(monthly_txn, aov,selected_competitors):
    comp_price_calculator = CompetitorPriceCalculation(float(monthly_txn), float(aov))
    if 'Xpresslane' in selected_competitors:
        competitor_prices['Xpresslane'] = comp_price_calculator.xpresslane_price()
    if 'Nimbl' in selected_competitors:
        competitor_prices['Nimbl'] = comp_price_calculator.nimbl_price()
    if 'GoKwik' in selected_competitors:
        competitor_prices['GoKwik'] = comp_price_calculator.gokwik_price()
    if 'Shopflo' in selected_competitors:
        competitor_prices['Shopflo'] =  comp_price_calculator.shopflo_price()
    return competitor_prices

def pricingModelSelector(monthly_txn, aov,txn_nature):
    if aov <= 500:
        if monthly_txn <=200000/12:
            return "Prepaid", 0
        else:
            if txn_nature == "Constant": 
                return "Postpaid Base Percentage",0
            else:
                return "Postpaid Base Percentage",1
    elif aov>500 and aov<=1000:
        if monthly_txn <=40000/12:
            return "Prepaid",0
        else:
            if txn_nature == "Constant": 
                return "Postpaid Base Percentage",0
            else:
                return "Postpaid Base Percentage",1

    elif aov>1000 and aov<=2500:
        if monthly_txn < 30000/12:
            return "Prepaid",0
        else:
            if txn_nature == "Constant": 
                return "Postpaid Base Price",0
            else:
                return "Postpaid Base Price",1
        

    elif aov>2500:
        if monthly_txn < 30000/12:
            return "Prepaid"
        else:
            if txn_nature == "Constant": 
                return "Postpaid Base Price",0
            else:
                return "Postpaid Base Price",1
    



# ---Logo & Heading Section---
#st.markdown("<p style='text-align: center;'><img src='/Users/shubhamsd4/Documents/Work/Aasaan Price Calculator/Images/aasaan_logo.png'></p>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>Aasaan Pricing Calculator</h1>", unsafe_allow_html=True)



#---Intro Section --- 
with st.container():
    st.subheader("Hi there :wave:")
    st.write("Aasaan Checkout Price Calculator is a tool for the Sales Executives (that is you :smiley:) so that you can show our prospective merchants about the price they'd have to pay for the current revenue they're generating and also compare it with Aasaan's competitors to show them we are way better in terms of pricing as well apart from the features :sunglasses:. All you have to do is:")
    st.markdown(
        """
        1. Ask our prospective merchants what their Avg. Order Value and their monthly transactions.
        2. Choose the pricing model and input the pricing details according to the guidelines.
        3. Choose the competitors you want to compare against
        """)

#--Choose Competitor ---
with st.container():
    st.write("---")
    st.subheader("Competitor Comparision")
    competitor_names = ['GoKwik', 'Shopflo','Xpresslane','Nimbl']
    selected_competitors = st.multiselect("Select Competitors to compare with", competitor_names)
    #update_competitor = st.button("Update Competitors")
    competitor_prices = {}


#--Pricing Model Selector---
with st.container():
    st.write("---")
    st.subheader("Pricing Model Selector")  
    
    #Taking the inputs aov,  txn and distribution details for comp. benchmarking
    aov_check = st.text_input("Avg. Order Value (in Rs.)", key="check")
    monthly_txn_check= st.text_input("Avg. Transactions per Month", key="check txn")
    txn_nature = st.radio("Select the nature of the monthly transactions over the year", ["Constant", "Fluctuating"], key="txn_nature_key")

    if aov_check and monthly_txn_check:
        priceModule,isTiered = pricingModelSelector(int(monthly_txn_check), float(aov_check),txn_nature)
    else:
        priceModule = 0

    getPricingModel = st.button("Get Pricing Model", key="getPMButton")


#---Prepaid ---
with st.container():
    st.write("---")
    if priceModule == "Prepaid":
            st.subheader("Prepaid Pricing Model")  
            
            #Taking the inputs aov and txn details for comp. benchmarking
            aov = st.text_input("Avg. Order Value (in Rs.)")
            monthly_txn = st.text_input("Avg. Transactions per Month")

            #Subscription Plan Dropdown 
            subscription_plans_options = ['Quarterly', 'Half-yearly', 'Yearly']
            selected_subscription_plan = st.selectbox("Select the Prepaid Subscription Type", subscription_plans_options, key='prepaid_sub_plan')
            prepaid_button = st.button("Calculate Price")
            
            #Competitor Function Values   
            if aov and monthly_txn:
                competitor_prices = comp_price_dict(monthly_txn, aov,selected_competitors)
            
            if prepaid_button:
                st.metric("Aasaan",aasaan_prepaid(selected_subscription_plan))
                for key in competitor_prices.keys():
                    st.metric(key, competitor_prices[key])
    else:
        st.empty()


    #---Postpaid Base Price---
    if priceModule == "Postpaid Base Price":    
        st.subheader("Postpaid Pricing Model: Base Price")
        if isTiered:
            st.write("Tiered")
            no_of_slabs = st.text_input("Enter number of slabs")
            st.button("Get Slabs")
        else:
            st.write("Non-Tiered")
            no_of_slabs = 1
        aov_bprice = st.text_input("Avg. Order Value (in Rs.)", key="AOV base price")
        max_txn = []
        base_price=[]
        if no_of_slabs:
            if int(no_of_slabs)<=5 and int(no_of_slabs)>0:
                for i in range(int(no_of_slabs)):
                    st.text(f"Slab {i+1}")
                    max_txn.append(st.text_input("Maximum number of transactions per month",key = f"key{i}"))
                    base_price.append(st.text_input("Price per transaction(in Rs.)", key = f"key{i+10}"))
            else:
                st.error("Number of slabs can be from 1-5")
            postpaid_base_price_button = st.button("Calculate Price", key="postpaid base price")

            if postpaid_base_price_button:
                postpaid_base_price_obj = AasaanPostPaidBasePriceCalculation(max_txn, base_price, no_of_slabs)
                postpaid_baseprice_pricing = postpaid_base_price_obj.aasaan_postpaid_base_price()
                st.metric("Aasaan", postpaid_baseprice_pricing)

                monthly_txn_bprice = max(max_txn)
                #st.write(monthly_txn_bprice)
                #Competitor Function Values   
                if aov_bprice and monthly_txn_bprice:
                    competitor_prices = comp_price_dict(monthly_txn_bprice, aov_bprice,selected_competitors)


                for key in competitor_prices.keys():
                    st.metric(key, competitor_prices[key])
    else:
        st.empty()
                
#---Postpaid Base Percentage---

    if priceModule =="Postpaid Base Percentage":    
        st.subheader("Postpaid Pricing Model: Base Percentage")
        if isTiered:
            st.write("Tiered")
            no_of_slabs = st.text_input("Enter number of slabs", key="base percentage")
            st.button("Get Slabs", key="base_perc_key")
        else:
            st.write("Non-Tiered")
            no_of_slabs = 1
        aov_bperc = st.text_input("Avg. Order Value (in Rs.)", key="AOV base percentage")
        max_txn_perc = []
        base_perc=[]
        if no_of_slabs:
            if int(no_of_slabs)<=5 and int(no_of_slabs)>0:
                for i in range(int(no_of_slabs)):
                    st.text(f"Slab {i+1}")
                    max_txn_perc.append(st.text_input("Maximum number of transactions per month",key = f"key{i+20}"))
                    base_perc.append(st.text_input("Percentage per transaction amount(in %)", key = f"key{i+50}"))
            else:
                st.error("Number of slabs can be from 1-5")
           
            postpaid_base_perc_button = st.button("Calculate Price", key="postpaid base perc")

            if postpaid_base_perc_button and aov_bperc:
                postpaid_base_perc_obj = AasaanPostPaidBasePercCalculation(max_txn_perc, base_perc, aov_bperc, no_of_slabs)
                postpaid_baseperc_pricing = postpaid_base_perc_obj.aasaan_postpaid_base_perc()
                st.metric("Aasaan", postpaid_baseperc_pricing)

                monthly_txn_bperc = max(max_txn_perc)
                
                #Competitor Function Values   
                if aov_bperc and monthly_txn_bperc:
                    competitor_prices_bperc = comp_price_dict(monthly_txn_bperc, aov_bperc, selected_competitors)

                for key in competitor_prices_bperc.keys():
                    st.metric(key, competitor_prices_bperc[key])  
    else:
        st.empty()

            

