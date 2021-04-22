import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from datetime import datetime
import time
from datetime import datetime

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
            time.sleep(25)
        else:
            print("not new")
            print("*_*")
        iterator += 1
    time.sleep(10)


def execute_command(current_command, data_getter_client, user_writer_client, done_putter_client, row_num):
    current_type = current_command[1]
    print(current_type)
    if current_type == "buy public":
        buy_public(current_command, data_getter_client, user_writer_client, done_putter_client, row_num)
    elif current_type == "sell private(make offer)":
        sell_private(current_command, data_getter_client, user_writer_client, done_putter_client, row_num)
    elif current_type == "buy private":
        buyPrivate(current_command, data_getter_client, user_writer_client, done_putter_client, row_num)


def buy_public(current_row, data_getter_client, user_writer_client, done_putter_client, row_num):
    stock = current_row[3]
    user_code = current_row[2]
    amount = current_row[4]
    
    print("--------------------amount = ", amount)
    print(stock)
    print(user_code)
    
    gallery_sheet = data_getter_client.open("stock_market_sim").sheet1
    
    stock_data = gallery_sheet.get_all_records()
    print("stock dataaaaaaaaaaaaaaaaaaaa- ",stock_data)
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
        if cell_list == []:
            user_sheet.update_cell(latest + 1, 2, stock)
            user_sheet.update_cell(latest + 1, 3, amount)
        else:
            
            val = cell_list[0]
            print(val)
            coords_of_stock_row_str = str(val)
            
            stock_val = coords_of_stock_row_str[7]
            print("val====", stock_val)
            current_amount = user_sheet_list[-1]["Amount"]
            print("currrrrrr", current_amount)
            new_amount = current_amount + int(amount)
            print("new amount = ", new_amount)
            user_sheet.update_cell(latest, 2, stock)
            user_sheet.update_cell(latest, 3, new_amount)
        print("RRRRROOOOOOWWW", row)
        new = int(num_of_stocks) - float(amount)
        gallery_sheet.update_cell(int(row), 11, new)
        
        write_done(done_putter_client, row_num)


def sell_private(current_row, data_getter_client, user_writer_client, done_putter_client, row_num):
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
    #print(team_name)
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
    
    if float(sellers_price_per_share)<=float(price)*1.5 and float(sellers_price_per_share)>=float(price)*0.5:
        print("PASSED|PASSED|PASSED|PASSED   ", " sellers_price_per_share ", sellers_price_per_share," float(price)*1.5 ", float(price)*1.5, " float(price)*0.5 " , float(price)*0.5)
    
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
            private_sheet.update_cell(row, 3, amount_to_sell)
            private_sheet.update_cell(row, 4, sellers_price_per_share)
            private_sheet.update_cell(row, 5, '=C' + str(row) + '*D' + str(row))
            
            write_done(done_putter_client, row_num)
    else:
        print("tried to sell for too LOW or too HIGH")
        write_done(done_putter_client, row_num)


