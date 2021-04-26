import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime
import time
from datetime import datetime
import random

now = datetime.now()


def init():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    survey_reader_creds = ServiceAccountCredentials.from_json_keyfile_name("creds1.json", scope)
    survey_reader_client = gspread.authorize(survey_reader_creds)
    
    data_getter_creds = ServiceAccountCredentials.from_json_keyfile_name("creds2.json", scope)
    data_getter_client = gspread.authorize(data_getter_creds)
    
    user_writer_creds = ServiceAccountCredentials.from_json_keyfile_name("creds3.json", scope)
    user_writer_client = gspread.authorize(user_writer_creds)
    
    done_putter_creds = ServiceAccountCredentials.from_json_keyfile_name("creds4.json", scope)
    done_putter_client = gspread.authorize(done_putter_creds)
    
    return survey_reader_client, data_getter_client, user_writer_client, done_putter_client


def to_loop():
    survey_reader_client, data_getter_client, user_writer_client, done_putter_client = init()
    full_database_sheet = survey_reader_client.open(
        "CSE Alpha buy/sell stocks (Responses)").sheet1  # Open the survey sheet
    full_database_array = full_database_sheet.get_all_values()
    # print(full_database_array)
    
    iterator = 0
    
    print("IIIIIIIIIII", full_database_array)
    while iterator < len(full_database_array):
        if full_database_array[iterator][-1] != "done":
            current_command = full_database_array[iterator]
            
            execute_command(current_command, data_getter_client, user_writer_client, done_putter_client, iterator)
            time.sleep(2)
        else:
            print("not new")
            print("*_*")
        iterator += 1
    time.sleep(1)


def execute_command(current_command, data_getter_client, user_writer_client, done_putter_client, row_num):
    current_type = current_command[1]
    print(current_type)
    if current_type == "buy public":
        buy_public(current_command, data_getter_client, user_writer_client, done_putter_client, row_num)
    elif current_type == "sell private(make offer)":
        sell_private(current_command, data_getter_client, user_writer_client, done_putter_client, row_num)
    elif current_type == "buy private":
        buyPrivate(current_command, data_getter_client, user_writer_client, done_putter_client, row_num)


def generate_random_code(number_of_digits):
    list_of_chars = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "q", "w", "e", "r", 't', 'y', 'u', 'i', 'o', 'p',
                     'a',
                     's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T',
                     'Y',
                     'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
    password = ""
    for j in range(0, number_of_digits, 1):
        password = password + random.choice(list_of_chars)
    print(password)
    return password


def buy_public(current_row, data_getter_client, user_writer_client, done_putter_client, row_num):
    stock = current_row[3]
    user_code = current_row[2]
    amount = current_row[4]
    
    print("--------------------amount = ", amount)
    print(stock)
    print(user_code)
    
    gallery_sheet = data_getter_client.open("stock_market_sim").sheet1
    
    stock_data = gallery_sheet.get_all_records()
    print("stock dataaaaaaaaaaaaaaaaaaaa- ", stock_data)
    coords_of_stock = cell = gallery_sheet.find(stock)
    print("COOOORDSSS = ", coords_of_stock)
    coords_of_stoc_str = str(coords_of_stock)
    row1 = coords_of_stoc_str[7]
    print("-----row1  ", row1)
    row2 = coords_of_stoc_str[8]
    print("-----row2  ", row2)
    if str(row1).isdigit() & str(row2).isdigit():
        row = (int(row1) * 10) + int(row2)
    else:
        row = row1
    
    print("-----row  ", row)
    price = stock_data[int(row) - 2]["Average\nPrice"]
    num_of_stocks = stock_data[int(row) - 2]["Number of\nShares"]
    print("--------------------price = ", price)
    total_cost = int(amount) * int(price)
    print(total_cost)
    user_sheet_str = user_code
    
    user_sheet = user_writer_client.open(user_sheet_str).sheet1
    user_sheet_list = user_sheet.get_all_records()
    latest = len(user_sheet_list) + 1
    print("latest= ", latest)
    print(user_sheet_list)
    current_balance_row = user_sheet_list[0]
    current_balance_val = current_balance_row["Current Balance"]
    print("current balance = ", current_balance_val)
    print("error      ", current_balance_val, " - ", total_cost)
    try:
        current_balance_val = int(current_balance_val.replace(",", ""))
    except:
        current_balance_val = int(current_balance_val)
    new_balance = current_balance_val - total_cost
    if new_balance < 0:
        print("NOT ENOUGH BALANCE")
        print("NOT ENOUGH BALANCE")
        print("NOT ENOUGH BALANCE")
        print("NOT ENOUGH BALANCE")
        print("NOT ENOUGH BALANCE")
        print("NOT ENOUGH BALANCE")
        print("NOT ENOUGH BALANCE")
    
    print("new_balance = ", new_balance)
    
    if new_balance > 0:
        user_sheet.update_cell(2, 1, new_balance)
        # check if stock exists
        cell_list = user_sheet.findall(stock)
        print("dupe list = ", cell_list)
        print(cell_list)
        
        # new shit
        user_sheet.update_cell(latest + 1, 2, stock)
        user_sheet.update_cell(latest + 1, 3, amount)
        user_sheet.update_cell(latest + 1, 4, price)
        
        print("RRRRROOOOOOWWW", row)
        new = int(num_of_stocks) - float(amount)
        gallery_sheet.update_cell(int(row), 11, new)
        
        write_done(done_putter_client, row_num)


