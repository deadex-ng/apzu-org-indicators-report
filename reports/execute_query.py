from utils.constants import UPPER_NENO, LOWER_NENO
import openpyxl
class ExecuteQuery:
    def __init__(self, cursor_obj, path):
        self.cursor_obj = cursor_obj
        self.path = path 

    def execute_query(self,sql, site,letter) -> None:
        end_date = '"2024-03-31"'
        if site == 'Upper':
            hc = UPPER_NENO
        elif site == 'Lower': 
            hc = LOWER_NENO
        else:
            print("Please specify the site")
        
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name('Sheet')  
        counter = 2
        for i in range(len(hc)):
            facility = hc[i]
            facility = '"' + facility + '"'
            formatted_qry = sql.format(facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            x1 = sheet["B" + str(counter)]
            if '"'+ x1.value + '"' == facility:
                sheet[letter + str(counter)] = len(response)
            counter+=1
        wb.save(self.path)

    def execute_count_query(self,sql, site,letter) -> None:
        if site == 'Upper':
            hc = UPPER_NENO
        elif site == 'Lower': 
            hc = LOWER_NENO
        else:
            print("Please specify the site")
        
        wb = openpyxl.load_workbook(self.path)
        sheet = wb.get_sheet_by_name('Sheet')  
        counter = 2
        for i in range(len(hc)):
            facility = hc[i]
            facility = '"' + facility + '"'
            formatted_qry = sql.format(facility)
            qry_lst = formatted_qry.split("---")
            for qry in qry_lst:
                self.cursor_obj.execute(qry)
            response = self.cursor_obj.fetchall()
            print(response)
            x1 = sheet["B" + str(counter)]
            if '"'+ x1.value + '"' == facility:
                sheet[letter + str(counter)] = response[0][0]
            counter+=1
        wb.save(self.path)