def buyPrivate(current_row, data_getter_client, user_writer_client, done_putter_client, row_num):
    ref_sheet = done_putter_client.open("Ref Sheet").sheet1
    ref_sheet_records = ref_sheet.get_all_records()
    
    private_sheet = done_putter_client.open("private_market").sheet1
    private_sheet_records = private_sheet.get_all_records()
    
    buyers_username = current_row[9]
    team_name_of_seller = current_row[10]
    name_of_stock = current_row[11]
    x = 0
    stock_present = False
    for i in private_sheet_records:
        x += 1
        if i["Company name"] == name_of_stock and i["Team Name of seller"] == team_name_of_seller:
            price = i["Total Cost"]
            amount = i["Amount"]
            stock_present = True
            break
    if stock_present == True:
        print("TRUE")
        print(price)
        print(amount)
    
    private_sheet = done_putter_client.open("private_market").sheet1
    private_sheet_records = private_sheet.get_all_records()
    buyers_code = current_row[9]
    print(buyers_code)
    sellers_team_name = current_row[10]
    print(sellers_team_name)
    
    for i in ref_sheet_records:
        if i["team name"] == sellers_team_name:
            sellers_code = i["username"]
    
    stock = current_row[11]
    print(stock)
    print(private_sheet_records)
    x = 2
    found = False
    
    for i in private_sheet_records:
        print("hea")
        print("Company name = = = = ", i["Company name"], "staxxxx = ", stock)
        print("iIiIiI", i)
        if i["Company name"] == stock and i["Team Name of seller"] == sellers_team_name:
            found = True
            price = i["Total Cost"]
            
            amount = i["Amount"]
            print("AAAMMMOOOUUUNNNT + + = ", amount)
            
            buyer_sheet_str = buyers_code
            buyer_sheet = user_writer_client.open(buyer_sheet_str).sheet1
            buyer_sheet_list = buyer_sheet.get_all_records()
            
            seller_sheet_str = sellers_code
            seller_sheet = user_writer_client.open(seller_sheet_str).sheet1
            seller_sheet_list = seller_sheet.get_all_records()
            
            buyer_current_cash = buyer_sheet_list[0]["Current Balance"]
            seller_current_cash = seller_sheet_list[0]["Current Balance"]
            buyer_new_cash = int(buyer_current_cash) - int(price)
            if buyer_new_cash > 0:
                print("OOOOOKKKKK")
                print(buyer_new_cash)
                if (buyer_sheet_str != seller_sheet_str):
                    buyer_sheet.update_cell(2, 1, buyer_new_cash)
                    seller_current_cash = seller_current_cash
                    seller_new_cash = int(seller_current_cash) + int(price)
                    print(seller_new_cash)
                    seller_sheet.update_cell(2, 1, seller_new_cash)
                    write_done(done_putter_client, row_num)
            else:
                print("NOT ENOUGH BALANCE")
                print("NOT ENOUGH BALANCE")
                print("NOT ENOUGH BALANCE")
                print("NOT ENOUGH BALANCE")
                print("NOT ENOUGH BALANCE")
                print("NOT ENOUGH BALANCE")
                print("NOT ENOUGH BALANCE")
        
        else:
            
            x += 1
    
    if found:
        buyer_sheet_str = buyers_code
        buyer_sheet = user_writer_client.open(buyer_sheet_str).sheet1
        buyer_sheet_list = buyer_sheet.get_all_records()
        buyer_current_cash = buyer_sheet_list[0]["Current Balance"]
        price = i["Total Cost"]
        buyer_new_cash = int(buyer_current_cash) - int(price)
        if buyer_new_cash > 0:
            latest = len(buyer_sheet_list) + 1
            cell_list = buyer_sheet.findall(stock)
            print("cccc", cell_list)
            if cell_list == []:
                buyer_sheet.update_cell(latest + 2, 2, stock)
                buyer_sheet.update_cell(latest + 2, 3, amount)
            else:
                
                val = cell_list[0]
                print(val)
                coords_of_stock_row_str = str(val)
                
                stock_val = coords_of_stock_row_str[7]
                print("val====", stock_val)
                current_amount = buyer_sheet_list[-1]["Amount"]
                print("currrrrrr", current_amount)
                amount = i["Amount"]
                print("current_amount= ", current_amount)
                print("amount= ", amount)
                new_amount = int(current_amount) + int(amount)
                print("new amount = ", new_amount)
                buyer_sheet.update_cell(latest, 2, stock)
                buyer_sheet.update_cell(latest, 3, new_amount)
                print(
                    "bbbbbbbbbbbbppppppppppbpbpbppbpbpbpbpbpbpbpbpbppbpbpbpbpbpbpbpbpbpbpbpbppbppbpbpbpbpbpbpbpbpbpbpb   ",
                    x)
            private_sheet.delete_rows(x-1)
            write_done(done_putter_client, row_num)
        else:
            print("NOT ENOUGH BALANCE")
            print("NOT ENOUGH BALANCE")
            print("NOT ENOUGH BALANCE")
            print("NOT ENOUGH BALANCE")
            print("NOT ENOUGH BALANCE")
            print("NOT ENOUGH BALANCE")
            print("NOT ENOUGH BALANCE")


def write_done(done_putter_client, row_num):
    database_sheet = done_putter_client.open("CSE Alpha buy/sell stocks (Responses)").sheet1
    print("rooooooooooooooooooooowwoowowowowwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww", row_num + 1)
    database_sheet.update_cell(row_num + 1, 14, "done")
    print("I PUT DONE!!!!!!!!!!")


# ----------------------------------------------------------------------------------------------------------------------
while True:
    to_loop()
