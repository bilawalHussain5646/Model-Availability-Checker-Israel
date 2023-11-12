import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import tkinter.font as tkFont
import threading
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


def InfiniteScrolling(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(10)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height



def Traklin_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Traklin'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    model_links :list = []
                    driver.get(dyno_link)
                    # # Get scroll height
                    InfiniteScrolling(driver)
                    
                    # driver.get(dyno_link)
                    # time.sleep(5)
                    ids = driver.find_element(By.ID,"cph_main_div_cat_contents_wrap_all")

                    all_divs  = ids.find_elements(By.CLASS_NAME, "prod_name")
                    # print(len(all_divs))
                    # Compare product name with model name 
                    for div in all_divs:
                        title = div
                        model_link = title.get_attribute('href')
                        title_value = title.text
                        model_id = title_value
                        print(model_id)
                        check_once = 1
                        # Save this model id in the list and use it later 
                        # 
                        model_ids.append(model_id)
                        model_links.append(model_link)



                total_models = len(model_ids)
                counter = 0
                mdlinks = 0 
                for each_model in model_ids: 
                    if each_model.find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "Traklin": "o",
                                "Product Link": model_links[mdlinks]
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1
                    mdlinks+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "Traklin": "x",
                            "Product Link": ""
      
                    },ignore_index=True)
                    print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Traklin")
        
def Payngo_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Payngo'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    # Dont touch this
                    # dyno_link = df_link["Links"].iloc[0]
                    # 
                    # print(dyno_link)
           
                    model_ids :list = []
                    driver.get("https://www.payngo.co.il/instantsearchplus/result/?q="+models)
                    
                    # # Get scroll height
                    # InfiniteScrolling(driver)
                    
                    # driver.get(dyno_link)
                    # time.sleep(5)
                    
                    time.sleep(5)
                 
                    all_divs  = driver.find_element(By.ID, "isp_results_summary_total_results").text
                    if int(all_divs) > 0:
                        product_link = driver.find_element(By.CSS_SELECTOR,".isp_product_image_href").get_attribute("href")
                
                        output_df = output_df.append({
                                "Model":models,
                                "Payngo": "o",
                                "Product link": product_link
                        },ignore_index=True)
                        print(models,"Found")
                        # break
                    # counter+=1

                # if counter == total_models:
                    else:
                        output_df = output_df.append({
                                "Model":models,
                                "Payngo": "x",
                                "Product link": ""
        
                        },ignore_index=True)
                        print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Payngo")
 

def KSP_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','KSP'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    model_link : list = []

                    driver.get(dyno_link)
                    # # Get scroll height
                    InfiniteScrolling(driver)
                    
                    # driver.get(dyno_link)
                    time.sleep(5)
                    all_divs  = driver.find_elements(By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-subtitle1")
                    # print(len(all_divs))
                    # Compare product name with model name 
                    for div in all_divs:
                        product_link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                        model_id = div.text
                        print(model_id)
                        check_once = 1
                        # Save this model id in the list and use it later 
                        # 
                        model_ids.append(model_id)
                        model_link.append(product_link)


                
                total_models = len(model_ids)
                counter = 0
                mdl_link = 0 
                for each_model in model_ids: 
                    print(each_model)
                    if each_model.find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "KSP": "o",
                                "Product link": model_link[mdl_link]
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1
                    mdl_link +=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "KSP": "x",
                            "Product link": ""
      
                    },ignore_index=True)
                    print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="KSP")
 

def Traklin_WebT20(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Traklin',"Old Models"])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    driver.get(dyno_link)
                    # # Get scroll height
                    time.sleep(5)
                    # InfiniteScrolling(driver)
                    
                    # driver.get(dyno_link)
                    # time.sleep(5)
                    ids = driver.find_element(By.CSS_SELECTOR,".div_cat_contents_wrap_all")

                    all_divs  = ids.find_elements(By.CLASS_NAME, "prod_name")
                    # print(len(all_divs))
                    # Compare product name with model name 
                    x=0
                    for div in all_divs:
                        if div.text.find("LG") != -1:
                            title = div
                            title_value = title.text
                            model_id = title_value
                            print(model_id)
                            check_once = 1
                            # Save this model id in the list and use it later 
                            # 
                            model_ids.append(model_id)
                        x+=1
                        if x>20:
                            break


                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if each_model.find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "Traklin": "o"
                                ,"Old Models": total_models
                                
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "Traklin": "x"
                            ,"Old Models": total_models
      
                    },ignore_index=True)
                    print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="TraklinTop20")
        
