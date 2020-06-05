from db import *

class Paginator:
    def __init__(self, contex, start_page, obj_per_page, data):
        self.page = start_page-1
        self.obj_per_page = obj_per_page
        self.data = data
        self.contex = contex    
    
    def is_last_page(self, page):
        l = len(self.data)
        max_pages = l // self.obj_per_page + 1
        if self.page + 1 >= max_pages:
            return True
        return False
    
    def is_end(self):
        l = len(self.data)
        max_pages = l // self.obj_per_page + 1
        if self.page + 1 > max_pages:
            return True
        return False

    def next(self):
        if not self.is_end():
            is_last = False
            if not self.is_last_page(self.page):
                res = self.data[self.page*self.obj_per_page: self.page*self.obj_per_page+self.obj_per_page]
            else:
                res = self.data[self.page*self.obj_per_page:]
                is_last = True
            self.page += 1
            self.contex.paginator_page += 1
            self.contex.save()

            if len(res)>0:
                return res, is_last
            else:
                return False, True
        else: 
            return False, True
    
                