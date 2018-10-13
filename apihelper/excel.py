from openpyxl import Workbook
from openpyxl.styles import Font,colors


class Write_xls(object):
    def __init__(self,name):
        self.file_name = name
        self.wb = Workbook()
        self.ws = self.wb.get_sheet_by_name("Sheet")
        self.row_cnt = 1

    def write_row(self,items,hyper=None):
        for ii,item in enumerate(items):
            cell = self.ws.cell(row = self.row_cnt, column = ii+1)            
            if hyper and ii==0:
                cell.font = Font(underline="single",color=colors.RED)
                cell.value = '=HYPERLINK("%s","%s")'%(hyper,item)
            else:
                cell.value = item
        self.row_cnt += 1
            
    def save(self):
        self.wb.save(self.file_name)
        
            
        

if __name__=="__main__":
    row = ['ciocoloc0',34,45]
    wxls = Write_xls('test.xlsx')
    wxls.write_row(row,hyper = 'http://openpyxl.readthedocs.io/en/default/styles.html')
    wxls.save()