def Payngo_WebT20(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Payngo',"Old Models"])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    driver.get(dyno_link)
                    
                    # # Get scroll height
                    # InfiniteScrolling(driver)
                    
                    # driver.get(dyno_link)
                    # time.sleep(5)
                    
                    time.sleep(5)
                 
                    all_divs  = driver.find_elements(By.CSS_SELECTOR, ".isp_grid_product")
                    # print(len(all_divs))
                    # Compare product name with model name 
                    x=0
                    for div in all_divs:
                        
                                title = div.find_element(By.CSS_SELECTOR,".isp_product_title")
                                # title.text
                                if title.text.find("LG") != -1:
                                    title_value = title.text
                                    model_id = title_value
                                    print(model_id)
                                    check_once = 1
                                    # Save this model id in the list and use it later 
                                    # 
                                    model_ids.append(model_id)
                                x+=1
                                if x>20:
                                    break


                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if each_model.find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "Payngo": "o"
                                ,"Old Models": total_models
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "Payngo": "x"
                            ,"Old Models": total_models
      
                    },ignore_index=True)
                    print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="PayngoTop20")
 

def KSP_WebT20(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','KSP',"Old Models"])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    driver.get(dyno_link)
                    time.sleep(5)
                    # # Get scroll height
                    # InfiniteScrolling(driver)
                    
                    # driver.get(dyno_link)
                    # time.sleep(5)
                    all_divs  = driver.find_elements(By.CSS_SELECTOR, ".MuiTypography-root.MuiTypography-subtitle1")
                    # print(len(all_divs))
                    # Compare product name with model name 
                    x=0
                    for div in all_divs:
                        if div.text.find("LG") != -1:
                            model_id = div.text
                            print(model_id)
                            check_once = 1
                            # Save this model id in the list and use it later 
                            # 
                            model_ids.append(model_id)

                        x+=1
                        if x>20:
                            break    


                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if each_model.find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "KSP": "o"
                                ,"Old Models": total_models
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "KSP": "x"
                            ,"Old Models": total_models
                    },ignore_index=True)
                    print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="KSPTop20")
 


def Run_Traklin():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Traklin")
    # LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Traklin_Web(driver,list_of_categories,data,Sharaf_DG)
    
  

def Run_Payngo():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Payngo")
    # LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Payngo_Web(driver,list_of_categories,data,Sharaf_DG)
 
        
def Run_KSP():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="KSP")
    # LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    KSP_Web(driver,list_of_categories,data,Sharaf_DG)
 
def Run_TraklinT20():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="TraklinTop20")
    # LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Traklin_WebT20(driver,list_of_categories,data,Sharaf_DG)
    
  

def Run_PayngoT20():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="PayngoTop20")
    # LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Payngo_WebT20(driver,list_of_categories,data,Sharaf_DG)
 
        
def Run_KSPT20():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="KSPTop20")
    # LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    KSP_WebT20(driver,list_of_categories,data,Sharaf_DG)
 

        
            
                    
         

# Main App 
class App:

    def __init__(self, root):
        #setting title
        root.title("Israel Model Check")
        ft = tkFont.Font(family='Arial Narrow',size=13)
        #setting window size
        width=640
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg='black')

        ClickBtnLabel=tk.Label(root)
       
      
        
        ClickBtnLabel["font"] = ft
        
        ClickBtnLabel["justify"] = "center"
        ClickBtnLabel["text"] = "Israel Model Check"
        ClickBtnLabel["bg"] = "black"
        ClickBtnLabel["fg"] = "white"
        ClickBtnLabel.place(x=120,y=190,width=150,height=70)
    

        
        Lulu=tk.Button(root)
        Lulu["anchor"] = "center"
        Lulu["bg"] = "#009841"
        Lulu["borderwidth"] = "0px"
        
        Lulu["font"] = ft
        Lulu["fg"] = "#ffffff"
        Lulu["justify"] = "center"
        Lulu["text"] = "START"
        Lulu["relief"] = "raised"
        Lulu.place(x=375,y=190,width=150,height=70)
        Lulu["command"] = self.start_func




  

    def ClickRun(self):

        running_actions = [
            Run_Traklin,          
            Run_Payngo,
            Run_KSP
            # Run_TraklinT20,          
            # Run_PayngoT20,
            # Run_KSPT20
        ]

        thread_list = [threading.Thread(target=func) for func in running_actions]

        # start all the threads
        for thread in thread_list:
            thread.start()

        # wait for all the threads to complete
        for thread in thread_list:
            thread.join()
    
    def start_func(self):
        thread = threading.Thread(target=self.ClickRun)
        thread.start()

    
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


# Run()
