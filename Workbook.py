import openpyxl as xl

class Workbook:
    def __init__(self):
        self.workbook=xl.Workbook()
        self.worksheet = self.workbook.active
        self.worksheet.title = "Data"
        self.worksheet.cell(1,1).value='评论'
        self.worksheet.cell(1,2).value='省份'
        self.Line=1

    def Add_Line(self,Comments,Province):
        self.Line=self.worksheet.max_row+1
        self.worksheet.cell(self.Line,1).value=Comments
        self.worksheet.cell(self.Line,2).value=Province
    
    def Save(self,Path):
        self.workbook.save(Path)