def sell_private(current_row, data_getter_client, user_writer_client, done_putter_client, row_num):
    global current_amount
    print("why are you here??????????????????????????????????????????????????????????????")
    """
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    full_database_sheet = client.open("buy/sell stocks (Responses)").sheet1  # Open the spreadhseet
    gallery_sheet = client.open("stock_market_sim").sheet1
    """
    
    private_sheet = done_putter_client.open("private_market").sheet1
    private_sheet_records = private_sheet.get_all_records()
    print("PRIVATE SHEEEEEET = = ", private_sheet_records)
    ref_sheet = done_putter_client.open("Ref Sheet").sheet1
    ref_sheet_records = ref_sheet.get_all_records()
    
    sellers_user_code = current_row[5]
    for i in ref_sheet_records:
        print("reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeef;;; ", i)
        
        code = i["username"]
        if code == sellers_user_code:
            team_name = i['team name']
    # print(team_name)
    row_num_a = len(private_sheet_records) + 2
    print("row_num = ", row_num_a)
    print("PRIVATE SHEEEEET  ", private_sheet_records)
    
    stock_to_sell = current_row[6]
    print("STOCK NAME = = ", stock_to_sell)
    # sellers_user_code = current_row['Your user code is:']
    amount_to_sell = current_row[7]
    sellers_price_per_share = current_row[8]
    print("current row ----- ", current_row)
    user_sheet_str = sellers_user_code
    user_sheet = user_writer_client.open(user_sheet_str).sheet1
    user_sheet_list = user_sheet.get_all_records()
    stock_present = False
    x = 0
    ###ldldldddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
    gallery_sheet = data_getter_client.open("stock_market_sim").sheet1
    stock_data = gallery_sheet.get_all_records()
    coords_of_stock = cell = gallery_sheet.find(stock_to_sell)
    coords_of_stoc_str = str(coords_of_stock)
    row1 = coords_of_stoc_str[7]
    print("-----row1  ", row1)
    row2 = coords_of_stoc_str[8]
    print("-----row2  ", row2)
    if str(row1).isdigit() & str(row2).isdigit():
        row = (int(row1) * 10) + int(row2)
    else:
        row = row1
    
    print("-----row  ", row)
    price = stock_data[int(row) - 2]["Average\nPrice"]
    
    if float(sellers_price_per_share) <= float(price) * 1.5 and float(sellers_price_per_share) >= float(price) * 0.5:
        print("PASSED|PASSED|PASSED|PASSED   ", " sellers_price_per_share ", sellers_price_per_share,
              " float(price)*1.5 ", float(price) * 1.5, " float(price)*0.5 ", float(price) * 0.5)
        
        for i in user_sheet_list:
            x = x + 1
            if stock_to_sell == i["Stock"]:
                current_amount = i["Amount"]
                stock_present = True
                break
            
            print("X is ", x)
        if stock_present:
            # 99,00,1 ->99001
            new_amount_of_stock_to_sell = int(current_amount) - int(amount_to_sell)
            print(new_amount_of_stock_to_sell)
            if new_amount_of_stock_to_sell >= 0:
                print("something")
                user_sheet.update_cell(x + 1, 3, str(new_amount_of_stock_to_sell))
                row = len(private_sheet_records) + 2
                
                private_sheet.update_cell(row, 1, stock_to_sell)
                private_sheet.update_cell(row, 2, team_name)
                private_sheet.update_cell(row, 3, generate_random_code(6))
                private_sheet.update_cell(row, 4, amount_to_sell)
                private_sheet.update_cell(row, 5, sellers_price_per_share)
                private_sheet.update_cell(row, 6, '=D' + str(row) + '*E' + str(row))
                write_done(done_putter_client, row_num) # try1
                
                if new_amount_of_stock_to_sell == 0:
                    user_sheet.delete_row(x + 1)
            
            else:
                write_done(done_putter_client, row_num)
    else:
        print("tried to sell for too LOW or too HIGH")
        write_done(done_putter_client, row_num)


