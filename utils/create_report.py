from constants import LOWER_NENO, UPPER_NENO, HIV_HEADERS, NCD_HEADERS
import openpyxl
import argparse

def get_sheet(wb, report_path):
    try:
        cur_sht = wb.get_sheet_by_name('Sheet')
        return cur_sht
    except Exception as e:
        print(e)

def save(report_path):
    wb.save(report_path)

def write_facilities(cur_sht, facilities, report_path):
    hc_num = len(facilities)
    counter = 2
    for i in range(hc_num):
        cur_sht["B" + str(counter)] = facilities[i]
        counter+= 1 
    save(report_path)
    print("Finished writing facilities")    
def write_headers(cur_sht, headers, report_path):
    letters = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
    num_headers = len(headers)
    counter = 0
    for i in range(num_headers):
        cur_sht[letters[counter] + "1"] = headers[counter]
        counter+=1
    save(report_path)
    print("Finished writing headers")
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', type =str, help = 'path of the report')
    parser.add_argument('-s', type = str, help = "site of the report")
    parser.add_argument('-t', type = str, help = "type of the report")

    args = parser.parse_args()

if args.p is None:
    print("Please add file path")
else:
    report_path = args.p
    wb = openpyxl.Workbook()
    wb.save(report_path)
    wb = openpyxl.load_workbook(report_path)
    sheet = get_sheet(wb, report_path)
    if args.t is None:
        print("Please specifiy the type of report")
    elif args.t == "HIV":
        write_headers(sheet, HIV_HEADERS, report_path)
    elif args.t == "NCD":
        write_headers(sheet, NCD_HEADERS, report_path)
    else:
        print("Please specifiy the type of report")

if args.s == "Lower":
    write_facilities(sheet, LOWER_NENO, report_path)
if args.s == "Upper":
    write_facilities(sheet, UPPER_NENO, report_path)