def buyPrivate(current_row, data_getter_client, user_writer_client, done_putter_client, row_num):
    ref_sheet = done_putter_client.open("Ref Sheet").sheet1
    ref_sheet_records = ref_sheet.get_all_records()
    
    private_sheet = done_putter_client.open("private_market").sheet1
    private_sheet_records = private_sheet.get_all_records()
    print("currr = === = ", current_row)
    
    unique_code = current_row[11]
    buyers_username = current_row[9]
    team_name_of_seller = current_row[10]
    
    print("CHECK THIS = = = = ", private_sheet_records)
    x = 0
    code_present = False
    for i in private_sheet_records:
        x += 1
        print("comparing ", i["Unique Transaction ID"], " to ", unique_code)
        if i["Unique Transaction ID"] == unique_code:
            price = i["Cost per Share"]
            amount = i["Amount"]
            stock_name = i["Company name"]
            code_present = True
            break
    if code_present:
        print("TRUE")
        print(price)
        print(amount)
        print("row to delete = ", x + 1)
        private_sheet.delete_row(x + 1)
        
        print("team name of seller ", team_name_of_seller)
        print("REEf", ref_sheet_records)
        sellers_code = "rain"
        for i in ref_sheet_records:
            if i["team name"] == team_name_of_seller:
                sellers_code = i["username"]
                break
        
        if sellers_code == "rain":
            print("failure")
        else:
            print("going forward")
            
            if sellers_code == buyers_username:
                print("buyer == seller")
                seller_sheet = user_writer_client.open(sellers_code).sheet1
                seller_sheet_list = seller_sheet.get_all_records()
                latest = len(seller_sheet_list) + 1
                seller_sheet.update_cell(latest + 1, 2, stock_name)
                seller_sheet.update_cell(latest + 1, 3, amount)
                seller_sheet.update_cell(latest + 1, 4, price)
                write_done(done_putter_client, row_num)
            
            else:
                buyer_sheet = user_writer_client.open(buyers_username).sheet1
                buyer_sheet_list = buyer_sheet.get_all_records()
                buyer_latest = len(buyer_sheet_list) + 1
                
                buyer_current_cash = buyer_sheet_list[0]["Current Balance"]
                buyer_new_cash = buyer_current_cash - (amount * price)
                if buyer_new_cash > 0:
                    buyer_sheet.update_cell(2, 1, buyer_new_cash)
                    buyer_sheet.update_cell(buyer_latest + 1, 2, stock_name)
                    buyer_sheet.update_cell(buyer_latest + 1, 3, amount)
                    buyer_sheet.update_cell(buyer_latest + 1, 4, price)
                # ---------------------------------------------------------------------------
                seller_sheet = user_writer_client.open(sellers_code).sheet1
                seller_sheet_list = seller_sheet.get_all_records()
                
                seller_current_cash = seller_sheet_list[0]["Current Balance"]
                seller_new_cash = seller_current_cash + (amount * price)
                if seller_new_cash > 0:
                    seller_sheet.update_cell(2, 1, seller_new_cash)
                write_done(done_putter_client, row_num)
    
    else:
        print("transaction does not exist")
        write_done(done_putter_client, row_num)


def write_done(done_putter_client, row_num):
    database_sheet = done_putter_client.open("CSE Alpha buy/sell stocks (Responses)").sheet1
    print(
        "rooooooooooooooooooooowwoowowowowwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
        row_num + 1)
    database_sheet.update_cell(row_num + 1, 14, "done")
    print("I PUT DONE!!!!!!!!!!")


# ----------------------------------------------------------------------------------------------------------------------
while True:
    to_loop()
